#!/usr/bin/python

def modpow(k, n, m):
  """ Calculate "k^n" modular "m" efficiently.

  Even with python2 this is 100's of times faster than "(k**n) % m",
  particularly for large "n".
  """
  ans = 1
  kn = k
  while n:
    if n & 1:
      ans = (ans*kn) % m
    kn = (kn*kn) % m
    n >>= 1
  return ans

def modinv(k, m):
  """ Calculate the inverse of "k" modular "m".

  This is the number "i" that is equivalent to 1/k modular m and satisfies the
  equation;

  (i * k) % m = 1
  """
  # Values k and m need to be coprime AKA relatively prime.
  assert not set(factors(m)) & set(factors(k))
  x, xn = 0, 1
  n, d = m, k
  q, r = n / d, n % d
  while r:
    x, xn = xn, x - xn * q
    n, d = d, r
    q, r = n / d, n % d
  i = xn % m
  # The inverse i multiplied by k modular m must give 1.
  assert (i * k) % m == 1
  return i

def factors(n):
  """Find all the prime factors of n."""
  f = []
  while n % 2 == 0:
    f.append(2)
    n /= 2
  for i in xrange(3, int(n**0.5)+1, 2):
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
  # Choose the largest prime < m/2 that is not a factor of m.
  c = max(set(primes(m/2)) - primefactors_m)
  # Make a-1 have all the prime factors of m.
  a_1 = reduce(int.__mul__, primefactors_m)
  # If m is divisible by 4, make sure a-1 is also.
  if factors_m.count(2) > 1:
    a_1 *= 2
  # If a-1 is too small compared to m, multiply it by another prime.
  if 2*a_1 < m:
    a_1 *= maxprime(m / a_1)
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

def period(m, a, c):
  """Find the period for a hash starting at 1."""
  hash = makehash(m, a, c)
  h,o = 1, []
  while h not in o:
    print h
    o.append(h)
    h = hash(h)
  print h
  p = len(o) - o.index(h)
  print "m=%s,a=%s,c=%s period=%s" % (m, a, c, p)

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
  K = 0b1000000100000100001000100101
  M = 1<<32
  print "m=%s modinv(m)=%s" % (hex(K), hex(modinv(K,M)))
  m = 0xffff
  a, c = lcg_ac(m)
  print "m=%s, a=%s (%s), c=%s (%s)" %(hex(m), hex(a), bin(a), hex(c), bin(c))
  #a, c = testa(m), 0
  #check(m, a, c)
