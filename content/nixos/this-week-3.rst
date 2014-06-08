This Week in NixOS, third issue
===============================
:date: 2014-06-08 21:00
:slug: this-week-in-nixos-3

Welcome to the third issue of `This Week in NixOS`. Nix is a purely
functional package manager that aims at solving old problems with a
new approach, and NixOS is the distribution based on Nix. This is an
overview of what happened in the development of NixOS and in its
community this week. A lot of things happen in a lot of places and I
might miss some, so if you want to make sure that something is
mentionned in the next issue, send me an email_!

.. _email: mailto:georges.dubus@gmail.com?subject=This%20Week%20in%20NixOS%20Suggestion

Nix itself
----------

Nothing new in Nix. However, emacs users will be happy to know that
`the nix-mode has been added to melpa
<http://melpa.milkbox.net/#/nix-mode>`_.

Nixpkgs
-------

A change in `openssl
<https://github.com/NixOS/nixpkgs/commit/15f092d7a7088ef1fadb059f305685da045fd979>`_
led to a full recompilation of nixpkgs, which hammered the hydra build
machines for a few days. This sparkled a `discussion on the mailing
list <http://comments.gmane.org/gmane.linux.distributions.nixos/13216>`_
on the best way to handle security updates quickly.

Community
---------

The new NixOS website gets a wonderful `packages search page <http://nixos.org/nixos/packages.html>`_.

A call for help
---------------

This week's issue is quite short. My sources include watching the git
logs, the mailing list, and asking on IRC at the last minute. This
means there probably are many interesting things that I
missed. Therefore, if you are a NixOS contributor and do or see
something interesting, please send me an `email`_ or ping me on IRC
(I'm madjar) to make sure no good deed stays unpublished.
