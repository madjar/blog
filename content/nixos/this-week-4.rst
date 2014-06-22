This Week couple of weeks in NixOS
==================================
:date: 2014-06-22 21:00
:slug: this-week-in-nixos-4

Welcome to a new issue of `This Week in NixOS`. Nix is a purely
functional package manager that aims at solving old problems with a
new approach, and NixOS is the distribution based on Nix. This is an
overview of what happened in the development of NixOS and in its
community this week. A lot of things happen in a lot of places and I
might miss some, so if you want to make sure that something is
mentionned in the next issue, send me an email_!

.. _email: mailto:georges.dubus@gmail.com?subject=This%20Week%20in%20NixOS%20Suggestion

Nix, the package manager
------------------------

Nix gets its usual share of fixes, but nothing groundbreaking, it seems.

Nixpkgs, the package compilation
--------------------------------

The last two weeks have been busy for nixpkgs. I only skipped a week,
and have 4 times as much commits as usual to review. That is good
news!

We have new versions of a lot of things, including `a new kernel
<https://github.com/NixOS/nixpkgs/commit/8bb2313915dcf5dff9cf2fcf5b0acaee6adf30bd>`_.

It is now possible to activate unfree packages `based on a predicate
<https://github.com/NixOS/nixpkgs/commit/a076a60735bb8598571978a40aab4d65be265c2f>`_,
which makes it possible to cherry-pick unfree packages.

A `stdenv update
<https://github.com/NixOS/nixpkgs/commit/1b78ca58bccd564350b52d00471399305e4eab23>`_
triggered a full rebuild. It included a gcc update, a pkgconfig
update, and the merge of the grsecurity branch. Changes to stdenv are
usually bundled together in order to reduce the number of rebuilds
necessary.

Security updates trigger massive rebuilds, and Hydra only update a
channel once the rebuild is over. Thus a security update can take a
few days to reach your machine. However, if you need the update right
now, you can replace runtime dependencies of the packages installed on
your system. `This is documented on the wiki
<https://nixos.org/wiki/Security_Updates>`_.


The community
-------------

Fonts on linux have always been a thing to configure. `A wiki page
<https://nixos.org/wiki/Fonts>`_ explains how to configure them in
NixOS. As for me, I still haven't found the right configuration (those
pesky Outlook emails still are ugly), but I'll keep searching!

Nix provides way to customize a package by changing parts of the
derivation, but only the default expression is built by Hydra and has
a binary package. The `mailing list discuss
<http://comments.gmane.org/gmane.linux.distributions.nixos/13274>`_ on
making Hydra build all the variants of a package.
