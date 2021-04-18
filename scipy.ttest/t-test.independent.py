#####
# Independent Sample T-Test
# comparing samples from two different populations and are testing whether or not they have a different average.
#####


# generate 2 samples of 50 observations each. 
# Sample A is taken from a population of mean 55 and a standard deviation of 20. 
# Sample B is taken from a population of mean 50 and a standard deviation of 15.
import random
random.seed(20) #for results to be recreated
N = 50 #number of samples to take from each population
a = [random.gauss(55,20) for x in range(N)] #take N samples from population A
b = [random.gauss(50,15) for x in range(N)] #take N samples from population B

# Using the seaborn library to generate a histogram of our 2 samples
import seaborn as sns
import matplotlib.pyplot as plt
sns.kdeplot(a, shade=True)
sns.kdeplot(b, shade=True)
plt.title("Independent Sample T-Test")
plt.show()

# Null Hypothesis: µa = µb (the means of both populations are equal)
# Alternate Hypothesis: µa ≠ µb (the means of both populations are not equal)
from scipy import stats
tStat, pValue = stats.ttest_ind(a, b, equal_var = False) #run independent sample T-Test; equal_var: we are specifying that the population does not have equal variance passing along False for the equal_var parameter. We know this because both samples were taken from populations with different standard deviations. Normally you wouldn’t know this is true and would have to run a Levene Test for Equal Variances
print("P-Value:{0} T-Statistic:{1}".format(pValue,tStat)) #print the P-Value and the T-Statistic
###P-Value:0.017485741540118758 T-Statistic:2.421942924642376

### conclusion
# there is enough evidence to reject the Null Hypothesis 
# as the P-Value is low (typically ≤ 0.05).