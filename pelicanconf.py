#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Georges Dubus'
SITENAME = 'Compile-toi toi même'
SITESUBTITLE = u'(Georges Dubus)'         # TODO: remove in next version ?
SITEURL = ''
ABSOLUTE_SITEURL = SITEURL                # TODO: remove

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'en'
LOCALE = ('en_US.UTF-8', 'fr_FR.UTF8')    # TODO: toujours d'actualité ?

THEME = 'stolenidea'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

MENUITEMS = (
	('Archives', SITEURL + '/archives.html'),
	('Tags', SITEURL + '/tags.html')
)

# Social widget
SOCIAL = (
          ('Github', 'https://github.com/madjar'),
          ('Twitter', 'http://twitter.com/georgesdubus'),
          ('Google+', 'https://plus.google.com/u/0/104750974388692229541'),
         )
# TWITTER_USERNAME = 'georgesdubus'

DEFAULT_PAGINATION = 10                   # TODO: voir si je dois modifier quelque chose pour ça

PATH = ('content')
STATIC_PATHS = ['CNAME', 'images']


# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
