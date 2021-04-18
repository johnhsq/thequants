import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt

# Set plotting options
#%matplotlib inline
plt.rc('figure', figsize=(16, 9))

### Create a normal and a non-normal distribution
# Sample A: Normal distribution
sample_a = stats.norm.rvs(loc=0.0, scale=1.0, size=(1000,))

# Sample B: Non-normal distribution
sample_b = stats.lognorm.rvs(s=0.5, loc=0.0, scale=1.0, size=(1000,))


### Boxplot-Whisker Plot and Histogram
# visually check if a distribution looks normally distributed. 
# a normal distribution
fig, axes = plt.subplots(2, 1, figsize=(16, 9), sharex=True)
# a box whisker plot lets us check for symmetry around the mean. 
axes[0].boxplot(sample_a, vert=False)
# A histogram lets us see the overall shape. 
axes[1].hist(sample_a, bins=50)
axes[0].set_title("Boxplot of a Normal Distribution")
plt.show()

# a log-normal distribution
fig, axes = plt.subplots(2, 1, figsize=(16, 9), sharex=True)
axes[0].boxplot(sample_b, vert=False)
axes[1].hist(sample_b, bins=50)
axes[0].set_title("Boxplot of a Lognormal Distribution")
plt.show()


# A QQ-plot lets us compare our data distribution with a normal distribution (or any other theoretical "ideal" distribution).
# Q-Q plot of normally-distributed sample
plt.figure(figsize=(10, 10)); plt.axis('equal')
stats.probplot(sample_a, dist='norm', plot=plt)
plt.show()

# Q-Q plot of non-normally-distributed sample
plt.figure(figsize=(10, 10)); plt.axis('equal')
stats.probplot(sample_b, dist='norm', plot=plt)
plt.show()



### Testing Normality
# Shapiro-Wilk
# The null hypothesis assumes that the data distribution is normal. 
# If the p-value is greater than the chosen alpha_level, we'll assume that it's normal. 
# Otherwise we assume that it's not normal.
def is_normal(sample, test=stats.shapiro, alpha_level=0.05, **kwargs):
    """Apply a normality test to check if sample is normally distributed."""
    t_stat, p_value = test(sample, **kwargs)
    print("Test statistic: {}, p-value: {}".format(t_stat, p_value))
    print("Is the distribution Likely Normal at Alpha level {} ? {}".format(alpha_level, p_value > alpha_level))
    return p_value > alpha_level

# Using Shapiro-Wilk test (default)
print("Sample A:-"); is_normal(sample_a);
print("Sample B:-"); is_normal(sample_b);

# Kolmogorov-Smirnov
# The K-S test compares the data distribution with a theoretical distribution. 
# We'll choose the 'norm' (normal) distribution as the theoretical distribution, 
# and we also need to specify the mean and standard deviation of this theoretical distribution. 
# We'll set the mean and stanadard deviation of the theoretical norm with the mean and standard deviation of the data distribution.
def is_normal_ks(sample, test=stats.kstest, alpha_level=0.05, **kwargs):
    """
    sample: a sample distribution
    test: a function that tests for normality
    alpha_level: if the test returns a p-value > than alpha_level, assume normality
    
    return: True if distribution is normal, False otherwise
    """
    normal_args = (np.mean(sample),np.std(sample))
    
    t_stat, p_value = test(sample, 'norm', normal_args, **kwargs)
    print("Test statistic: {}, p-value: {}".format(t_stat, p_value))
    print("Is the distribution Likely Normal at Alpha level {} ? {}".format(alpha_level, p_value > alpha_level))
    return p_value > alpha_level

# Using Kolmogorov-Smirnov test
print("Sample A:-"); is_normal_ks(sample_a)
print("Sample B:-"); is_normal_ks(sample_b)