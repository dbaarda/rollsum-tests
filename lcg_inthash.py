#!/usr/bin/python

def factors(n):
  """Find all the prime factors of n."""
  f = []
  for i in xrange(2, int(n**0.5)+1):
    while n % i == 0:
      f.append(i)
      n /= i
  if n > 1:
    f.append(n)
  return f

_primes_searched = 2
_primes = [2]
def primes(m):
  """Find all the primes below m."""
  global _primes_searched
  for x in xrange(_primes_searched+1, m):
    if all(x % p for p in _primes):
      _primes.append(x)
  _primes_searched = max(_primes_searched, m)
  return [p for p in _primes if p <= m]

def maxprime(m):
  return primes(m)[-1]

def lcg_ac(m):
  """Calculate LCG a,c terms for a given m size."""
  factors_m = factors(m)
  primefactors_m = set(factors_m)
  c = max(set(primes(m)) - primefactors_m)
  a_1 = reduce(int.__mul__, primefactors_m)
  if factors_m.count(2) > 1:
    a_1 *= 2
  a_1 *= maxprime(m / (2*a_1))
  return a_1+1, c

def makehash(m, a, c):
  """Create an LCG integer hash function."""
  # Values a and c must be less than m.
  assert 0 < a < m
  assert 0 <= c < m
  # Values m and c are relatively prime.
#  assert not set(factors(m)) & set(factors(c))
  # All prime factors of m are factors of a-1.
  print m, set(factors(m)), a-1, set(factors(a-1))
#  assert not set(factors(m)) - set(factors(a-1))
  # Either m is not divisable by 4 or both m and a-1 are.
#  assert (m % 4) or not ((a-1) % 4)
  def hash(x):
    return (a * x + c) % m
  return hash


def check(m, a, c):
  """Check that a hash for size m covers all possible hash values.""" 
  hash = makehash(m, a, c)
  f = set(xrange(0, m))
  for x in range(0, m):
    h=hash(x)
    f.discard(h)
    print x, h
  print "m=%s,a=%s,c=%s missed set=%s" % (m,a,c,f)

def testa(m):
  b = 1
  a = 0
  s = 1
  while b < m:
    a |= b
    b <<= s
    s += 1
  print hex(a), bin(a)
  return a

if __name__ == '__main__':
  m = 0xffff
  a, c = lcg_ac(m)
  print hex(m), bin(a), bin(c)
  #a, c = testa(m), 0
  #check(m, a, c)
