Algorithms
==========

Rollsum
-------

This is the rollsum algorithm used by rsync and librsync. It is a
variant of Adler32, with some similarities to Fletcher. It uses 16bit
s1 sum and s2 sum-of-sums concatenated into a 32bit sum.

RabinKarp
---------

This is a rollsum using multiplies and adds as used in the `RabinKarp string
searching <https://en.wikipedia.org/wiki/Rabin%E2%80%93Karp_algorithm>`_
algorithm. This is NOT the same as Rabin-fingerprint, which uses more
expensive (in software, but easier in dedicated silicon) GF(2) operations that
require table lookups instead of adds/mults. Also known as Polynomial Hash.

CyclicPoly
----------

This is similar to RabinKarp, but uses rotate-left and xor operations
instead of multiplies and adds. This is also known as buzzhash, and used by
IPFS for its content based chunking.

Gear
----

This is a special rollsum that can only be used for chunking. It doesn't
explicitly use a sliding window, but instead incrementally expires older input
data by slowly shifting it left out of the sum. This means it only includes as
many input bytes as there are bits in the checksum (usually 32bits), so it
only gives you a hash of the last 32 bytes. It requires input bytes to be
mapped to a full hash width to ensure the latest byte added has its entropy
spread over the entire hash. The older bytes have the entropy slowly removed
from the LSBits of the hash, with only MSBits including entropy from the older
bytes.

Variations
==========

Initializers and Offsets
------------------------

Rollsum can use an initial seed or character offset to ensure that
zero blocks of different sizes have different hashes. Either approach
for a fixed blocksize is equivalent to adding fixed values to s1 and
s2, so have zero effect on the hash collision or clustering
performance.

Pure RabinKarp and CyclicPoly both give zero hash values for zero
blocks of any size. They would need to be modified with either a
initial seed or character offset to ensure they give different hashes
for zero blocks of different sizes.

The RabinKarp roll calc for both offs and seed looks like this;

rollin:
  H = K*H + Cn + offs
rollout:
  H = H - K^(n-1)*C0 - K^(n-1)*offs - K^(n-1)*(K - 1)*seed
  H = H - K^(n-1)*(C0 + offs + (K - 1)*seed)
rotate:
  H = K*H + Cn - K^n*C0  - (K^n - 1)*offs - K^n*(K - 1)*seed
  H = K*H + Cn + offs - K^n*(C0 + offs + (K - 1)*seed)

Not that the offs and seed adjustments can be pre-calculated and
reduced to just one addition for an seed, or 2 additions for an offs.

Both offs and seed equate to a value added to the hash that is a
function of the blocklength, and should behave exactly the same.

Adding an initial seed or offset character to CyclicPoly can be done
in a similar way with a similar effect.

Librsync's Rollsum uses offs=31 and Adler32 uses seed=1. Tests
indicate that there is no difference between using offs and seed, but
seed is a tiny bit faster.

AndMask vs ModMask vs ModPrime
---------------------------------

Any intermediate hash calculations that produce values with more bits
than are needed must be pruned down to the required number of bits.
Note CyclicPoly doesn't need this since it's rotate-left and xor
operations don't produce more bits.

If we need N bits, we can "and" against a bitmask of (2^N-1) to keep
only the lowest N bits. This throws away any information in the higher
bits. This is what Rollsum and RabinKarp uses.

To keep information in the higher bits we can instead "mod" against the
bitmask. This is equivalent to using 1's compliment arithmetic, and
effectively "end-over-carry"s the discarded high bits into the lower
bits. It sacrifices one value (2^N-1) in the the hash-space, but can
result in better hashes. This is what Fletcher uses.

Another option is to "mod" against the largest prime in the 2^N value
range. This sacrifices more values in the hash-space, but is more
likely to avoid degenerate alignment problems caused by common prime
factors in the data and hash algorithm. It also effectively mixes
information in the discarded higher bits into the lower bits to give a
better hash distribution. In practice the sacrificed hash-space values
appears to be more of a loss than the improved hash distribution. This
is what Adler32 uses.

For Rollsum we experimented with all three methods for maintaining the
16bit s1 and s2 sums, using a --base value to 'mod' against. A
base of 0x10000 is "and_mask", 0xffff is "mod_mask", and 0xfff1 is
'mod_prime".

Character mapping
-----------------

This is mapping the input byte values to different values before
feeding them into the algorithm. This can distribute the input data
better before feeding it to the hash algorithm, possibly producing a
better hash distribution.

In particular ASCII data tends to be tightly clustered around a small
range of values, which produces very variance in sums of those values.
For Rollsum with small blocksizes, the s1 sum of bytes ends up tightly
clustered in a small part of the s1 part of the hashspace.

It can be used to both distribute clustered input bytes more evenly
over the 8bit byte-range, or distribute them over more than 8bits if
the algorithm can use it.

The mappings provided are "ord" (just use the byte value), "pow" (square the
value into 16bits), "mul" (multiply the values by 0x08104225 into 32bits),
"mix" (mix into 32bits from MurmurHash3) and ipfs (lookup into 32bits used by
IPFS chunker). Note for Rollsum we only use the lower 16 bits.

Note xdelta uses a byte-> 16bit mapping that is equivalant to using 16 bits of
mix. CyclicPoly recommends using a byte->32bit mapping like mix or ipfs.

Note that character offsets could also have been implemented using a
mapping function. However, it was not done this way because the
algorithms can more efficiently take into account the offset.

Algorithm Specific
------------------

RabinKarp has a 32bit constant multiplier and doesn't specify a
particular value. It recommends the same kinds of values are are used
for LCG random number generators, which have several requirements.
We've tried 0x41c64e6d (Recommended LCG value), 0x01010101 (sparse bit
pattern), 55555555 (balanced bit pattern), 0xfffffffd (dense bit
pattern) 0x8104225 (varying bit pattern).

Measuring Performance
=====================

Collisions are when different data blocks produce the same hash.
Clustering is when many different data blocks produce hash values
unevenly distributed across the hash space. Both are bad for hashtable
performance, particularly Open Addressing hashtables, which degenerate
badly for clustering.

Bad clustering with OK collision behaviour can be compensated for
using something like MurmurHash3's mix32 finalizer function to
distribute the clustered values evenly across the hash space.

An ideal hash has an independently even chance of producing any hash
value in the hash range for any entry. If you divide the hash range
evenly over a subrange of buckets, there should be an even chance of
producing a hash value in any bucket. Under these ideal conditions the
number of entries per hash value or bucket should match a `Poisson
distribution <http://en.wikipedia.org/wiki/Poisson_distribution>`_
(from the definition of a Poisson distribution).

The variance of the number of entries per hash value or bucket can be
used to measure how evenly the hashes are spread. The larger the
variance, the more buckets there are with way more or less than the
mean, and hence are less evenly distributed.

Poisson distributions have the interesting property that the variance
is equal to the mean. This means we can use (mean / variance) as a
measure of how good a hash function is, where small values near zero
are bad, and 1.0 is ideal. Any values > 1.0 are probably statistical
noise.

Looking at the (mean / variance) of the number of entries per hash
value gives us an indication of how close to ideal a hash is for
collisions.

Dividing the hash space into 2^N buckets is tested using "and_mask"
(AndMask described above), "mod_mask" (ModMask described above) or
"mix_mask" (mix32() and then ModMask). The (mean / variance) bucket
size for these give an indication of the hashtable collision rate for
the hash using those bucketing methods.

Finally hashtable clustering is tested as "and_clust", "mod_clust",
and "mix_clust" for the 3 bucketing methods merging 16 adjacent
buckets into a "bucket-cluster". The (mean / variance) of the
bucket-cluster sizes shows how badly the hash clusters for those
bucketing methods.

Since we care about both collisions and clustering, a single "score" is
calculated using a `Geometric Mean
<https://en.wikipedia.org/wiki/Geometric_mean>`_ so a low score for either
collisions or clustering drags the score down more than an arithmetic mean
would.

Comparisons
===========

See the `cmphash.py output table `<./data/cmphash.rst>`_ for the raw
results.

RollSum
-------

Rollsum is pretty terrible from a collisions and particularly
clustering point of view. It's much worse for ASCII and blocksizes
smaller than 16K. Changing to squaring the input bytes helps
significantly, which starts to make it competitive on collisions for
even ASCII 1K blocks, but it is still bad for clustering ASCII up to
64K blocks, with OK clustering for random 1K blocks. Without squaring
it only begins to be competitive in collisions for random 16K blocks,
and for clustering it is still bad for random 64K blocks.

Offset vs seed makes no difference, but seed is faster.

AndMask vs ModMask vs ModPrime for the hash algorithm makes minimal
difference. Using ModMask helps a little, but in practice the s1 sum
for small ASCII blocks gives a tight bell-curve custered distribution
that doesn't even overflow out of 16bits. ModPrime discards too much
of the hash space.

Character mapping using "mul" makes little difference at all because
for a fixed block size it behaves like constant multipliers for s1 and
s2, which does nothing for the collisions and little for the
clustering. Using "pow" makes a significant difference.

For bucketing, and_mask gives terrible clustering and collisions
because it discards bits from the s2 sum which is better distributed
than s1. Using mod_mask doesn't help much, because the poor
distribution is in the high bits of s1 which are in the middle of the
hash, and ModMask mixes the discarded high bits into the low bits,
leaving the middle bits largely untouched. Using mix_mask solves the
clustering, but cannot fix the collisions.

CyclicPoly
----------

CyclicPoly (Buzzhash) has near optimal clustering regardless of data type or
blocksizes. It also has near-optimal collisions for random data. However, it
has the worst collisions for ASCII data. The only thing worse on collisions
for ASCII is Rollsum without squaring for <4K blocksizes. Character mapping to
expand the bytes across the full 32bit sum makes a big difference for very
small 32 byte blocks, but has less impact for large blocks.

Interesting is the ASCII collisions are much better for very small 32 byte
blocks, almost certainly because the way the rotate/or operations distribute
the bits means you don't have repeated bytes at multiples of 32 offsets
canceling each other out. This means its probably fine for chunking operations
where buzzhash is often used.

The rotate/xor operations used don't overflow changes up to adjacent bits like
add/mult does, so it's much more vulnerable to degenerate data patterns. In
particular, any bytes that repeat a multiple of 32 bytes apart will cancel
each other out of the sum.

Another interesting degenerate case for chunkers using 32 byte rolling windows
is runs of 32 identical bytes will either hash to all 0's or all 1's depending
on if your character mapping has an even or odd number of 1's for that
character. This is because every bit in the hash becomes an xor of every bit
in the mapped value. The ipfs mapping tries to ensure each character map value
has evenly distributed bits, resulting in most characters having even number
of 1's and thus hashing 32 byte runs of any character to 0. This can result in
chunkers being "accidentally context aware" and putting chunk boundaries at
the zero-padding runs between files inside tar archives, giving better
deduplication than would normally be expected.

RabinKarp
---------

RabinKarp has near optimal clustering and collision performance
regardles of blocksizes or data type. It's only for random 16K blocks
that CyclicPoly and Rollsum with squaring start to just (in the noise)
match it on collisions while still just trailing it (in the noise) on
clustering.

Gear
----

Gear can only be used on 32byte blocksizes, and even then the oldest bytes are
only represented in the MSBits of the sum. The collisions and clustering are
fine for random data, but really terrible for ASCII data, so bad it's a bit
hard to understand why. It's worth noting that the clustering test uses the
lower 20bits of the hash, while Gear has best entropy in the upper bits, but
the bad collisions suggests the upper bits are not particularly well
distributed either. The mapping doesn't seem to help much, but again it
probably helps to distribute the upper bits which are not checked by the
collision test.

The way the data from old bytes gets slowly shifted out means that even though
it effectively has a block size of 32 bytes, the hash doesn't include all the
entropy in all those bytes, and probably only includes about 16 bytes worth.
Assuming each input byte has 1 bit of entropy, and the mapping distributes
that entropy over the full 32bits, only the most significant 16 bits are
useful. This means it's not going to be great for a chunker with a target
chunk size greater than 64K.

This poor collision and clustering performance probably doesn't matter much
for most chunking algorithms which only check when select bits of the hash
have a particular value, but you need to use the higher bits, and ensure the
value chosen is not a degenerate case with disproportionately high or low
occurances.

Summary
-------

Rollsum without "pow" squaring is terrible for anything less than
random 16K blocks. Adding squaring it becomes OK for collisions, but
still has terrible clustering for ASCII for even 16K blocks, so needs
a mix32 finalizer when using it for a hashtable.

CyclicPoly the worst collisions for ASCII data, so is not worth
considering.

RabinKarp has excellent collision and clustering performance for all
data types and block sizes. The good clustering means it can be used
without a mix32 finalizer.

Gear is an efficient and OK algorithm for chunkers, but has really bad
collisions and clustering on ASCII data, with only the upper 16 bits being
useful. Always use the upper bits of the hash and ensure the value compared
against is not a degenerate case.
