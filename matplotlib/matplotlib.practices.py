import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

### Basic plot
df = pd.read_excel("./sample-salesv3.xlsx")
print(df.head())

# summarize the data so we can see the total number of purchases and total sales for the top 10 customers. 
top_10 = (df.groupby('name')['ext price', 'quantity'].agg({'ext price': 'sum', 'quantity': 'count'})
          .sort_values(by='ext price', ascending=False))[:10].reset_index()
# rename the columns to be used in plots
top_10.rename(columns={'name': 'Name', 'ext price': 'Sales', 'quantity': 'Purchases'}, inplace=True)
print(top_10)

# plotting the table as a bar chart.
# choose a plotstyle
plt.style.use('ggplot')
# plot the data using the standard pandas plotting function
# which is a quick and easy way to prototype your visualization
top_10.plot(kind='barh', y="Sales", x="Name")
plt.show()

### customize the plot
# the Figure is the final image that may contain 1 or more axes. The Axes represent an individual plot.
# all of the customization will be done via "fig" and "ax" objects
# customize x limites, axis labels, adjust image size
def currency(x, pos):
    'The two args are the value and tick position'
    if x >= 1000000:
        return '${:1.1f}M'.format(x*1e-6)
    return '${:1.0f}K'.format(x*1e-3)
# Create the figure and the axes
fig, ax = plt.subplots(figsize=(5, 6))

# Plot the data and get the averaged
top_10.plot(kind='barh', y="Sales", x="Name", ax=ax)
avg = top_10['Sales'].mean()

# Set limits and labels
ax.set_xlim([-10000, 140000])
ax.set(title='2014 Revenue', xlabel='Total Revenue', ylabel='Customer')

# Add a line for the average
ax.axvline(x=avg, color='b', label='Average', linestyle='--', linewidth=1)

# Annotate the new customers
for cust in [3, 5, 8]:
    ax.text(115000, cust, "New Customer")

# Format the currency
formatter = FuncFormatter(currency)
ax.xaxis.set_major_formatter(formatter)

# Hide the legend
ax.legend().set_visible(False)
plt.show()


### Multi-plots
# axes get unpacked to ax0 and ax1 
# 1x2 plots
# sharey=Ture: yaxis will share the same labels
fig, (ax0, ax1) = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=(7, 4))
top_10.plot(kind='barh', y="Sales", x="Name", ax=ax0)
ax0.set_xlim([-10000, 140000])
ax0.set(title='Revenue', xlabel='Total Revenue', ylabel='Customers')

# Plot the average as a vertical line
avg = top_10['Sales'].mean()
ax0.axvline(x=avg, color='b', label='Average', linestyle='--', linewidth=1)

# Repeat for the unit plot
top_10.plot(kind='barh', y="Purchases", x="Name", ax=ax1)
avg = top_10['Purchases'].mean()
ax1.set(title='Units', xlabel='Total Units', ylabel='')
ax1.axvline(x=avg, color='b', label='Average', linestyle='--', linewidth=1)

# Title the figure
fig.suptitle('2014 Sales Analysis', fontsize=14, fontweight='bold');

# Hide the legends
ax1.legend().set_visible(False)
ax0.legend().set_visible(False)
plt.show()

# save plots
# Matplotlib supports many different formats for saving files. You can use fig.canvas.get_supported_filetypes() to see what your system supports:
fig.savefig('sales.png', transparent=False, dpi=80, bbox_inches="tight")