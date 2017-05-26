#!/usr/bin/python

import rollsum

bc = 1000000
K = 1024


def dotest(src, bsize, bcount, seed, offs, base, map):
  f = open('data/%s.dat' % src, 'rb')
  r = rollsum.RollSum(seed=seed, offs=offs, base=base, map=map)
  table = rollsum.HashTable(2**32, lambda k: k)
  datastats = rollsum.runtest(r, f, bsize, bcount, (table,))
  stats, empty, colls = table.stats()
  return src, bsize, bcount, seed, offs, base, map, stats, empty, colls

ans = []
# Test for different sources.
for src in ('csv', 'zip'):
  # Test for different blocksize.
  for blocksize in (1*K, 4*K, 16*K, 64*K, 256*K):
    # Test rsync rollsum.
    # ans.append(dotest(src, blocksize, bc, 0, 31, 0x10000, ord))
    # Test using map=mul.
    # ans.append(dotest(src, blocksize, bc, 1, 0, 0xffff, rollsum.mul))
    # Test for different base.
    for base in (0x10000, 0xffff, 0xfff1):
      # Test for different character mappings.
      for mapfunc in (ord, rollsum.pow):
        ans.append(dotest(src, blocksize, bc, 1, 0, base, mapfunc))


for a in sorted(ans, key=lambda a: (a[0:2], a[-3].sdev)):
  src, bsize, bcount, seed, offs, base, map, stats, empty, colls = a
  bsize = '%sK' % (bsize/K)
  stats = '%s/%8f/%s/%8f' % (stats.min, stats.avg, stats.max, stats.sdev)
  map = map.__name__
  fmt = '%s %4s %s %s %s %#07x %s %s %.6f %.6f'
  val = (src, bsize, bcount, seed, offs, base, map, stats, empty, colls)
  print fmt % val
