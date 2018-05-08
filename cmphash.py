#!/usr/bin/python
import rollsum

bc = 1000000
K = 1024

def dotest(src, bsize, bcount, sum):
  f = open('data/%s.dat' % src, 'rb')
  table = rollsum.HashTable(2**32, lambda k: k)
  clust = rollsum.HashTable(2**16, lambda k: (k & (2**20 - 1)) >> 4)
  datastats = rollsum.runtest(sum, f, bsize, bcount, (table, clust))
  #print "%48s: %s %s" % (sum, stats, clust)
  return src, bsize, bcount, sum, table.stats(), clust.stats()

ans = []
# Test for different sources.
for src in ('csv', 'zip'):
  # Test for different blocksize.
  for blocksize in (1*K, 4*K, 16*K, 64*K): # 256*K):
    # Test rsync rollsum.
    sum = rollsum.RollSum(seed=0, offs=31, base=0x10000, map=ord)
    ans.append(dotest(src, blocksize, bc, sum))
    # Test using map=mul.
    sum = rollsum.RollSum(seed=1, offs=0, base=0x10000, map=rollsum.mul)
    ans.append(dotest(src, blocksize, bc, sum))
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

def fmtstats(stats):
  return '%s %s %.6f %.6f' % (stats.min, stats.max, stats.colls, stats.perf)

for a in sorted(ans, key=lambda a: (a[0:2], -a[-2].perf, -a[-1].perf)):
  src, bsize, bcount, sum, table, clust = a
  bsize = '%sK' % (bsize/K)
  bcount = table.count
  table = fmtstats(table)
  clust = fmtstats(clust)
  fmt = '%s %4s %s %52s %s %s'
  val = (src, bsize, bcount, sum, table, clust)
  print fmt % val
