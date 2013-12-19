Using ZODB with Pyramid on Heroku
=================================

:tags: zodb, pyramid, heroku, python
:status: draft

I recently discovered zodb_ through a `post by Chris McDonough`_.
It's a nice object database that add persistence to normal python
objects.  It works quite well with the traversal mode of pyramid.  I
won't show here how it works or how to use it with pyramid : there
already is an excellent tutorial_ in the pyramid documentation.

.. _`post by Chris McDonough` : http://plope.com/Members/chrism/why_i_like_zodb
.. _zodb : http://zodb.org/
.. _tutorial : http://docs.pylonsproject.org/projects/pyramid/en/1.3-branch/tutorials/wiki/index.html

In this post, I'll show how to make it work on Heroku, which, at the
time I started this, was far from trivial.  In the process of making
this post, I patched RelStorage_ to provide an extension to zodburi_,
thus allowing the use of a postgresql uri in pyramid's config file for
zodb, .

.. _zodburi : https://github.com/Pylons/zodburi
.. _RelStorage : http://pypi.python.org/pypi/RelStorage

Preliminaries
-------------
First of all, let's create a basic project to work with :

.. code-block:: sh

  $ virtualenv -ppython2 venv
  $ source venv/bin/activate
  $ pip install pyramid
  $ pcreate -t zodb herokuproject
  $ cd herokuproject
  $ python setup.py develop

Then, we follow the step 0, 1, 2 and 3 of the cookbook_ to have a basic
heroku setup. Here are the raw commands. You should take a look at the
cookbook_ if you never done this.

.. code-block:: sh

  $ pip freeze | grep -v herokuproject > requirements.txt
  $ echo "web: ./run" > Procfile
  $ cat > run << EOF
  #!/bin/bash
  python setup.py develop
  python runapp.py
  EOF
  $ chmod +x run
  $ cat > runapp.py << EOF
  import os
  
  from paste.deploy import loadapp
  from waitress import serve
  
  if __name__ == "__main__":
      port = int(os.environ.get("PORT", 5000))
      app = loadapp('config:production.ini', relative_to='.')
  
      serve(app, host='0.0.0.0', port=port)
  EOF
  $ wget -O .gitignore https://raw.github.com/github/gitignore/master/Python.gitignore
  $ git init
  $ git add .
  $ git commit -m "initial commit"
  $ heroku create --stack cedar

.. _cookbook : http://docs.pylonsproject.org/projects/pyramid_cookbook/en/latest/deployment/heroku.html

.. note::
   You may wonder what that ugly ``grep`` is doing in the ``pip
   freeze`` command. It is needed because ``pip freeze`` lists all the
   packages installed, including ``herokuproject`` himself. That's why
   we need to remove it from the listing, otherwise pip would try to
   install it from pypi during the setup process, and would fail.


Configuring the database
------------------------

We now have a project with a basic setup to deploy to heroku. All we
have to do is configure the backend for zodb. We will use RelStorage_,
which provide a Postgres backend for zodb, and connect to the postgres
database provided by heroku.

Enable the database at heroku
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First let's tell heroku we want a database. For that, we will need a
verified heroku account. This means you'll have to give your credit
card number to them. They won't bill you if you don't use non free
features, so this won't be a problem. We'll use a `dev plan`_.

.. _dev plan : https://devcenter.heroku.com/articles/heroku-postgres-dev-plan

.. code-block:: sh

  $ heroku addons:add heroku-postgresql:dev

Look at the name given to your database (mine is
``HEROKU_POSTGRESQL_CRIMSON``), and make it the default database
(available as ``DATABASE_URL`` using
the pg:promote command.

.. code-block:: sh

  $ heroku pg:promote HEROKU_POSTGRESQL_CRIMSON  # Replace this with yours

Installing the dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~

We'll need the postgres support in RelStorage, so let's add it to our
``setup.py``. This will install all we need (psycopg2 and zodburi).

.. code-block:: python

  requires = [
      'pyramid',
      'pyramid_zodbconn',
      'pyramid_tm',
      'pyramid_debugtoolbar',
      'ZODB3',
      'waitress',
      'relstorage[postgresql]',  # <--- add this line
      ]

Then, we install the new dependencies :

.. code-block:: sh

  $ python setup.py develop

Configuring the app
~~~~~~~~~~~~~~~~~~~

The tricky part is that heroku provides us the database as an
environment variable (``DATABASE_URL``), so we must add a little bit
of code to the application setup for this to work. But first, let's
modify the ``production.ini`` file. Replace the line

.. code-block:: ini

  zodbconn.uri = file://%(here)s/Data.fs?connection_cache_size=20000

with the line 

.. code-block:: ini

  zodbconn.args = ?connection_cache_size=20000

Then, add add this in to the beginning of the main function in
``herokuproject/__init__.py`` :

.. code-block:: python

  if 'DATABASE_URL' in os.environ:
    settings['zodbconn.uri'] =  os.environ['DATABASE_URL'] + settings['zodbconn.args']

Also add ``import os`` at the beginning of that same file.

This will make your app construct the zodb uri at startup using the
database provided by heroku and the arguments provided in the
configuration file. This way, any command can be run on heroku,
including ``pshell``.

Deploying
---------

We're nearly good. Let's update our requirements.txt and commit all
this.


.. code-block:: sh

  $ pip freeze | grep -v herokuproject > requirements.txt
  $ git commit -a -m "added zodb support for heroku"

.. note::
   The ``pip freeze`` command might send a warning looking like "*Error when trying to get requirement for VCS system Command /usr/bin/git config remote.origin.url failed with error code 1 in /somepath/herokuproject, falling back to uneditable format*
   *Could not determine repository location of /somepath/herokuproject*".
   This is because we use git and pip is unable to determine what the
   public address of the repository is. This is not a problem, as we
   don't want it to add herokuproject to the requirements.txt
   file. You can safely ignore this warning.

All should be good, so I direct you back to the cookbook_ to
deploy. In short, you can run :

.. code-block:: sh

  $ git push heroku master
  $ heroku scale web=1


BONUS : Using the database from your computer
---------------------------------------------

At some point, you might want to manipulate the database directly. You
could use the ``heroku run`` command to run a pshell on the server,
but that's not necessary, and that could be billed if you take too
much time. Instead, you can connect to the database from your
computer.

For that, run ``heroku config``, and look for the ``DATABASE_URL``
variable, which looks like
``postgres://something:somethingelse@somehost.amazonaws.com:12345/somedb``. Copy
that variable, and set it as an environment variable locally by
running

.. code-block:: sh

  $ export DATABASE_URL=postgres://something:somethingelse@somehost.amazonaws.com:12345/somedb

Now you can run ``pshell production.ini`` and do whatever you want with
the database.

Conclusion
----------

There, you have a working deployment on heroku of pyramid configured
to use zodb. These instructions are for a new project, but they can easily
be adapted for an existing project.

The main point of this post, which is the modification in
``__init.py__`` could easily be adapted to configure sqlalchemy for
heroku.

I hope this was helpful. If you have any comment to make about this,
please do so. If nobody objects this method, I'll update the cookbook
with the interesting part of this post.

..
  Local Variables:
  mode: rst
  mode: auto-fill
  mode: flyspell
  ispell-local-dictionary: "english"
  End:
