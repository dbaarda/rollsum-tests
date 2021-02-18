#!/usr/bin/pypy -O
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
    # We only use 16 LSB's of the map output, so wrap map if it is >16bit.
    cmax = max(map(chr(c)) for c in xrange(256))
    if cmax > 0xffff:
      _map = lambda c: map(c) & 0xffff
      _map.__name__ = map.__name__
      cmax = max(_map(chr(c)) for c in xrange(256))
    else:
      _map = map
    self.base, self.sum2 = base, 0
    # Find the max updates without doing mod where sum2 doesn't overflow.
    # Largest n such that n*(n+1)/2*(cmax+offs)+(n+1)*(base-1) <= 2^32-1.
    # Where cmax is the largest possible map(c) value.
    # Solving using (-b + sqrt(b^2 - 4*a*c)) / (2*a).
    a = (cmax + offs)/2.0
    b = a + (base-1)
    c = (base-1) - (2**32 - 1)
    self._nmax = int((-b + (b**2 - 4*a*c)**0.5) / (2*a))
    super(RollSum, self).__init__(data, seed, offs, _map)

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
    while self.sum >= self.base:
      self.sum -= self.base
    self.sum2 += self.sum
    if self.sum2 >= self.base:
      self.sum2 -= self.base
    self.count += 1

  def rollout(self, c1):
    c1 = self.map(c1) + self.offs
    self.sum -= c1
    while self.sum < 0:
      self.sum += self.base
    self.sum2 -= self.count * c1 + self.seed
    self.sum2 %= self.base
    self.count -= 1

  def rotate(self, c1, cn):
    c1, cn = self.map(c1), self.map(cn)
    self.sum += cn - c1
    # Note: timeit shows this is a little faster than "%= self.base".
    while self.sum >= self.base:
      self.sum -= self.base
    while self.sum < 0:
      self.sum += self.base
    self.sum2 += self.sum - (self.count * (c1 + self.offs) + self.seed)
    self.sum2 %= self.base

  def digest(self):
    return (self.sum2<<16) | self.sum


class RabinKarp(BaseHash):
  """Rabin-Karp rolling checksum (polyhash)."""

  def __init__(self, data=None, seed=0, offs=0, map=ord, mult=0x08104225):
    """Initialize a Rabin-Karp rollsum calculator.

    Args:
      data: optional str input data to update with.
      seed: optional value to initialize sum with.
      offs: optional offset to add to each byte.
      map: optional mapping function to transform input bytes.
      mult: optional Rabin-Karp multiplier to use (default: 0x08104225).
    """
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
  """Cyclic Polynomial rolling checksum (buzzhash)."""

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


class Gear(BaseHash):
  """Gear rolling checksum.

  This rollsum is special and designed for chunking. It effectively uses a
  fixed window with as many bytes as there are bits in the checksum, and
  naturally rolls data out by shifting it left for each byte rolled in. This
  means it is very fast and you don't need to keep a sliding window. It also
  means it can't really be used for checksumming a block of data, as it always
  only checksums the last 32 bytes.

  Note that this is identical to RabinKarp with mult=2.
  """

  def __init__(self, data=None, offs=0, map=ord):
    super(Gear, self).__init__(data, 0, offs, map)
    self.count = 32

  def __str__(self):
    return 'Gear(offs=%s, map=%s)' % (
        self.offs, self.map.__name__)

  def update(self, data):
    for c in data:
      self.sum = ((self.sum<<1) + self.map(c) + self.offs) & self.mask

  def rollin(self, cn):
    self.sum = ((self.sum<<1) + self.map(cn) + self.offs) & self.mask

  def rollout(self, c1):
    pass

  def rotate(self, c1, cn):
    self.rollin(cn)


class RGear(BaseHash):
  """RGear rolling checksum.

  This is a modified version of Gear that uses a right shift instead of a left
  shift as introduced in https://github.com/ronomon/deduplication. It is
  unusual and harder to analyse because it means bytes don't fully "expire"
  from the hash, so bytes from the very start of the block can modify the
  hash. This is because addition in the Gear rollsum also propogates some bit
  changes upwards. This means the sliding window size is variable depending on
  the data. It still usually only includes the last 32 bytes, because the
  chance of a changed older byte impacting on bits in the hash quickly
  approaches zero.
  """

  def __init__(self, data=None, offs=0, map=ord):
    # We only use 31 LSB's of the map output, so wrap map if it is >31bit.
    cmax = max(map(chr(c)) for c in xrange(256))
    if cmax > 0x7fffffff:
      _map = lambda c: map(c) & 0x7fffffff
      _map.__name__ = map.__name__
    else:
      _map = map
    super(RGear, self).__init__(data, 0, offs, _map)

  def __str__(self):
    return 'RGear(offs=%s, map=%s)' % (
        self.offs, self.map.__name__)

  def update(self, data):
    for c in data:
      self.sum = ((self.sum>>1) + self.map(c) + self.offs)
    self.count += len(data)

  def rollin(self, cn):
    self.sum = ((self.sum>>1) + self.map(cn) + self.offs)
    self.count += 1

  def rollout(self, c1):
    self.count -= 1

  def rotate(self, c1, cn):
    self.sum = ((self.sum>>1) + self.map(cn) + self.offs)


inf = float('inf')

class Stats(object):
  """Simple distribution statistics."""

  def __init__(self, data=None):
    self.num = 0
    self.sum = self.sum2 = 0
    self.min, self.max = inf, -inf
    if data:
      self.update(data)

  def add(self, v, num=1):
    if num:
      self.num += num
      self.sum += v*num
      self.sum2 += v*v*num
      self.min = min(self.min, v)
      self.max = max(self.max, v)

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
  def dev(self):
    return self.var ** 0.5

  def __str__(self):
    return "num=%s sum=%s min/avg/max/dev=%s/%s/%s/%s" % (self.num, self.sum, self.min, self.avg, self.max, self.dev)


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
    return "size=%s count=%s min/avg/max/dev=%s/%s/%s/%s empty=%.6f colls=%.6f perf=%.4f" % (
        self.size, self.count, self.min, self.avg, self.max, self.dev, self.empty, self.colls, self.perf)


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

_mul_map = [(c * 0x08104225) & 0xffffffff for c in xrange(256)]
def mul(c):
  """Rollsum ord(c)*0x08104225&0xffffffff function."""
  return _mul_map[ord(c)]

_mix32_map = [mix32(i) for i in xrange(256)]
def mix(c):
  return _mix32_map[ord(c)]

# This is the bytehash map used by ipfs buzhash.
_ipfs_map = [
    0x6236e7d5, 0x10279b0b, 0x72818182, 0xdc526514, 0x2fd41e3d, 0x777ef8c8,
    0x83ee5285, 0x2c8f3637, 0x2f049c1a, 0x57df9791, 0x9207151f, 0x9b544818,
    0x74eef658, 0x2028ca60, 0x0271d91a, 0x27ae587e, 0xecf9fa5f, 0x236e71cd,
    0xf43a8a2e, 0xbb13380, 0x9e57912c, 0x89a26cdb, 0x9fcf3d71, 0xa86da6f1,
    0x9c49f376, 0x346aecc7, 0xf094a9ee, 0xea99e9cb, 0xb01713c6, 0x88acffb,
    0x2960a0fb, 0x344a626c, 0x7ff22a46, 0x6d7a1aa5, 0x6a714916, 0x41d454ca,
    0x8325b830, 0xb65f563, 0x447fecca, 0xf9d0ea5e, 0xc1d9d3d4, 0xcb5ec574,
    0x55aae902, 0x86edc0e7, 0xd3a9e33, 0xe70dc1e1, 0xe3c5f639, 0x9b43140a,
    0xc6490ac5, 0x5e4030fb, 0x8e976dd5, 0xa87468ea, 0xf830ef6f, 0xcc1ed5a5,
    0x611f4e78, 0xddd11905, 0xf2613904, 0x566c67b9, 0x905a5ccc, 0x7b37b3a4,
    0x4b53898a, 0x6b8fd29d, 0xaad81575, 0x511be414, 0x3cfac1e7, 0x8029a179,
    0xd40efeda, 0x7380e02, 0xdc9beffd, 0x2d049082, 0x99bc7831, 0xff5002a8,
    0x21ce7646, 0x1cd049b, 0xf43994f, 0xc3c6c5a5, 0xbbda5f50, 0xec15ec7,
    0x9adb19b6, 0xc1e80b9, 0xb9b52968, 0xae162419, 0x2542b405, 0x91a42e9d,
    0x6be0f668, 0x6ed7a6b9, 0xbc2777b4, 0xe162ce56, 0x4266aad5, 0x60fdb704,
    0x66f832a5, 0x9595f6ca, 0xfee83ced, 0x55228d99, 0x12bf0e28, 0x66896459,
    0x789afda, 0x282baa8, 0x2367a343, 0x591491b0, 0x2ff1a4b1, 0x410739b6,
    0x9b7055a0, 0x2e0eb229, 0x24fc8252, 0x3327d3df, 0xb0782669, 0x1c62e069,
    0x7f503101, 0xf50593ae, 0xd9eb275d, 0xe00eb678, 0x5917ccde, 0x97b9660a,
    0xdd06202d, 0xed229e22, 0xa9c735bf, 0xd6316fe6, 0x6fc72e4c, 0x206dfa2,
    0xd6b15c5a, 0x69d87b49, 0x9c97745, 0x13445d61, 0x35a975aa, 0x859aa9b9,
    0x65380013, 0xd1fb6391, 0xc29255fd, 0x784a3b91, 0xb9e74c26, 0x63ce4d40,
    0xc07cbe9e, 0xe6e4529e, 0xfb3632f, 0x9438d9c9, 0x682f94a8, 0xf8fd4611,
    0x257ec1ed, 0x475ce3d6, 0x60ee2db1, 0x2afab002, 0x2b9e4878, 0x86b340de,
    0x1482fdca, 0xfe41b3bf, 0xd4a412b0, 0xe09db98c, 0xc1af5d53, 0x7e55e25f,
    0xd3346b38, 0xb7a12cbd, 0x9c6827ba, 0x71f78bee, 0x8c3a0f52, 0x150491b0,
    0xf26de912, 0x233e3a4e, 0xd309ebba, 0xa0a9e0ff, 0xca2b5921, 0xeeb9893c,
    0x33829e88, 0x9870cc2a, 0x23c4b9d0, 0xeba32ea3, 0xbdac4d22, 0x3bc8c44c,
    0x1e8d0397, 0xf9327735, 0x783b009f, 0xeb83742, 0x2621dc71, 0xed017d03,
    0x5c760aa1, 0x5a69814b, 0x96e3047f, 0xa93c9cde, 0x615c86f5, 0xb4322aa5,
    0x4225534d, 0xd2e2de3, 0xccfccc4b, 0xbac2a57, 0xf0a06d04, 0xbc78d737,
    0xf2d1f766, 0xf5a7953c, 0xbcdfda85, 0x5213b7d5, 0xbce8a328, 0xd38f5f18,
    0xdb094244, 0xfe571253, 0x317fa7ee, 0x4a324f43, 0x3ffc39d9, 0x51b3fa8e,
    0x7a4bee9f, 0x78bbc682, 0x9f5c0350, 0x2fe286c, 0x245ab686, 0xed6bf7d7,
    0xac4988a, 0x3fe010fa, 0xc65fe369, 0xa45749cb, 0x2b84e537, 0xde9ff363,
    0x20540f9a, 0xaa8c9b34, 0x5bc476b3, 0x1d574bd7, 0x929100ad, 0x4721de4d,
    0x27df1b05, 0x58b18546, 0xb7e76764, 0xdf904e58, 0x97af57a1, 0xbd4dc433,
    0xa6256dfd, 0xf63998f3, 0xf1e05833, 0xe20acf26, 0xf57fd9d6, 0x90300b4d,
    0x89df4290, 0x68d01cbc, 0xcf893ee3, 0xcc42a046, 0x778e181b, 0x67265c76,
    0xe981a4c4, 0x82991da1, 0x708f7294, 0xe6e2ae62, 0xfc441870, 0x95e1b0b6,
    0x445f825, 0x5a93b47f, 0x5e9cf4be, 0x84da71e7, 0x9d9582b0, 0x9bf835ef,
    0x591f61e2, 0x43325985, 0x5d2de32e, 0x8d8fbf0f, 0x95b30f38, 0x7ad5b6e,
    0x4e934edf, 0x3cd4990e, 0x9053e259, 0x5c41857d]
def ipfs(c):
  return _ipfs_map[ord(c)]

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
      return dict(rs=RollSum, rk=RabinKarp, cp=CyclicPoly, gr=Gear, rg=RGear)[s]
    except KeyError:
      raise ValueError(s)

  def map(s):
    """Parser for --map argument."""
    try:
      return dict(ord=ord, pow=pow, mul=mul, mix=mix, ipfs=ipfs)[s]
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
  parser.add_argument('--rollsum','-R', type=rollsum, default=RollSum, help='Rollsum to use "rs|rk|cp|gr|rg".')
  parser.add_argument('--blocksize','-B', type=size, default=1024, help='Block size to use.')
  parser.add_argument('--blockcount','-C', type=size, default=1000000, help='Number of blocks to use.')
  parser.add_argument('--seed', type=int, default=0, help='Value to initialize hash to.')
  parser.add_argument('--offs', type=int, default=31, help='Value to add to each input byte.')
  parser.add_argument('--base', type=eval, default=2**16, help='RollSum value to mod s1 and s2 with.')
  parser.add_argument('--mult', type=eval, default=0x08104225, help='RabinKarp multiplier to use.')
  parser.add_argument('--map', type=map, default=ord, help='Map type to use "ord|pow|mul|mix|ipfs".')
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
  elif args.rollsum == Gear:
    rollsum = Gear(offs=args.offs, map=args.map)
  elif args.rollsum == RGear:
    rollsum = RGear(offs=args.offs, map=args.map)
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
