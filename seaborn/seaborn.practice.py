import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

plt.style.use('classic')

# Create some data
rng = np.random.RandomState(0)
x = np.linspace(0, 10, 500)
y = np.cumsum(rng.randn(500, 6), 0)

### simply comparison between Matplotlib and Seaborn
# Plot the data with Matplotlib defaults
plt.plot(x, y)
plt.legend('ABCDEF', ncol=2, loc='upper left')
plt.show()

### Seaborn approach
# set default style
# it can also overwrite Matplotlib's default parameters 
# and in turn get even simple Matplotlib scripts to produce vastly superior output. 
sns.set()
# same plotting code as above!
plt.plot(x, y)
plt.legend('ABCDEF', ncol=2, loc='upper left')
plt.show()


### plot histograms and joint distributions of variables.
data = np.random.multivariate_normal([0, 0], [[5, 2], [2, 2]], size=2000)
data = pd.DataFrame(data, columns=['x', 'y'])

for col in 'xy':
    plt.hist(data[col], density=True, alpha=0.5)
plt.show()

# Rather than a histogram, we can get a smooth estimate of the distribution using a kernel density estimation
for col in 'xy':
    sns.kdeplot(data[col], shade=True)
plt.show()

# combine Histograms and KDE
sns.distplot(data['x'])
sns.distplot(data['y'])
plt.show()

# If we pass the full two-dimensional dataset to kdeplot, we will get a two-dimensional visualization of the data:
sns.kdeplot(data['x'],data['y'])
plt.show()

# We can see the joint distribution and the marginal distributions together using sns.jointplot. For this plot, we'll set the style to a white background:
with sns.axes_style('white'):
    sns.jointplot("x", "y", data, kind='kde')
plt.show()

# use a hexagonally based histogram instead:
with sns.axes_style('white'):
    sns.jointplot("x", "y", data, kind='hex')
plt.show()

### Use Pairplots to explore correlations between multidimensional data
iris = sns.load_dataset("iris")
print(iris.head())
sns.pairplot(iris,hue='species', height=2.5)
plt.show()


### Faceted histograms
# histograms of subsets of data
# the following example shows histograms by "Sex", "Time:Lunch or Dinner"
# Seaborn's FacetGrid makes this extremely simple
tips = sns.load_dataset('tips')
print(tips.head())
tips['tip_pct'] = 100 * tips['tip'] / tips['total_bill']

grid = sns.FacetGrid(tips, row="sex", col="time", margin_titles=True)
grid.map(plt.hist, "tip_pct", bins=np.linspace(0, 40, 15))
plt.show()


### Factor plots
# Factor plots can be useful for this kind of visualization as well. This allows you to view the distribution of a parameter within bins defined by any other parameter:
with sns.axes_style(style='ticks'):
    g = sns.catplot("day", "total_bill", "sex", data=tips, kind="box")
    g.set_axis_labels("Day", "Total Bill")
plt.show()


### Joint distributions
# show the joint distribution between different datasets, along with the associated marginal distributions:
with sns.axes_style('white'):
    sns.jointplot("total_bill", "tip", data=tips, kind='hex')
plt.show()

# The joint plot can even do some automatic kernel density estimation and regression:
sns.jointplot("total_bill", "tip", data=tips, kind='reg');
plt.show()


### Bar plots
# Time series can be plotted using sns.factorplot. In the following example, we'll use the Planets data that we first saw in Aggregation and Grouping:
planets = sns.load_dataset('planets')
print(planets.head())
with sns.axes_style('white'):
    g = sns.catplot("year", data=planets, aspect=2,
                       kind="count", color='steelblue')
    g.set_xticklabels(step=5)
plt.show()

# We can learn more by looking at the "method" of discovery of each of these planets:
with sns.axes_style('white'):
    g = sns.catplot("year", data=planets, aspect=4.0, kind='count',
                       hue='method', order=range(2001, 2015))
    g.set_ylabels('Number of Planets Discovered')
plt.show()
