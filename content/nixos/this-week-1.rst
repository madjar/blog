This Week in NixOS, first issue
===============================
:date: 2014-05-25 21:00
:slug: this-week-in-nixos-1

Welcome to the first issue of `This Week in NixOS`. Nix is a purely
functional package manager that aims at solving old problems with a
new approach, and NixOS is the distribution based on Nix. This is an
overview of what happened in the development of NixOS and in its
community this week. If you want something mentioned in the next issue,
send me an email_ !

.. _email: mailto:georges.dubus@gmail.com?subject=This%20Week%20in%20NixOS%20Suggestion

This is the first issue, and I'm still trying to find the right
formula for this weekly overview. Any comment welcome!

Nix itself
----------

``nix-store --read-log`` `gets the ability to download the build
logs <https://github.com/NixOS/nix/commit/9f9080e2c019f188ba679a7a89284d7eaf629710>`_
from the build servers if they aren't available locally. For those,
like me, who didn't know the ``--read-log`` option, it prints the
build log of a given derivation. Since the builds are deterministic,
the build logs are always the same whether the build occurred locally
or on another machine.

Nixpkgs
-------

Nixpkgs received its usual stream of package updates, the most
noticeable probably being `Gnome 3.12
<https://github.com/NixOS/nixpkgs/pull/2694>`_.

Updates also include but are not limited to `the linux kernel
<https://github.com/NixOS/nixpkgs/commit/2ee6c0c63e381c2afb3540261a353a7094fcf659>`_,
`firefox
<https://github.com/NixOS/nixpkgs/commit/8b89cba9c6c747ad10afc831dd03ed2af487a794>`_,
and a lot of haskell packages.

NixOS
-----

- Many updates to ``nixos-install`` and to the install ISO (`here is
  one of the 12 commits
  <https://github.com/NixOS/nixpkgs/commit/1e2291f23ae2f51615353610db0482f464a7a77e>`_).
- `Better support EC2 HVM instances
  <https://github.com/NixOS/nixpkgs/commit/973fa21b52d0222ea5033ef265b2fbc0d2ab85c2>`_.

Mailing list
------------

Many questions and discussions this week, including discussion about a
`restructuring of the wiki
<http://thread.gmane.org/gmane.linux.distributions.nixos/13034>`_.

..  LocalWords:  NixOS Nixpkgs
