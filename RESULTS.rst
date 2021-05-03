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

RGear
-----

This is a widely used variant of Gear copied from
https://github.com/ronomon/deduplication uses a right-shift instead of a left
shift to ensure the least-significant-bits have the most entropy, and a
mapping table constrained to 31 bits for efficiency in javascript. This means
bytes don't fully "expire" from the hash, so it no longer only includes only
the last 32 bytes, and older bytes can modify the hash. In practice the
probability that older bytes modify the sum rapidly tends to zero the older
they are. The chance that a byte propagates a bit change into the 32 bit hash
is 1/2^(i-32) where "i" is the index back to the byte. This is equivalent to
the window size being probabalistic, with a less than 0.4% chance the window
is larger than 40 bytes.

UGear
-----

This is idential to Gear except the hash bits are shifted so that the tests
use the upper bits which include more entropy. This shows how much better Gear
is if you use the upper bits instead of the lower bits.

MGear
-----

This is a variant of UGear that adds a multiply operation to improve bit
mixing across the hash. It should improve the hash and reduce the requirement
for a mapping. It also copies UGears use of the upper bits. The update
algorithm becomes;

  H = (H << 1 + Cn) * 0x08104225

This is like a hybrid of Gear and RabinKarp with a simple 'mul' mapping. It
retains Gear's shift to expire out old bytes without needing to keep a rolling
window, while using RabinKarps multiply to mix the bits more effectively. It
also modifies the RabinKarp bit to apply the multiply after adding in the byte
which ensures the last byte added is mixed over the whole hash, which is
important because that last byte is a significant fraction of the entropy for
small windows.

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

In particular ASCII data tends to be tightly clustered around a small range of
values, which produces very small variance in sums of those values. For
Rollsum with small blocksizes, the s1 sum of bytes ends up tightly clustered
in a small part of the s1 part of the hashspace.

Mappings can use lookup tables, which is the traditional solution that nearly
always benchmarks fastest in isolation. However, lookup tables eat CPU cache,
and a 256x32bit mapping table uses 1K, which can be a significant portion of a
low end CPU's 32K L1 cache. In the wider context of a program doing many
things that could use that L1 cache, simple mapping algorithms can be faster
and give hash results nearly as good. Hence the desire to avoid the need for
mappings or find fast-and-good-enough mapping algorithms.

Mapping can be used to both distribute clustered input bytes more evenly over
the 8bit byte-range, or distribute them over more than 8bits if the algorithm
can use it.

The mappings provided are "ord" (just use the byte value), "pow" (square the
value into 16bits), "mul" (multiply the values by 0x08104225 into 32bits),
"mix" (mix into 32bits from MurmurHash3) and ipfs (lookup into 32bits used by
IPFS chunker). Note for Rollsum we only use the lower 16 bits.

Note xdelta uses a byte-> 16bit mapping that is equivalant to using 16 bits of
mix. CyclicPoly and Gear recommends using a byte->32bit mapping like mix or
ipfs.

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

RabinKarp without a mapping doesn't mix the last byte into all the hash bits.
For very small rolling windows as used in chunking algorithms, the last byte
can be a significant portion of the entropy. Changing the algorithm to add the
byte before doing the multiply fixes this. This is equivalent to using the simple
"mul" mapping, but can be more cheaply implemented by adjusting the algorithm.

Measuring Performance
=====================

Hash Performance
----------------

For testing the general hash performance a range of block sizes are used
to test how the hash performs against block size. Performance is measured by
checking for collisions and clustering.

Collisions are when different data blocks produce the same hash.
Clustering is when many different data blocks produce hash values
unevenly distributed across the hash space. Both are bad for hashtable
performance, particularly Open Addressing hashtables, which degenerate
badly for clustering.

Bad clustering with OK collision behaviour can be compensated for
using something like MurmurHash3's mix32 finalizer function to
distribute the clustered values evenly across the hash space.

An ideal hash has an independently even chance of producing any hash value in
the hash range for any entry. If you divide the hash range evenly over a
subrange of buckets, there should be an even chance of producing a hash value
in any bucket. Under these ideal conditions the number of entries per hash
value or bucket should match a `Binomial distribution
<https://en.wikipedia.org/wiki/Binomial_distribution>`_, which tends towards a
`Poisson distribution <http://en.wikipedia.org/wiki/Poisson_distribution>`_
as the number of buckets gets large.

The variance of the number of entries per hash value or bucket can be
used to measure how evenly the hashes are spread. The larger the
variance, the more buckets there are with way more or less than the
mean, and hence are less evenly distributed.

Poisson distributions have the interesting property that the variance is equal
to the mean. This means we can use (mean / variance) as a measure of how good
a hash function is, where small values near zero are bad, and 1.0 is ideal.
Any values > 1.0 are probably statistical noise. To be slightly more accurate
we can use the expected binomial variance over the measured variance, which is
((size-1)/size * mean/variance), where size is the number of buckets.

Dividing the hash space into 2^N buckets is tested using "and_mask" (AndMask
described above), "mod_mask" (ModMask described above) or "mix_mask" (mix32()
and then ModMask). The (mean / variance) bucket size for these give an
indication of the hashtable collision rate for the hash using those bucketing
methods. Note this effectively tests the entropy in the bottom N bits, and the
overall hash collision rate/entropy is tested using 2^32 buckets.

Finally hashtable clustering is tested as "and_clust", "mod_clust", and
"mix_clust" for the 3 bucketing methods merging 16 adjacent buckets into a
"bucket-cluster". The (mean / variance) of the bucket-cluster sizes shows how
badly the hash clusters for those bucketing methods. Note this effectively
tests the entropy in the 4th to Nth bit of the hash.

Since we care about both collisions and clustering, a single "score" is
calculated using a `Weighted Geometric Mean
<https://en.wikipedia.org/wiki/Weighted_geometric_mean>`_. They are weighted
by ``log(1/sqrt(2/size))`` where size is the number of buckets. This weighting
is based on the `confidence interval for the measured variance
<https://en.wikipedia.org/wiki/Normal_distribution#Confidence_intervals>`_
based on the number of buckets. It is roughly proportional to the number of
significant digits in the score. This ensures a low score for either
collisions or clustering drags the score down more than an arithmetic mean
would, while still weighting the collisions about 2x as high as the
clustering.

Chunking performance
--------------------

For measuring chunking performance small windows of 32 and 16 bytes are used.
The 32 byte size is commonly used for chunking algorithms and is the effective
window size of Gear. The smaller 16 byte window is the minimum window size to
give about 16 bits of entropy from highly redundant ASCII data, which is just
enough for target chunk sizes upto 64K.

In practice, Gear always has a window size of 32, and RGear has a variable
window size of at least 32. When doing the test with window sizes smaller than
the rollsum's effective window size, it means the rolling hash can include
earlier bytes not included in the test window data. This means identical test
window data can have different rolling hash values. This messes a bit with
analysis, since identical windows can appear multiple times in different
rolling hash buckets. In practice it's not too bad, and we only treat
identical window data as identical if it also lands in the same rolling hash
bucket. The main artifact is test runs over the same data can end up with
different test-window counts for different rollsum algorithms due to the
different duplicate detection.

Gear based algorithms also include less and less entropy from the older bytes,
so even though their effective windows are 32 bytes (or more for RGear), in
practice they only really include about 16 bytes of entropy. So testing using
a smaller 16 byte window gives a better indication of how good the rollsum is
at representing/hashing the the last 16 byte window.

Comparisons
===========

See the `cmphash.py output table <./data/cmphash.rst>`_ for the raw
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

Interesting is the ASCII collisions are much better for very small 16 and 32
byte blocks, almost certainly because the way the rotate/or operations
distribute the bits means you don't have repeated bytes at multiples of 32
offsets canceling each other out. This means its probably fine for chunking
operations where buzzhash is often used.

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
clustering. It works fine without mappings for large windows.

For tiny 16 byte chunking windows the 'mul' mapping is noticably better than
no mapping for clustering. This is also visible to a lesser degree for 32 byte
windows. This is because the 'mul' mapping ensures the last byte is mixed
over the whole hash, and for small windows the last byte is a significant part
of the entropy. This means a modified RabinKarp that adds the next byte before
the multiply would be better for chunking applications.

Gear
----

Gear can only be used on 32 byte windows, and even then the oldest bytes are
only represented in the MSBits of the sum. The way the data from old bytes
gets slowly shifted out means that even though it effectively has a window
size of 32 bytes, the hash doesn't include all the entropy in all those bytes,
and probably only includes about 16 bytes worth. Highly redundant ASCII data
has about 1 bit of entropy per byte, and the mapping distributes that entropy
over the full 32bits with it concentrating into the upper bits. This means
only the most significant 16 bits are really useful, so it's not going to be
great for a chunker with a target chunk size greater than 64K.

For 32 byte windows the collisions and clustering are fine for random data,
but really terrible for ASCII data. This is because it doesn't include all the
entropy of the older bytes in that 32 byte window, resulting in lots of
collisions and clustering. Also the clustering test uses the lower 20bits of
the hash, while Gear has best entropy in the upper bits. Using a decent
mapping doesn't seem to help, probably because there is so little entropy it
doesn't matter how you mix it into the hash. It probably helps a bit to
distribute the upper bits which are not checked by the collision test.

Using a 16 byte window the collisions is much better provided you have a good
mapping, showing that Gear really only has about the last 16 bytes worth of
entropy for ASCII data. The collisions are still worse than RabinKarp, but
it's not terribly worse. The clustering is still terrible because it's still
testing the wrong bits.

This poor collision and clustering performance probably doesn't matter much
for most chunking algorithms which only check when select bits of the hash
have a particular value, but you need to use the higher bits, and ensure the
value chosen is not a degenerate case with disproportionately high or low
occurances.

RGear
-----

This significantly improves clustering compared to Gear because the entropy is
in the least-significant bits used by the clustering test. It also potentially
includes some entropy from bytes before the 32 bytes. In every other respect
it seems about the same as Gear, maybe a tiny bit worse for collisions,
possibly due to only using 31 bit mappings.

UGear
-----

This shows that using Gear's upper bits gives you much better clustering
performance. For 16 bytes ASCII data it makes the clustering nearly as good as
RabinKarp with the 'mul' mapping, but still not as good on collisions. It's
maybe slightly better than RGear for collisions and clustering with the 32bit
mapping.

MGear
-----

This performs as well as UGear without requiring a lookup table.

Summary
=======

Hashing
-------

Rsync style algorithms use the rollsum as a sliding window hash of a whole
block in the size range of around 1K~64K, and is used for a hashtable lookup.
For this application the hash quality for whole blocks of data matters, with
poor collisions and clustering resulting in degraded hashtable performance.

Rollsum without "pow" squaring is terrible for anything less than
random 16K blocks. Adding squaring it becomes OK for collisions, but
still has terrible clustering for ASCII for even 16K blocks, so needs
a mix32 finalizer when using it for a hashtable.

CyclicPoly has the worst collisions for ASCII data, so is not worth
considering.

RabinKarp has excellent collision and clustering performance for all data
types and block sizes, without needing a mapping table. The good clustering
means it can be used without a mix32 finalizer. This is the algorithm to use
for new applications

Chunking
--------

Chunking algorithms use the rollsum as a hash of only a tiny sliding window of
about 16~48 bytes and use about N bits of the hash for a target chunk size of
2^N bytes. So only N bits of the hash matter, and the consequence of poor
collisions and clustering would only be a different chunk-size distribution
from what is expected/desired. So speed matters more than hash quality, and
the hash quality only matters for part of the hash.

Rollsum is just terrible for windows this small, and is not worth using. A
decent mapping can help reduce collisions, but its clustering is always
terrible.

Gear is an efficient and OK algorithm for chunkers, with the nice property
that it doesn't need to keep a sliding window. However, it requires a mapping
table and has really bad collisions and clustering on ASCII data, with an
effective window size of only about 16 bytes and only the upper 16 bits are
useful (as shown by "UGear"). Always use a good mapping table, use the upper
bits of the hash, and ensure the value compared against is not a degenerate
case. It might give poor chunk distributions for ASCII data with windows
larger than 64K.

RGear performs like Gear except the bottom bits are the best bits to use.
However, it is a bit worse than Gear using the upper bits, so it's not worth
using unless you really want to use the lower bits and/or have a 31 bit
integer requirement.

MGear performs as well as Gear but doesn't require a mapping table, using a
multiply instead.

CyclicPolly (AKA BuzzHash) needs to keep the sliding window and requires a
mapping table, but peforms really well for windows up to 32 bytes, with
excellent collisions and clustering across all the hash bits. However, it is a
bit more vulnerable to degenerate cases and for windows larger than 32 bytes
and ASCII it starts to suffer a bit from the collisions cases we see under the
hash tests.

RabinKarp with a "mul" mixer, modified to do the multiply after adding the
byte, does require the sliding window but doesn't require a mapping table. It
performs as well as CyclicPolly on collisions and clustering for any window
size across all the hash bits. It doesn't have CyclicPollys vulnerability to
degenerate cases and larger windows.

For new applications, Gear with a good mapping and using the upper bits will
be fast, doesn't need to keep the sliding window, and will be good enough for
chunk sizes upto 64K. If your application is thrashing L1 cache, MGear will be
just as good and faster because it removes the mapping table. Its small
effective window size of only 16 bytes and about 16 effective bits does mean
it's operating at the bare minimum required though, so it's possible you'd see
degenerate cases with poor chunk distribution in some applications.

If you need to retain the sliding window data anyway and want a better hash
with more effective bits and/or a larger window, a modified RabinKarp with
'mul' mixer is probably best. It doesn't require a mapping table and gives a
good hash for any type of data and any window size.

For existing applications BuzzHash is fine. It is about as good as the
modified RabinKarp but requires a mapping table.
