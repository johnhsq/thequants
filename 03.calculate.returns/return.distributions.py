from scipy.stats import bernoulli
import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline
plt.style.use('ggplot')


### generate an array of 0 or 1 with probability = 50%
# p=0.5
# bernoulli.rvs(p, size=num)	
###

##### simulate a stock possible return distribution after 6 months
###
# the stock has a mean monthly return of 1%. But there is dispersion around the mean: the actual returns of the stock each month are 1% + 2% = 3% or 1% - 2% = -1%, with equal probability. 
#     x = bernoulli.rvs(p, size=num_returns) # array with 0 or 1 with 50% probability
#     x = x - 0.5 # array with -0.5 or +0.5
#     x = x * 0.04 # array with -2% or +2%
#     x = 0.01+x # array with -1% or +3%
###
def generate_returns(num_returns):
    p = 0.5
    return 0.01 + (bernoulli.rvs(p, size=num_returns)-0.5)*0.04
print(generate_returns(6))  

###
# generate_returns(6) # generate an array with size 6 with value either -1% or 3%
# 100*np.prod(generate_returns(6)+1) # after 6 month, the possible value of $100 investment
# 100*np.prod(generate_returns(6)+1) for i in range(1,1000)] # generate an array of size 1000 of possible $100 investment values
# plt.hist(final_values, bins=20) # generate histogram of the 1000 data point distribution
###
final_values = [100*np.prod(generate_returns(6)+1) for i in range(1,1000)]
plt.hist(final_values, bins=20)
plt.ylabel('Frequency')
plt.xlabel('Value after 6 months')
plt.show()

# As you can see, the distribution gets less and less normal-looking over time. 
final_values = [100*np.prod(generate_returns(20)+1) for i in range(1,1000)]
plt.hist(final_values, bins=20)
plt.ylabel('Frequency')
plt.xlabel('Value after 20 months')
plt.show()

final_values = [100*np.prod(generate_returns(100)+1) for i in range(1,1000)]
plt.hist(final_values, bins=20)
plt.ylabel('Frequency')
plt.xlabel('Value after 100 months')
plt.show()