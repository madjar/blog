This Week in NixOS, second issue
================================
:date: 2014-06-01 21:00
:slug: this-week-in-nixos-2

Welcome to the second issue of `This Week in NixOS`. Nix is a purely
functional package manager that aims at solving old problems with a
new approach, and NixOS is the distribution based on Nix. This is an
overview of what happened in the development of NixOS and in its
community this week. A lot of things happen in a lot of places and I
might miss some, so if you want to make sure that something is
mentionned in the next issue, send me an email_!

.. _email: mailto:georges.dubus@gmail.com?subject=This%20Week%20in%20NixOS%20Suggestion

Nix itself
----------

``scopedImport`` `was introduced in Nix
<https://github.com/NixOS/nix/commit/c273c15cb13bb86420dda1e5341a4e19517532b5>`_. It
enables the definition of package expressions without having to list
the dependencies again as function arguments (which is the case for
every packages as of now), making the writing of package expressions
(even) simpler. It isn't used in nixpkgs yet, but I guess we will see
a big commit removing all argument definitions at some point.



Nixpkgs
-------

As usual, a lot of packages updates, though I don't think I have seen
anything huge. I plan on writing some tools to generate an exhaustive
list of updates for this section (and at some point, for your
``nixos-rebuild`` and ``nix-env -u``).

Darwin support has been greatly improved, with `several
<https://github.com/NixOS/nixpkgs/commit/b09a788e13712f694f12ea1d0fdbf630395effd2>`_
`major
<https://github.com/NixOS/nixpkgs/commit/0369769bd9843c7ddaab1f9ba77732337abfaee2>`_
`bug
<https://github.com/NixOS/nixpkgs/commit/2e2f42f21509b72e337b456c4986b8ea08a11e18>`_
fixes.

A lot of progress in the new `pypi2nix
<https://github.com/NixOS/nixpkgs/pull/1903>`_. I don't think
we'll have to wait too long for this new, shiny way to generate nix
expressions from python packages.

Community
---------

NixOS now has a new `website <http://nixos.org/>`_. While the old
website presented all Nix related projects (nix, nixos, hydra, disnix,
etc) on an equal footing, the new website focuses on NixOS to give an
immediate overview of its advantages and the dynamism of its
community. The new website a lot of `feedback and constructive
criticism
<http://comments.gmane.org/gmane.linux.distributions.nixos/13148>`_ on
the mailing list.

Joachim Schiele presented the `first preview
<http://blog.lastlog.de/posts/nix-build-view_using_ncurses/>`_ of
``nix-build-view``, a graphical frontend for nix-build, to visualize
parallel execution of downloads and builds. This first preview does
not actually display nix build execution: it aims at generating
discussion about what a good tool should be before actually find how
to integrate with nix. The goal is to create NixOS tools that have the
same level of quality as Gentoo tools. This is something I have in
mind for some time, so I'll keep a close eye on the initiative.
