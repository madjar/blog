Quick authentication on pyramid with persona
============================================
:date: 2012-09-01 15:30
:tags: pyramid, persona, python

A few days ago, the first beta of persona_ was released, and I thought
it would be nice to try it as a authentication mechanism in my next
project. For the pyramid framework, the persona documentation pointed
to this blog post : `Painless Authentication with Pyramid and
BrowserID`, which describes how to use `pyramid_whoauth` with
`repoze.who.plugins.browserid` to use persona in pyramid.

Sadly, this method only provides a special 403 page with a
login button, and no obvious way to put a login button on another
page. A quick look at the internals revealed it wouldn't be easy to do
so, as most of the work is done inside a wsgi application. To have a
login button, I would have to rewrite the generation of the javascript
that communicates with the persona api, and probably most of the
login code in order to keep the csrf verification.

.. _persona: https://login.persona.org/
.. _`Painless Authentication with Pyramid and BrowserID`: http://www.rfk.id.au/blog/entry/painless-auth-pyramid-browserid/

So, instead of re-implementing half of it and try to plugin it with
existing implementation, I decided to rewrite it from scratch, and I
though it would be nice to release it as a library. It's called
`pyramid_persona`_, and it's available on pypi_. The README should
explain how to use it, but here is a more visual demonstration.

.. _`pyramid_persona`: https://github.com/madjar/pyramid_persona
.. _pypi: http://pypi.python.org/pypi/pyramid_persona

The forbidden view
------------------

First, let's show how to have it handle authentication and give us a nice
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

Of course, all we get is an error message:

.. image:: images/pyramid-persona/basic.png

Let's include `pyramid_persona` and add some settings. The secret is
used to sign the cookies, and the audience is a security feature of
persona, to prevent an attacker from logging into your website using
the login process from another website.

.. code-block:: python

    settings = {
        'persona.secret': 'some secret',
        'persona.audiences': 'http://localhost:8080'
    }
    config = Configurator(settings=settings)
    config.include('pyramid_persona')

We now have a login button on the forbidden page, and the login
process works as expected.

.. image:: images/pyramid-persona/forbidden.png

Clicking on the login button opens the persona login form (in french
for me, because I'm french).

.. image:: images/pyramid-persona/persona.png

Once it's done, we are logged in, the page is reloaded, and everything
works as expected.

.. image:: images/pyramid-persona/logged_in.png

A login button
--------------

We just got a nice, nearly free login system. It would be even nicer
to have login buttons on arbitrary pages.

That won't be hard. There are some html involved, so let us create a
template for this one. We change the view and the configuration a
little :

.. code-block:: python

    def hello_world(request):
	userid = authenticated_userid(request)
	return {'user': userid}

    # ...

	settings = {
	    'persona.secret': 'some secret',
	    'persona.audiences': 'http://localhost:8080',
	    'mako.directories': '.',  # Where to find the template file
	}

    # ...

    config.add_view(hello_world, route_name='hello', renderer='hello.mako')

And we create a `hello.mako` file in the same directory :

.. code-block:: html

    <html>
    <head>
	<script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
	<script src="https://login.persona.org/include.js" type="text/javascript"></script>
	<script type="text/javascript">${request.persona_js}</script>
    </head>
    <body>
    <h1>Persona test page</h1>
    Hello ${user}
    ${request.persona_button}
    </body>
    </html>

We need to include the persona api, jquery, and add a little bit of
javascript needed to make persona work (it is provided by
`request.persona_js`). We use `request.persona_button` which provides
a simple login/logout button depending on whether the user is logged
in. Here is the result :

.. image:: images/pyramid-persona/button_out.png
.. image:: images/pyramid-persona/button_in.png

The button can of course be customized, as can the javascript if you
want to more than just reload the page on login. For more on this,
look at the README.

Conclusion
----------

`pyramid_persona` provides a quick to setup authentication method,
that can be customized to grow with your app. It is available on
pypi_, so it's pip installable. You can check the readme and the
source on github_. Of course, issue reports and suggestions are welcome.

.. _github: https://github.com/madjar/pyramid_persona

..
  Local Variables:
  mode: rst
  mode: auto-fill
  mode: flyspell
  ispell-local-dictionary: "english"
  End:
