import numpy as np

from scipy.special import kolmogorov, smirnov, betainc
from scipy.stats.distributions import ksone, kstwobign


# Converting correlation to pvalue
def r2pv(r, n):
  df = n - 2
  tsq = r**2 * (df / ((1.0 - r)*(1.0 + r)))
  bim = np.fmin(np.asarray(df/(df + tsq)), 1.0)
  return betainc(0.5*df, 0.5, bim)

# kstest simplified for performance
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