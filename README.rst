====================
Rollsum Tests README
====================

Introduction
============

These are a bunch of experiments, and results on rolling hash
algorithms, trying variants and analysing how well they perform. This
was prompted by work on the `librsync
<https://github.com/librsync/librsync>`_ hashtable which identified
that the librsync rollsum had nasty clustering behaviour that required
adding a MurmurHash3 mix32() finalizer to get decent open addressing
hashtable performance. This suggested that the rollsum hash was far
from optimal.

Initially this was used to analyse librsync's adler32/fletcher based
rollsum and try variants to improve it. After that was exhausted, a
tiny bit of research found the `Wikipedia Rolling_hash
<https://en.wikipedia.org/wiki/Rolling_hash>`_ page that included
RabinKarp and CyclicPolynomial rolling hash algorithms. I added these
algorithms with similar variations as used for the rollsum for
comparison.

Contents
========

=============== ======================================================
Name            Description
=============== ======================================================
README.rst      This file.
RESULTS.rst     Discussion and analysis comparing different rollsums.
LICENSE         Copyright and licencing details.
rollsum.py      Script to test different rollsum algorithms.
run.sh          Script to run rollsum.py for many rollsum variants.
runtest.py      Script to compare rollsum variants.
cmphash.py      Script to compare rollsum, RabinKarp, and CyclicPoly.
lcg_inthash.py  LCG random number and primes functions.
data/csv.dat    File fragment of csv (ASCII) data for input.
data/zip.dat    File fragment of zip (random) data for input.
data/*.out      Output files from script runs.
=============== =======================================================

Credits
=======

Martin Pool <mbp@sourcefrog.net> for librsync.
Martin Nowak <code@dawg.eu> for pointing out how bad rollsum clusters
and how MurmurHash's mix32() can fix it.

Conditions
==========

See LICENSE for the copyright and licencing details.

Install
=======

There is nothing to install here, just scripts to run and data to use.

Usage
=====

For rollsum.py help run::

    $ ./rollsum.py -h

To run rollsum.py to get detailed stats for a RabinKarp rolling hash::

    $ ./rollsum.py -R rk -B 1K -C 1000000 --seed=1 --offs=0 \
    --mult=0x41c64e6d --map=ord --indexbits=20 <data/csv.dat

To run rollsum.py for a bunch of librsync rollsum variants and output
a summary::

    $ run.sh -B 1K -C 1000000 ./data

To generate comparisons of rollsum variants::

    $ runtest.py
    
To generate comparisons of rollsum, RabinKarp, and CyclicPoly hashes::

    $ cmptest.py

Support
=======

Documentation
-------------

http://minkirri.apana.org.au/wiki/LibrsyncRollsumAnalysis
  Some early analysis and observations.
  
http://github.com/dbaarda/rollsum-tests
  The project on github.

RESULTS.rst
  Detailed analysis and comparisons of different rolling hash
  algorithms and their variants.

Discussion
----------

For any questions send email to abo@minkirri.apana.org.au or use the
github issue tracker.

Reporting Problems
------------------

Report any problems on the github issue tracker.

Development
===========

These scripts are a bit ad-hoc and were heavily modified and tweaked
during various exploritory experiments. It is possible they still
contain fragments of dead or broken code from old experiments that
never got cleaned up.

Some result data provided may have been generated from older variants
of the scripts and do not reflect the current output. Not all the
result data that guided the experiments and contibuted to conclusions
is provided or was kept.

Design
======

Not so much designed, as evolved...


Plans
=====

The results of this analysis will probably be used to implement a
RabinKarp rollsum in future versions of librsync.

History
=======

Unfortunately the early development history was not checked into git.


----

http://project/url/README
$Id: README,v 69a01169087f 2014/11/27 00:12:55 abo $
