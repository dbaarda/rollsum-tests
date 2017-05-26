#!/usr/bin/python
import rollsum

bc = 1000000
K = 1024

def dotest(src, bsize, bcount, sum):
  f = open('data/%s.dat' % src, 'rb')
  table = rollsum.HashTable(2**32, lambda k: k)
  clust = rollsum.HashTable(2**16, lambda k: (k & (2**20 - 1)) >> 4)
  datastats = rollsum.runtest(sum, f, bsize, bcount, (table, clust))
  stats, empty, colls = table.stats()
  clust = clust.stats()[0]
  #print "%48s: %s %s" % (sum, stats, clust)
  return src, bsize, bcount, sum, stats, empty, colls, clust

ans = []
# Test for different sources.
for src in ('csv', 'zip'):
  # Test for different blocksize.
  for blocksize in (1*K, 4*K, 16*K, 64*K): # 256*K):
    # Test rsync rollsum.
    # ans.append(dotest(src, blocksize, bc, 0, 31, 0x10000, ord))
    # Test using map=mul.
    # ans.append(dotest(src, blocksize, bc, 1, 0, 0xffff, rollsum.mul))
    # Test for different character mappings.
    for mapfunc in (ord, rollsum.pow):
      sum = rollsum.RollSum(seed=1, offs=0, base=0x10000, map=mapfunc)
      ans.append(dotest(src, blocksize, bc, sum))
      sum = rollsum.CyclicPoly(map=mapfunc)
      ans.append(dotest(src, blocksize, bc, sum))
      for mult in (0xfffffffd, 0x55555555, 0x08104225, 0x41c64e6d):
	sum = rollsum.RabinKarp(mult=mult, map=mapfunc)
        ans.append(dotest(src, blocksize, bc, sum))
      sum = rollsum.RabinKarp(seed=1, mult=0x41c64e6d, map=mapfunc)
      ans.append(dotest(src, blocksize, bc, sum))
      sum = rollsum.RabinKarp(offs=1, mult=0x41c64e6d, map=mapfunc)
      ans.append(dotest(src, blocksize, bc, sum))


for a in sorted(ans, key=lambda a: (a[0:2], a[-4].sdev)):
  src, bsize, bcount, sum, stats, empty, colls, clust = a
  bsize = '%sK' % (bsize/K)
  stats = '%s/%8f/%s/%8f' % (stats.min, stats.avg, stats.max, stats.sdev)
  clust = '%s/%8f/%s/%8f' % (clust.min, clust.avg, clust.max, clust.sdev)
  map = sum.map.__name__
  fmt = '%s %4s %s %52s %s %.6f %.6f %s'
  val = (src, bsize, bcount, sum, stats, empty, colls, clust)
  print fmt % val
