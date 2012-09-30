Quick authentication on pyramid with persona
============================================
:date: 2012-09-29 21:00
:tags: pyramid, persona, python
:status: draft

A few days ago, the first beta of persona_ was released, and I though
it would be nice to try as a authentication mechanism in my next
project. For the pyramid framework, the persona documentation pointed
to this blog post : `Painless Authentication with Pyramid and
BrowserID`. Sadly, this method only provides a special 403 page with a
login button, and a quick look at the internal revealed it wouldn't be
easy to use it another way (say, with a login button on my pages).

.. _persona: https://login.persona.org/
.. _`Painless Authentication with Pyramid and BrowserID`: http://www.rfk.id.au/blog/entry/painless-auth-pyramid-browserid/

So I implemented it myself, and I decided it would be nice to release
it as a library. It's called `pyramid_persona`_, and it's available on
pypi_. The README should explain who to use it, but here is a more
visual demonstration.

.. _`pyramid_persona`: https://github.com/madjar/pyramid_persona
.. _pypi: http://pypi.python.org/pypi/pyramid_persona

The forbidden view
------------------

First, let's show to have it handle authentication and give us a nice
forbidden view. Let's take a small application with a view that says
hello if we are logged in, and returns a 403 otherwise.

.. code-block:: python

    from waitress import serve
    from pyramid.config import Configurator
    from pyramid.response import Response
    from pyramid.security import authenticated_userid
    from pyramid.exceptions import Forbidden

    def hello_world(request):
	userid = authenticated_userid(request)
	if userid is None:
	    raise Forbidden()
	return Response('Hello %s!' % (userid,)) 


    if __name__ == '__main__':
	config = Configurator()
	config.add_route('hello', '/')
	config.add_view(hello_world, route_name='hello')
	app = config.make_wsgi_app()
	serve(app, host='0.0.0.0')

Logically, all we get is an error message:

.. image:: images/pyramid-persona/basic.png

Let's include `pyramid_persona` and add some settings:

.. code-block:: python

    settings = {
        'persona.secret': 'some secret',
        'persona.audience': 'http://localhost:8080'
    }
    config = Configurator(settings=settings)
    config.include('pyramid_persona')

And we have a login button on the forbidden page :

.. image:: images/pyramid-persona/forbidden.png
.. image:: images/pyramid-persona/persona.png
.. image:: images/pyramid-persona/logged_in.png

A login button
--------------

That is nice, but that won't get us far. What would be extra nice

TODO la suite

..
  Local Variables:
  mode: rst
  mode: auto-fill
  mode: flyspell
  ispell-local-dictionary: "english"
  End:
