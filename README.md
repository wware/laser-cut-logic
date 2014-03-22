Laser-cut Logic
==

This project is an initial step toward a toy to implement and teach simple
Boolean logic, in the spirit of the Digi-Comp I from the 1960s, using laser-cut
pieces of plywood or acrylic, a little glue, and maybe a few inexpensive items
from the local hardware store. The design shouuld be easily modifiable and
customizable. The diagram (sketch.jpg) is a hand-drawn preliminary design for
the toy.

The shapes will be specified in Python, written to generate
[Postscript](http://www-cdf.fnal.gov/offline/PostScript/BLUEBOOK.PDF) files
that can be run on laser cutters such as those at danger!awesome in Cambridge,
Massachusetts.

I'll want to provide a simple set of minimal instructions for people who just
want to build the design as given: where and how to shop for materials, where
to find a laser cutting shop, how to assemble the pieces once you have them,
how to operate the thing and set up logic problems on it.

Future
--

The Digi-Comp could implement a very wide variety of 3-bit finite state
machines. It could count and work a variety of simple puzzles and games.

In order to reach the same level, I need not just the simple logic gates in
this first version, but full flip-flops that retain state across clock edges.
So there is more design work to do in order to make that happen.

Ultimately I'd like to be able to produce teeny metal logic machines that could
be built using Shapeways or Ponoko or similar services, and be able to program
them using some little compiler that figures out where the pegs go, and
possibly creates permanent pegs rather than replaceable pegs, for when the
logic function can remain fixed.
