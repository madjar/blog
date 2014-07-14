This last few weeks in NixOS
============================
:date: 2014-07-14 17:30
:slug: this-week-in-nixos-5


Welcome to a new issue of `This Week in NixOS`. Nix is a purely
functional package manager that aims at solving old problems with a
new approach, and NixOS is the distribution based on Nix. This is an
overview of what happened in the development of NixOS and in its
community this week. A lot of things happen in a lot of places and I
might miss some, so if you want to make sure that something is
mentionned in the next issue, send me an email_!

.. _email: mailto:georges.dubus@gmail.com?subject=This%20Week%20in%20NixOS%20Suggestion

Nixpkgs, the package compilation
--------------------------------

As usually, a ton of changes happened in Nixpkgs. I'll cite the new
expression `firefox-bin` for the binary distribution of Firefox, which
fixed a strange session problem I had with the source version of
Firefox 30.

The more time I spend trying to follow the changes in Nixpkgs, the
more I realize how much we need tools to seen what's happening in
NixOS. I hope I can discuss this with the fellow NixOS users I meet at
the EuroPython next week.

Alexander Kjeldaas has worked on `binary determinism
<https://github.com/NixOS/nixpkgs/pull/2281>`_ in Nixpkgs. The goal of
binary determinism is that the output of package build is always the
same, bit for bit. This is not the case currently: there are many
things that can result in a different binary. For example, many
programs include the build time in the resulting binary. One of main
advantage is security: since anybody can get the exact same binary
package, anybody can verify that the NixOS binary cache serves the
right binaries, without any backdoor added. Thanks to Austin Seipp for
explaining this to me. You can check `his explaination
<https://gist.github.com/madjar/545e1a9b6a8f9b7faeb8>`_ for more
details.

A `staging branch has been added to the git repository
<http://thread.gmane.org/gmane.linux.distributions.nixos/13447>`_. Changes
that cause massive rebuilds/redownloads are to be merge into staging,
and staging will be merge into master every few weeks. That way, Hydra
can start all the rebuilds while still building the master channel,
which should avoid the channel freezes caused by Hydra rebuilding the
world before updating the channel.


The community
-------------

On twitter, `@NixOsTips <https://twitter.com/NixOsTips>`_ tweets
useful tips about using Nix and NixOS usage, which can be difficult to
discover in the docs or the wiki. They also tweet articles about
NixOS, and end up being one of the sources of this newsletter.

On the mailing list, a discussion about the `rebuild impact factor
<http://thread.gmane.org/gmane.linux.distributions.nixos/13432>`_ and
how to compute it, a thread about `the use of ruby gems in NixOS
<http://thread.gmane.org/gmane.linux.distributions.nixos/13381>`_
(it's not pretty for now, and needs some love from someone how knows
ruby packaging well enough), and a `nice trick to avoid needless
copying when using nix-shell
<http://thread.gmane.org/gmane.linux.distributions.nixos/13458/focus=13460>`_.

NixOS is recieving a lot of attention recently, especially from
Haskell developpers: a `couple
<http://fuuzetsu.co.uk/blog/posts/2014-06-28-My-experience-with-NixOS.html>`_
`of
<http://www.pavelkogan.com/2014/07/09/haskell-development-with-nix/>`_
people give feedback on their experience with Nix for development, and
it's quite positive, with some useful criticism.
