import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


df = pd.read_excel('/Users/linpel/Desktop/Job/python/Data/1year from 2022.08.30.xlsx', index_col=0)
data = df['Balance at the end of a day']
df.index = pd.to_datetime(df.index)

log_returns = np.log(1+data.pct_change().dropna())

u = log_returns.mean()
var = log_returns.var()
drift = u - (0.5 * var)
stdev = log_returns.std()
norm.ppf(0.95)

t_intervals = 6 * 365 + 1
iterations = 10000

daily_change = np.exp(np.array(drift) + np.array(stdev) * norm.ppf(np.random.rand(t_intervals, iterations)))

S0 = data.iloc[-1]
acc_list = np.zeros_like(daily_change)
acc_list[0] = S0

for t in range(1, t_intervals):
    acc_list[t] = acc_list[t - 1] * daily_change[t]

clients_acc = pd.DataFrame(acc_list)

investing_years = [1, 2, 3, 4, 5, 6]
portfolio_values = []
per_5 = []
per_95 = []

for i in investing_years:
    days = i * 365
    portfolio = round(clients_acc[:days], 2)
    portfolio_values.append(round(np.mean(portfolio), 2))
    per_5.append(round(np.percentile(portfolio, 5), 2))
    per_95.append(round(np.percentile(portfolio, 1), 2))
    print(f"Expected clients\' accounts portfolio (Year {i}):", f'{round(np.mean(portfolio), 2):,}'.replace(',', ' '))

allocation_df = pd.DataFrame()

investing_years = [1, 2, 3, 4, 5, 6]
allocation_df['year'] = investing_years

percentiles = [1, 2.5, 5, 10, 25]

for y in percentiles:
    allocations = []
    for i in investing_years:
        days = i * 365
        investing_sum = round(np.percentile(clients_acc.iloc[days], y), 2)
        allocations.append(int(investing_sum))
    allocation_df[y] = allocations

clients_accc = clients_acc.values

print(allocation_df)

allocation_df.set_index('year', inplace=True)

# Plotting the simulations by year
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
fig.suptitle('Monte Carlo Simulation')

for col in allocation_df.columns:
    ax1.plot(allocation_df.index, np.abs(allocation_df[col]), label=f'{100-col}%')

ax1.ticklabel_format(style='plain')
ax1.set_xlabel('Year')
ax1.set_ylabel('Balance')
ax1.set_title('Monte Carlo Simulation by Year')
ax1.legend(title='Percentile', loc='upper left')

# Plotting the simulations by day
for i in range(clients_acc.shape[1]):
    ax2.plot(np.abs(clients_accc[:, i]), linewidth=0.5, alpha=0.5)
ax2.ticklabel_format(style='plain')
ax2.set_xlabel('Day')
ax2.set_ylabel('Balance')
ax2.set_title('Monte Carlo Simulation by Day')

plt.tight_layout()
plt.show()




plt.figure(figsize=(15, 8))
plt.plot(investing_years, portfolio_values, marker='o', linestyle='-', label='Mean Portfolio')
plt.title('Expected Clients\' Accounts Portfolio Over Time')
plt.xlabel('Investing Years')
plt.ylabel('Portfolio Value')
plt.grid(True)

# Function to format Y-axis labels with zeros and space as the thousands separator
def format_y_axis_labels(value, pos):
    return f'{value:,.0f}'.replace(',', '')

# Apply the custom Y-axis label formatting function
plt.gca().yaxis.set_major_formatter(FuncFormatter(format_y_axis_labels))

for i, value in enumerate(portfolio_values):
    plt.annotate(f'{value:,.0f}'.replace(',', ''), (investing_years[i], value), textcoords="offset points", xytext=(0,10), ha='center')

# Your code for plotting acc_list
plt.figure(figsize=(10, 6))
plt.plot(acc_list)

# Show the plots
plt.show()