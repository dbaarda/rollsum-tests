#!/usr/bin/python
import md5
from lcg_inthash import modinv

class BaseHash(object):
  """Base class for rolling checksums."""

  def __init__(self, data=None, seed=0, offs=0, map=ord):
    """Initialize a base rollsum calculator.

    Args:
      data: optional str input data to update with.
      seed: initial hash value to use.
      offs: offset to add to each input byte.
      map: optional mapping function to transform input bytes.
    """
    self.seed, self.offs, self.map = seed, offs, map
    self.mask = (1 << 32) - 1
    self.count, self.sum = 0, seed
    if data:
      self.update(data)

  def digest(self):
    return self.sum


class RollSum(BaseHash):
  """Rsync rollsum rolling checksum."""

  def __init__(self, data=None, seed=0, offs=31, map=ord, base=2**16):
    """Initialize a rollsum calculator.

    Args:
      data: optional str input data to update with.
      seed: optional value to initialize sum with.
      offs: optional offset to add to each byte.
      map: optional mapping function to transform input bytes.
      base: optional base to mod sum and sum2 with.
    """
    self.base, self.sum2 = base, 0
    # Find the max updates without doing mod where sum2 doesn't overflow.
    # Largest n such that n*(n+1)/2*(cmax+offs)+(n+1)*(base-1) <= 2^32-1.
    # Where cmax is the largest possible map(c) value.
    # Solving using (-b + sqrt(b^2 - 4*a*c)) / (2*a).
    cmax = max(map(chr(c)) for c in range(256))
    a = (cmax + offs)/2.0
    b = a + (base-1)
    c = (base-1) - (2**32 - 1)
    self._nmax = int((-b + (b**2 - 4*a*c)**0.5) / (2*a))
    super(RollSum, self).__init__(data, seed, offs, map)

  def __str__(self):
    return 'RollSum(seed=%s, offs=%s, map=%s, base=%#x)' % (
        self.seed, self.offs, self.map.__name__, self.base)

  def update(self, data):
    size = len(data)
    for i in xrange(0, size, self._nmax):
      for c in data[i:i+self._nmax]:
        self.sum += self.map(c)
        self.sum2 += self.sum
      n = min(self._nmax, size - i)
      self.sum = (self.sum + n * self.offs) % self.base
      self.sum2 = (self.sum2 + n * (n+1) / 2 * self.offs) % self.base
    self.count += size

  def rollin(self, cn):
    self.sum += self.map(cn) + self.offs
    # Note: timeit shows this is a little faster than "% self.base".
    if self.sum >= self.base:
      self.sum -= self.base
    self.sum2 += self.sum
    if self.sum2 >= self.base:
      self.sum2 -= self.base
    self.count += 1

  def rollout(self, c1):
    c1 = self.map(c1) + self.offs
    self.sum -= c1
    if self.sum < 0:
      self.sum += self.base
    self.sum2 -= self.count * c1 + self.seed
    if self.sum2 < 0:
      self.sum2 += self.base
    self.count -= 1

  def rotate(self, c1, cn):
    c1, cn = self.map(c1), self.map(cn)
    self.sum = (self.sum + cn - c1) % self.base
    # Note: timeit shows this is a little slower than "% self.base".
    # if self.sum >= self.base:
    #   self.sum -= self.base
    # elif self.sum < 0:
    #   self.sum += self.base
    self.sum2 = (self.sum2 + self.sum - self.count * (c1 + self.offs) - self.seed) % self.base

  def digest(self):
    return (self.sum2<<16) | self.sum


class RabinKarp(BaseHash):
  """Rabin-Karp rolling checksum."""

  def __init__(self, data=None, seed=0, offs=0, map=ord, mult=None):
    """Initialize a Rabin-Karp rollsum calculator.

    Args:
      data: optional str input data to update with.
      seed: optional value to initialize sum with.
      offs: optional offset to add to each byte.
      map: optional mapping function to transform input bytes.
      mult: optional Rabin-Karp multiplier to use (default: 2^32 - 3).
    """
    mult = mult or ((1 << 32) - 3)
    # The rabinkarp multiplier.
    self.mult = mult
    # The modular 2^32 inverse of mult.
    self.invm = modinv(mult, 1 << 32)
    # Calc ajustment for rolling character out.
    self._adj = offs + (mult - 1) * seed
    # Initialize multiplier for rolling character out to mult^count = 1.
    self._multn = 1
    super(RabinKarp, self).__init__(data, seed, offs, map)

  def __str__(self):
    return 'RabinKarp(seed=%s, offs=%s, map=%s, mult=%#x)' % (
        self.seed, self.offs, self.map.__name__, self.mult)

  def update(self, data):
    for c in data:
      self.sum = (self.sum * self.mult + self.map(c) + self.offs) & self.mask
    self.count += len(data)
    self._multn = (self.mult ** self.count) & self.mask

  def rollin(self, cn):
    self.sum = (self.sum * self.mult + self.map(cn) + self.offs) & self.mask
    self.count += 1
    self._multn = (self._multn * self.mult) & self.mask

  def rollout(self, c1):
    self.count -= 1
    self._multn = (self._multn * self.invm) & self.mask
    self.sum = (self.sum - self._multn * (self.map(c1) + self._adj)) & self.mask

  def rotate(self, c1, cn):
    c1, cn = self.map(c1) + self._adj, self.map(cn) + self.offs
    self.sum = (self.sum * self.mult + cn - self._multn * c1) & self.mask


class CyclicPoly(BaseHash):
  """Cyclic Polynomial rolling checksum."""

  def __init__(self, data=None, seed=0, offs=0, map=ord):
    # Calculate adjustment for rolling characters out.
    self._adj = (seed << 1) ^ seed
    # Initialise shift left and shift right for rolling characters out.
    self._sl, self._sr = 0, 32
    super(CyclicPoly, self).__init__(data, seed, offs, map)

  def __str__(self):
    return 'CyclicPoly(seed=%s, offs=%s, map=%s)' % (
        self.seed, self.offs, self.map.__name__)

  def _calcs(self):
    self._sl = self.count & 31  # shift left for rotlC.
    self._sr = 32 - self._sl    # shift right for rotlC.

  def _rotlC(self, v):
    return ((v << self._sl) & self.mask) | (v >> self._sr)

  def _rotl1(self, v):
    return ((v << 1) & self.mask) | (v >> 31)

  def update(self, data):
    for c in data:
      self.sum = self._rotl1(self.sum) ^ (self.map(c) + self.offs)
    self.count += len(data)
    self._calcs()

  def rollin(self, cn):
    self.sum = self._rotl1(self.sum) ^ (self.map(cn) + self.offs)
    self.count += 1
    self._calcs()

  def rollout(self, c1):
    self.count -= 1
    self._calcs()
    self.sum = self.sum ^ self._rotlC((self.map(c1) + self.offs) ^ self._adj)

  def rotate(self, c1, cn):
    #self.sum = rotl1(self.sum) ^ cn ^ rotlC(c1 ^ rotl1(seed) ^ seed)
    c1, cn = (self.map(c1) + self.offs) ^ self._adj, self.map(cn) + self.offs
    h = ((self.sum << 1) & self.mask) | (self.sum >> (32 - 1))
    c1 = ((c1 << self._sl) & self.mask) | (c1 >> self._sr)
    self.sum = h ^ cn ^ c1


class Stats(object):
  """Simple distribution statistics."""

  def __init__(self, data=None):
    self.num = 0
    self.sum = self.sum2 = 0
    self.min = self.max = None
    if data:
      self.update(data)

  def add(self, v, num=1):
    if num:
      self.num += num
      self.sum += v*num
      self.sum2 += v*v*num
      if self.min is None or v < self.min:
        self.min = v
      if self.max is None or v > self.max:
        self.max = v

  def update(self, data):
    for v in data:
      self.add(v)

  @property
  def avg(self):
    return float(self.sum) / self.num

  @property
  def var(self):
    avg = self.avg
    return float(self.sum2) / self.num - avg * avg

  @property
  def sdev(self):
    return self.var ** 0.5

  def __str__(self):
    return "num=%s sum=%s min/avg/max/sdev=%s/%s/%s/%s" % (self.num, self.sum, self.min, self.avg, self.max, self.sdev)


class TableStats(Stats):
  """Statistics for hastable performance."""

  def addempty(self, size):
      # Get the number of empty buckets and collisions.
      self.num_empty = size - self.num
      self.num_colls = self.sum - self.num
      # Add all the empty table entries.
      self.add(0, self.num_empty)
      self.size = self.num
      self.count = self.sum

  @property
  def perf(self):
    return self.avg / self.var

  @property
  def colls(self):
    return float(self.num_colls) / self.count

  @property
  def empty(self):
    return float(self.num_empty) / self.size

  def __str__(self):
    return "size=%s count=%s min/avg/max/sdev=%s/%s/%s/%s empty=%.6f colls=%.6f perf=%.4f" % (
        self.size, self.count, self.min, self.avg, self.max, self.sdev, self.empty, self.colls, self.perf)


class HashTable(object):
  """Simple Hashtable for collecting hash collision stats."""

  def __init__(self, size, hashfunc):
    self.size = size
    self.data = dict()
    self.hash = hashfunc

  def add(self, key, value):
    self.data.setdefault(self.hash(key), set()).add(value)

  def stats(self):
    stats = TableStats()
    # Add all the used table buckets.
    for v in self.data.itervalues():
      stats.add(len(v))
    # Add all the empty table buckets.
    stats.addempty(self.size)
    return stats

  def __str__(self):
    return str(self.stats())


def mix32(i):
  """MurmurHash3 mix32 finalizer."""
  i ^= i >> 16
  i = (i * 0x85ebca6b) & 0xffffffff
  i ^= i >>13
  i = (i * 0xc2b2ae35) & 0xffffffff
  i ^= i >> 16
  return i

def md5sum(data):
  return md5.new(data).digest()

def pow(c):
  """Rollsum map(c)->c^2 function."""
  c = ord(c)
  return c*c

def mul(c):
  """Rollsum ord(c)*173 function."""
  return ord(c) * 173

_mix32_map = [mix32(i) for i in range(256)]
def mix(c):
  return _mix32_map[ord(c)]

def runtest(rollsum, infile, blocksize=1024, blockcount=10000, tables=()):
  """Run a test using a rollsum instance collecting stats in multiple tables."""
  # Read first block and initialize data stats.
  data = infile.read(blocksize)
  datastats = Stats(rollsum.map(c) for c in data)
  # Add first block to rollsum and hashtables.
  rollsum.update(data)
  key, value = rollsum.digest(), md5sum(data)
  for t in tables:
    t.add(key, value)
  blockcount -= 1
  # Roll through the rest of the input one char at a time.
  c = infile.read(1)
  while c and blockcount:
    # Update data stats, rollsum, and hash tables.
    datastats.add(rollsum.map(c))
    rollsum.rotate(data[0],c)
    data = data[1:] + c
    key, value = rollsum.digest(), md5sum(data)
    for t in tables:
      t.add(key, value)
    blockcount -= 1
    c = infile.read(1)
  return datastats


if __name__ == "__main__":

  import sys,argparse

  def rollsum(s):
    """Parser for --rollsum argument."""
    try:
      return dict(rs=RollSum, rk=RabinKarp, cp=CyclicPoly)[s]
    except KeyError:
      raise ValueError(s)

  def map(s):
    """Parser for --map argument."""
    try:
      return dict(ord=ord, pow=pow, mul=mul, mix=mix)[s]
    except KeyError:
      raise ValueError(s)

  def size(s):
    """Parser for --blocksize argument."""
    scales='BKMGT'
    if s[-1] in scales:
      return int(s[:-1]) * 1024**(scales.find(s[-1]))
    else:
      return int(s)

  parser = argparse.ArgumentParser(description='Test different rollsum variants')
  parser.add_argument('--rollsum','-R', type=rollsum, default=RollSum, help='Rollsum to use "rs|rk|cp".')
  parser.add_argument('--blocksize','-B', type=size, default=1024, help='Block size to use.')
  parser.add_argument('--blockcount','-C', type=size, default=1000000, help='Number of blocks to use.')
  parser.add_argument('--seed', type=int, default=0, help='Value to initialize hash to.')
  parser.add_argument('--offs', type=int, default=31, help='Value to add to each input byte.')
  parser.add_argument('--base', type=eval, default=2**16, help='Value to mod s1 and s2 with.')
  parser.add_argument('--mult', type=eval, default=None, help='RabinKarp multiplier to use.')
  parser.add_argument('--map', type=map, default=ord, help='Map type to use "ord|pow|mul|mix16|mix32".')
  parser.add_argument('--indexbits', type=int, default=20, help='Number of bits in the hashtable index.')
  args=parser.parse_args()

  index_size = 2**args.indexbits
  index_mask = index_size - 1
  # Initialize rollsum and hash tables for collecting stats.
  if args.rollsum == RollSum:
    rollsum = RollSum(seed=args.seed, offs=args.offs, map=args.map, base=args.base)
  elif args.rollsum == RabinKarp:
    rollsum = RabinKarp(seed=args.seed, offs=args.offs, map=args.map, mult=args.mult)
  elif args.rollsum == CyclicPoly:
    rollsum = CyclicPoly(seed=args.seed, offs=args.offs, map=args.map)
  sumtable = HashTable(2**32, lambda k: k)
  s1index = HashTable(2**16, lambda k: k & 0xffff)
  s2index = HashTable(2**16, lambda k: k >> 16)
  andmask = HashTable(index_size, lambda k: k & index_mask)
  modmask = HashTable(index_size, lambda k: k % index_mask)
  mixmask = HashTable(index_size, lambda k: mix32(k) & index_mask)
  andcluster = HashTable(index_size>>4, lambda k: (k & index_mask)>>4)
  modcluster = HashTable(index_size>>4, lambda k: (k % index_mask)>>4)
  mixcluster = HashTable(index_size>>4, lambda k: (mix32(k) & index_mask)>>4)
  titles = ("rollsum:", "s1sum:", "s2sum:", "and_mask:", "mod_mask:", "mix_mask:", "and_clust:", "mod_clust:", "mix_clust:")
  tables = (sumtable, s1index, s2index, andmask, modmask, mixmask, andcluster, modcluster, mixcluster)

  # Run the test and display results.
  datastats = runtest(rollsum, sys.stdin, args.blocksize, args.blockcount, tables)
  print "Results for blocksize=%s blockcount=%s %s indexbits=%s" % (
      args.blocksize, args.blockcount, rollsum, args.indexbits)
  print
  print "map_data: %s" % datastats
  for title, table in zip(titles, tables):
    print title, table
