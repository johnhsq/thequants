#####
# Paired Sample T-Test
# compare the average of two samples taken from the same population but at different points in time
#####

# generate 2 samples of 30 observations each. 
# Sample A is taken from a population of mean 50 and a standard deviation of 15. 
# Sample B is taken from a population of mean 60 and a standard deviation of 15.
import random
random.seed(20) #for results to be recreated
N = 30 #number of samples to take from each population
a = [random.gauss(50,15) for x in range(N)] #take N samples from population A at time T
b = [random.gauss(60,15) for x in range(N)] #take N samples from population A at time T+x


import seaborn as sns
import matplotlib.pyplot as plt
sns.kdeplot(a, shade=True)
sns.kdeplot(b, shade=True)
plt.title("Paired Sample T-Test")
plt.show()

# Null Hypothesis: µd = 0 (the mean difference (d) between both samples is equal to zero)
# Alternate Hypothesis: µd ≠ 0 (the mean difference (d) between both samples is not equal to zero )
from scipy import stats
tStat, pValue =  stats.ttest_rel(a, b)
print("P-Value:{0} T-Statistic:{1}".format(pValue,tStat)) #print the P-Value and the T-Statistic
###P-Value:0.007834002687720413 T-Statistic:-2.856841146891359

### conclusion
# As expected, since we generated the data, 
# we can reject the null hypothesis and 
# accept the alternative hypothesis that 
# the mean difference between both samples is not equal to zero.