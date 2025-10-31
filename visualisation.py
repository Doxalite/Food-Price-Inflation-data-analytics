import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

data = pd.read_csv('data.csv')
data.head()

data.sort_values(by='date', inplace=True, ascending=True)

# plot a time series
x = data['date']
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
ax1.plot(x, data['CPI_SG'], label='CPI Singapore', color='red')
ax1.plot(x, data['CPI_US'], label='CPI US', color='blue')
ax1.plot(x, data['Food_Index_SG'], label='Food Index Singapore', color='red', linestyle='--')
ax1.plot(x, data['Food_Index_US'], label='Food Index US', color='blue', linestyle='--')
ax1.set_xlabel('Date')
ax1.set_ylabel('Indexes')
ax1.legend()
ax1.set_title('CPI, Food Index Over Time')

ax2.plot(x, data['CPI_SG'], label='CPI Singapore', color='red')
ax2.plot(x, data['Food_Index_SG'], label='Food Index Singapore', color='red', linestyle='--')
ax2.plot(x, data['income_index_SG'], label='Income Singapore', color='green', linestyle=':')
ax2.set_xlabel('Date')
ax2.set_ylabel('Indexes')
ax2.legend()
ax2.set_title('CPI, Food Index and Income Over Time for Singapore')

ax3.plot(x, data['CPI_US'], label='CPI US', color='blue')
ax3.plot(x, data['Food_Index_US'], label='Food Index US', color='blue', linestyle='--')
ax3.plot(x, data['income_index_US'], label='Income US', color='green', linestyle=':')
ax3.set_xlabel('Date')
ax3.set_ylabel('Indexes')
ax3.legend()
ax3.set_title('CPI, Food Index and Income Over Time for US')

plt.show()