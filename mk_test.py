
import numpy as np
from math import sqrt
from scipy.stats import norm

def mann_kendall(x, alpha=0.05):
    """
    Mann–Kendall trend test for a 1D sequence x.
    Returns dict with S, varS, Z, p, trend ('increasing'/'decreasing'/'no trend').
    """
    x = np.asarray(x, dtype=float)
    x = x[~np.isnan(x)]
    n = len(x)
    if n < 8:
        return {"S":0, "varS":0, "Z":0.0, "p":1.0, "trend":"no trend"}

    # Compute S
    S = 0
    for k in range(n-1):
        S += np.sum(np.sign(x[k+1:] - x[k]))

    # Ties correction
    unique, counts = np.unique(x, return_counts=True)
    ties = counts[counts > 1]
    varS = (n*(n-1)*(2*n+1))/18.0
    if len(ties) > 0:
        tie_term = np.sum(ties*(ties-1)*(2*ties+1))
        varS -= tie_term/18.0

    # Continuity correction
    if S > 0:
        Z = (S - 1) / sqrt(varS)
    elif S < 0:
        Z = (S + 1) / sqrt(varS)
    else:
        Z = 0.0

    p = 2*(1 - norm.cdf(abs(Z)))
    if p < alpha:
        trend = "increasing" if Z > 0 else "decreasing"
    else:
        trend = "no trend"
    return {"S":int(S), "varS":float(varS), "Z":float(Z), "p":float(p), "trend":trend}
