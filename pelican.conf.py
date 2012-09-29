#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u"Georges Dubus"
SITENAME = u"Compile-toi toi même"
SITESUBTITLE = u"(Georges Dubus)"
SITEURL = 'http://compiletoi.net'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'en'
LOCALE = ('en_US.UTF-8', 'fr_FR.UTF8')

THEME = 'stolenidea'

MENUITEMS = (
	('Archives', SITEURL + 'archives.html'),
	('Tags', SITEURL + 'tags.html')
)

# Blogroll
# LINKS = (
#     ('Pelican', 'http://docs.notmyidea.org/alexis/pelican/'),
#     ('Python.org', 'http://python.org'),
#     ('Jinja2', 'http://jinja.pocoo.org'),
#     ('You can modify those links in your config file', '#')
#          )

# Social widget
SOCIAL = (
          ('Github', 'https://github.com/madjar'),
          ('Twitter', 'http://twitter.com/georgesdubus'),
          ('Google+', 'https://plus.google.com/u/0/104750974388692229541'),
         )

DEFAULT_PAGINATION = False


PATH = ('src')
FILES_TO_COPY = (('CNAME', 'CNAME'),)

# TWITTER_USERNAME = 'georgesdubus'
DISQUS_SITENAME = 'compiletoi'
GOOGLE_ANALYTICS = 'UA-31800325-1'
