Fast scraping in python with asyncio
====================================
:date: 2014-03-02 17:50
:tags: python

Web scraping is one of those subjects that often appears in python
discussions. There are many ways to do this, and there doesn't seem to
be one best way. There are fully fledged frameworks like scrapy_ and more
lightweight libraries like mechanize_. Do-it-yourself solutions are
also popular: one can go a long way by using requests_ and
beautifulsoup_ or pyquery_.

.. _scrapy: http://scrapy.org
.. _mechanize: http://wwwsearch.sourceforge.net/mechanize/
.. _requests: http://python-requests.org/
.. _beautifulsoup: http://www.crummy.com/software/BeautifulSoup/
.. _pyquery: http://pythonhosted.org/pyquery/

The reason for this diversity is that "scraping" actually covers
multiple problems: you don't need to same tool to extract data from
hundreds of pages and to automate some web workflow (like filling a
few forms and getting some data back). I like the do-it-yourself
approach because it's flexible, but it's not well-suited for massive
data extraction, because `requests` does requests synchronously, and
many requests means you have to wait a long time.

In this blog post, I'll present you an alternative to `requests` based
on the new asyncio library : aiohttp_. I use it to write small
scraper that are really fast, and I'll show you how.

.. _aiohttp: https://github.com/KeepSafe/aiohttp

Basics of asyncio
-----------------

asyncio_ is the asynchronous IO library that was introduced in python
3.4. You can also get it from pypi on python 3.3. It's quite complex
and I won't go too much into details. Instead, I'll explain what you
need to know to write asynchronous code with it. If you want to know
more about, I invite you to read its documentation.

.. _asyncio: http://docs.python.org/3.4/library/asyncio.html

To make it simple, there are two things you need to know about :
coroutines and event loops. Coroutines are like functions, but they can
be suspended or resume at certain points in the code. This is used to
pause a coroutine while it waits for an IO (an HTTP request, for
example) and execute another one in the meantime. We use the ``yield
from`` keyword to state that we want the return value of a
coroutine. An event loop is used orchestrate the execution of the coroutines.

There is much more to asyncio, but that's all we need to know for
now. It might be a little unclear from know, so let's look at some code.

aiohttp
-------

aiohttp_ is a library designed to work with asyncio, with an API that
looks like requests'. It's not very well documented for now, but there
are some very useful examples_. We'll first show its basic usage.

.. _examples: https://github.com/KeepSafe/aiohttp/tree/master/examples

First, we'll define a coroutine to get a page and print it. We use
``asyncio.coroutine`` to decorate a function as a
coroutine. ``aiohttp.request`` is a coroutine, and so is the ``read``
method, so we'll need to use ``yield from`` to call them. Apart from
that, the code looks pretty straightforward:

.. code-block:: python

  @asyncio.coroutine
  def print_page(url):
      response = yield from aiohttp.request('GET', url)
      body = yield from response.read_and_close(decode=True)
      print(body)

As we have seen, we can call a coroutine from another coroutine with
``yield from``. To call a coroutine from synchronous code, we'll need an
event loop. We can get the standard one with
``asyncio.get_event_loop()`` and run the coroutine on it using its
``run_until_complete()`` method. So, all we have to do to run the
previous coroutine is:

.. code-block:: python

  loop = asyncio.get_event_loop()
  loop.run_until_complete(print_page('http://example.com'))

A useful function is ``asyncio.wait``, which takes a list a coroutines
and returns a single coroutine that wrap them all, so we can write:

.. code-block:: python

  loop.run_until_complete(asyncio.wait([print_page('http://example.com/foo'),
                                        print_page('http://example.com/bar')]))

Another one is ``asyncio.as_completed``, that takes a list of coroutines
and returns an iterator that yield the coroutines in the order in which
they are completed, so that when you iterate on it, you get each
result as soon as it's available.

Scraping
--------

Now that we know how to do asynchronous HTTP requests, we can write a
scraper. The only other part we need is something to read the html. I
use beautifulsoup_ for that, be others like pyquery_ or lxml_.

.. _lxml: http://lxml.de/

For this example, we'll write a small scraper to get the torrent
links for various linux distributions from the pirate bay.

First of all, a helper coroutine to do get requests:

.. code-block:: python

  @asyncio.coroutine
  def get(*args, **kwargs):
      response = yield from aiohttp.request('GET', *args, **kwargs)
      return (yield from response.read_and_close(decode=True))

The parsing part. This post is not about beautifulsoup, so I'll keep
it dumb and simple: we get the first magnet list of the page:

.. code-block:: python

  def first_magnet(page):
      soup = bs4.BeautifulSoup(page)
      a = soup.find('a', title='Download this torrent using magnet')
      return a['href']


The coroutine. With this url, results are sorted by number of seeders,
so the first result is actually the most seeded:

.. code-block:: python

  @asyncio.coroutine
  def print_magnet(query):
      url = 'http://thepiratebay.se/search/{}/0/7/0'.format(query)
      page = yield from get(url, compress=True)
      magnet = first_magnet(page)
      print('{}: {}'.format(query, magnet))

Finally, the code to call all of this:

.. code-block:: python

  distros = ['archlinux', 'ubuntu', 'debian']
  loop = asyncio.get_event_loop()
  f = asyncio.wait([print_magnet(d) for d in distros])
  loop.run_until_complete(f)

Conclusion
----------

And there you go, you have a small scraper that works
asynchronously. That means the various pages are being downloaded at
the same time, so this example is 3 times faster than the same code
with `requests`. You should now be able to write your own scrapers in
the same way.

You can find the resulting code, including the bonus tracks, in this
gist_.

.. _gist: https://gist.github.com/madjar/9312452

Once you are comfortable with all this, I recommend you take a look at
asyncio_'s documentation and aiohttp examples_, which will show you
all the potential asyncio have.

One limitation of this approach (in fact, any hand-made approach) is
that there doesn't seem to be a standalone library to handle
forms. Mechanize and scrapy have nice helpers to easily submit forms,
but if you don't use them, you'll have to do it yourself. This is
something that bugs be, so I might write such a library at some point
(but don't count on it for now).

Bonus track: don't hammer the server
------------------------------------

Doing 3 requests at the same time is cool, doing 5000, however, is not
so nice. If you try to do too many requests at the same time,
connections might start to get closed, or you might even get banned
from the website.

To avoid this, you can use a semaphore_. It is a synchronization tool
that can be used to limit the number of coroutines that do something
at some point. We'll just create the semaphore before creating the
loop, passing as an argument the number of simultaneous requests we
want to allow:

.. code-block:: python

  sem = asyncio.Semaphore(5)

Then, we just replace:

.. code-block:: python

  page = yield from get(url, compress=True)

by the same thing, but protected by a semaphore:

.. code-block:: python

  with (yield from sem):
      page = yield from get(url, compress=True)

This will ensure that at most 5 requests can be done at the same time.

.. _semaphore: http://docs.python.org/3.4/library/asyncio-sync.html#semaphores

Bonus track: progress bar
-------------------------

This one is just for free: tqdm_ is a nice library to make progress
bars. This coroutine works just like ``asyncio.wait``, but displays a
progress bar indicating the completion of the coroutines passed to
it:

.. code-block:: python

  @asyncio.coroutine
  def wait_with_progress(coros):
      for f in tqdm.tqdm(asyncio.as_completed(coros), total=len(coros)):
          yield from f

.. _tqdm: https://github.com/noamraph/tqdm
