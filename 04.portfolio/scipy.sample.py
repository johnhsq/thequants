import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import norm

print(stats.norm.__doc__)

rv = norm()
print(dir(rv))

print(norm.cdf([-1.,0,1]))
print(norm.cdf(np.array([-1., 0, 1])))
print(norm.mean(), norm.std(), norm.var())
print(norm.rvs(size=3))