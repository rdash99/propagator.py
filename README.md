## Fork Notes
- Depends on greenlet (pip install greenlet)
- Some depedancies were broken in the original fork, updated import statements

propagator.py
=============

#Propagator.py

**propagator.py** is a *propagator network* built with Python.

It is based on (or, should I say, translated from) the [Art of the Propagator][art],
a paper written by Alexey Radul and Gerald Sussman. There's a presentation
by Sussman called [We Really Don't Know How To Compute!][we-really-dont-know]
in which he explains the concepts and some applications wonderfully.

They wrote a complete propagator network and examples in MIT Scheme. I will
try to build a library that encompasses all the original features, together
with the examples.

My intentions translating it to Python are:

- Understanding how these propagators work -- I can make sense of Scheme
  functions (the trees), but it's more difficult to grasp the program as a
  whole (the forest).

- Making propagators available to a wider audience.

[art]: http://dspace.mit.edu/handle/1721.1/4421
[we-really-dont-know]: http://www.infoq.com/presentations/We-Really-Dont-Know-How-To-Compute


## Translation notes

### Overlap anomaly

In the section "6.1 Dependencies for Provenance", the system as it is coded
has a problem called "the overlap anomaly", in which a premise is included
in the justifications of a conclusion even though it is not really needed.

This anomaly does not occur in my translated examples, and I really don't
know why.
