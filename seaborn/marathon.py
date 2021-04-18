import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from datetime import timedelta

sns.set()

data = pd.read_csv('marathon-data.csv')
print(data.head())

# Pandas loads the time columns as Python strings by default
# convert it to time
def convert_time(s):
    h, m, s = map(int, s.split(':'))
    return timedelta(hours=h, minutes=m, seconds=s)

data = pd.read_csv('marathon-data.csv', converters={'split':convert_time, 'final':convert_time})
print(data.head())
print(data.dtypes)

# add columns that give the times in seconds
data['split_sec'] = data['split'].astype(int) / 1E9
data['final_sec'] = data['final'].astype(int) / 1E9

#  get an idea of what the data looks like, we can plot a jointplot over the data:
with sns.axes_style('white'):
    g = sns.jointplot("split_sec", "final_sec", data, kind='hex')
    g.ax_joint.plot(np.linspace(4000, 16000),
                    np.linspace(8000, 32000), ':k')
# The dotted line shows where someone's time would lie if they ran the marathon at a perfectly steady pace.
# The distribution lies above this indicates that most people slow down over the course of the marathon, called "positive split"
# The opposite called "negative split"
plt.show()

# the split fraction, which measures the degree to which each runner negative-splits or positive-splits the race
data['split_frac'] = 1 - 2 * data['split_sec'] / data['final_sec']
# Let's do a distribution plot of this split fraction:
sns.distplot(data['split_frac'], kde=False)
plt.axvline(0, color="k", linestyle="--")
plt.show()

# Out of nearly 40,000 participants, there were only 250 people who negative-split their marathon.
print(sum(data.split_frac < 0))


### Let's see whether there is any correlation between this split fraction and other variables. 
# We'll do this using a pairgrid, which draws plots of all these correlations:
g = sns.PairGrid(data, vars=['age', 'split_sec', 'final_sec', 'split_frac'],
                 hue='gender', palette='RdBu_r')
g.map(plt.scatter, alpha=0.8)
g.add_legend()
plt.show()
# It looks like the split fraction does not correlate particularly with age, 
# but does correlate with the final time: faster runners tend to have closer to even splits on their marathon time


# The difference between men and women here is interesting. Let's look at the histogram of split fractions for these two groups:
sns.kdeplot(data.split_frac[data.gender=='M'], label='men', shade=True)
sns.kdeplot(data.split_frac[data.gender=='W'], label='women', shade=True)
plt.xlabel('split_frac')
plt.show()
# The interesting thing here is that there are many more men than women who are running close to an even split!

# A nice way to compare distributions is to use a violin plot
sns.violinplot("gender", "split_frac", data=data,
               palette=["lightblue", "lightpink"])
plt.show()

# Let's look a little deeper, and compare these violin plots as a function of age. 
# We'll start by creating a new column in the array that specifies the decade of age that each person is in:
data['age_dec'] = data.age.map(lambda age: 10 * (age // 10))
print(data.head())
men = (data.gender == 'M')
women = (data.gender == 'W')

with sns.axes_style(style=None):
    sns.violinplot("age_dec", "split_frac", hue="gender", data=data,
                   split=True, inner="quartile",
                   palette=["lightblue", "lightpink"])
plt.show()


# to the men with negative splits: who are these runners? Does this split fraction correlate with finishing quickly? We can plot this very easily. We'll use regplot, which will automatically fit a linear regression to the data:
g = sns.lmplot('final_sec', 'split_frac', col='gender', data=data,
               markers=".", scatter_kws=dict(color='c'))
g.map(plt.axhline, y=0.1, color="k", ls=":")
plt.show()

