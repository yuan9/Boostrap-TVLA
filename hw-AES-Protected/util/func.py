import numpy as np

from scipy.special import kolmogorov, smirnov, betainc
from scipy.stats.distributions import ksone, kstwobign

from scipy.stats.stats import _betai

dpawstools = False
try:
  import DpawsTools
  dpawstools = True
except ImportError:
  pass

def dpa_ttest(traces, classifiers):
  pass


# Converting correlation to pvalue
def betai(a, b, x):
  x = np.asarray(x)
  x = np.where(x < 1.0, x, 1.0)  # if x > 1 then return 1.0
  return betainc(a, b, x)

def r2pv(r, n):
  df = n - 2
  tsq = r**2 * (df / ((1.0 - r) * (1.0 + r)))
  return betai(0.5*df, 0.5, df/(df+tsq))

def kstest(rvs, cdf):
  N = len(rvs)
  cdfvals = cdf(np.sort(rvs))
  space = np.arange(0.0, N)
  Dplus = ((space + 1)/N - cdfvals).max()
  Dmin  = (cdfvals - space/N).max()
  D = max(Dplus, Dmin)
  pval_two = kolmogorov(D * np.sqrt(N))
  if N < 2666 and (pval_two < (2666 - N)/3000.0):
    pval_two = 2 * ksone.sf(D, N)
  return D, pval_two
