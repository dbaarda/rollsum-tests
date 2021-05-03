#!/usr/bin/pypy -O
import rollsum

bc = 1000000
K = 1024

def dotest(src, bsize, bcount, sum):
  f = open('data/%s.dat' % src, 'rb')
  table = rollsum.HashTable(2**32, lambda k: k)
  clust = rollsum.HashTable(2**16, lambda k: (k & (2**20 - 1)) >> 4)
  datastats = rollsum.runtest(sum, f, bsize, bcount, (table, clust))
  #print "%-52s: %s %s" % (sum, table, clust)
  colls = table.stats()
  clust  = clust.stats()
  collsw, clustw = colls.weight, clust.weight
  # Score is geometric mean of collision and cluster performance,
  # Weighted by their digits of accuracy.
  score = (colls.perf**collsw * clust.perf**clustw)**(1/(collsw + clustw))
  return src, bsize, bcount, sum, colls, clust, score

def fmtstats(stats):
  return '%s/%s/%8.6f/%8.6f' % (stats.min, stats.max, stats.colls, stats.perf)

def printtable(results):
  f = '='
  hdr = '%3s %4s %7s %-52s %-25s %-25s %8s'
  fmt = '%3s %4s %7s %-52s %-25s %-25s %8.6f'
  frame = hdr % (3*f, 4*f, 7*f, 52*f, 25*f, 25*f, 8*f)
  print frame
  print hdr % ('dat', 'bs', 'count', 'rollsum', 'hash min/max/col/perf', 'cluster min/max/col/perf', 'score')
  print frame
  for src, bsize, bcount, sum, table, clust, score in results:
    if bsize >= 1024:
      bsize = '%sK' % (bsize/K)
    bcount = table.count
    table = fmtstats(table)
    clust = fmtstats(clust)
    print fmt % (src, bsize, bcount, sum, table, clust, score)
  print frame


datas = ('csv', 'zip')
sizes = (16, 32, 1*K, 4*K, 16*K, 64*K) # 256*K)
ans = []
# Test for different sources.
for src in datas:
  # Test for different blocksize.
  for blocksize in sizes:
    # test Gear variants with blocksize<=32 only.
    if blocksize <= 32:
      # Test Gear variants with different mappings.
      for mapfunc in (ord, rollsum.mul, rollsum.mix, rollsum.ipfs):
        sum = rollsum.Gear(map=mapfunc)
        ans.append(dotest(src, blocksize, bc, sum))
        sum = rollsum.RGear(map=mapfunc)
        ans.append(dotest(src, blocksize, bc, sum))
        sum = rollsum.UGear(map=mapfunc)
        ans.append(dotest(src, blocksize, bc, sum))
      # Test MGear with ord mapping only.
      sum = rollsum.MGear(map=ord)
      ans.append(dotest(src, blocksize, bc, sum))
    # Test rsync rollsum seed and offs values.
    sum = rollsum.RollSum(seed=0, offs=31, base=0x10000, map=ord)
    ans.append(dotest(src, blocksize, bc, sum))
    # Test RabinKarp with seed and offs.
    sum = rollsum.RabinKarp(seed=1, mult=0x08104225, map=ord)
    ans.append(dotest(src, blocksize, bc, sum))
    sum = rollsum.RabinKarp(offs=1, mult=0x08104225, map=ord)
    ans.append(dotest(src, blocksize, bc, sum))
    # Test CyclicPoly with different mappings.
    for mapfunc in (ord, rollsum.pow, rollsum.mul, rollsum.mix, rollsum.ipfs):
      sum = rollsum.CyclicPoly(map=mapfunc)
      ans.append(dotest(src, blocksize, bc, sum))
    # Test RollSum and RabinKarp with different mappings.
    for mapfunc in (ord, rollsum.pow, rollsum.mul):
      sum = rollsum.RollSum(seed=1, offs=0, base=0x10000, map=mapfunc)
      ans.append(dotest(src, blocksize, bc, sum))
      for mult in (0xfffffffd, 0x55555555, 0x08104225, 0x41c64e6d):
	sum = rollsum.RabinKarp(mult=mult, map=mapfunc)
        ans.append(dotest(src, blocksize, bc, sum))
# Sort results by src, bsize, and then score.
ans = sorted(ans, key=lambda a: (a[0:2], -a[-1]))
printtable(ans)
