import numpy as np

from scipy.stats import ttest_ind, ks_2samp, norm, rv_discrete, rv_continuous
from scipy.optimize import linprog


def welch_ttest_fvr(traces, classifiers):
  traces = np.asarray(traces, dtype=np.float64)
  classifiers = np.asarray(classifiers).astype(np.uint8)
  set0 = traces[np.where(classifiers == 0)]
  set1 = traces[np.where(classifiers == 1)]
  m0 = np.mean(set0, axis=0)
  m1 = np.mean(set1, axis=0)
  s0 = np.var(set0, axis=0, ddof=1)
  s1 = np.var(set1, axis=0, ddof=1)
  n0, n1 = len(set0), len(set1)
  return (m1 - m0) / np.sqrt(s0/n0 + s1/n1)

def generate_dist(moments, size, seed=0):
  m = moments[0]
  x = np.arange(-15, 16)
  c = np.ones_like(x)
  A_eq=[np.ones_like(x), x] + [(x - m) ** k for k in range(2, len(moments) + 1)]
  b_eq=[1] + moments
  p = linprog(c, A_eq=A_eq, b_eq=b_eq)
  assert p.success
  return rv_discrete(values=(x, p.x), seed=seed).rvs(size=size)
