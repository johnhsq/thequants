#####
# One-Sample T-Test
# test if the average of a single group is different from a known average or hypothesized average
#####

# generate 1 samples of 30 observations each. 
# Sample A is taken from a population of mean 50 and a standard deviation of 15. 
import random
random.seed(20) #for results to be recreated
N = 30 #number of samples to take from each population
a = [random.gauss(50,15) for x in range(N)] #take N samples from population A
popmean = 50.5  #hypothesized population mean

# Using the seaborn library to generate a histogram of our 2 samples
import seaborn as sns
import matplotlib.pyplot as plt
sns.kdeplot(a, shade=True)
plt.title("One Sample T-Test")
plt.show()

# Null Hypothesis: µa  = X (the population mean is equal to a mean of X)
# Alternate Hypothesis: µa ≠ X (he population mean is not equal to a mean of X )
from scipy import stats
tStat, pValue =  stats.ttest_1samp(a, popmean, axis=0)
print("P-Value:{0} T-Statistic:{1}".format(pValue,tStat)) #print the P-Value and the T-Statistic
###P-Value:0.5340949682112062 T-Statistic:0.6292755379958038

### conclusion
# Since the P-Value is not low, 0.5 in this case, 
# we fail to reject the Null Hypothesis. 
# Statistically speaking, there is not enough evidence 
# to conclude that the population average (mean) is not equal to 50.5.