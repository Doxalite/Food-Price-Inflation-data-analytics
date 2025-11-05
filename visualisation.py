import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

def plot_cpi_food_index(data, year = 0):
    # filter data by number of years history
    data = data.iloc[-12*year:, :]
    x = data['date']

    cpi_food_index_fig, ax1 = plt.subplots()
    ax1.plot(x, data['CPI_SG'], label='CPI Singapore', color='red')
    ax1.plot(x, data['CPI_US'], label='CPI US', color='blue')
    ax1.plot(x, data['Food_Index_SG'], label='Food Index Singapore', color='red', linestyle='--')
    ax1.plot(x, data['Food_Index_US'], label='Food Index US', color='blue', linestyle='--')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Indexes')
    plt.gcf().autofmt_xdate()
    ax1.legend()
    ax1.set_title('CPI, Food Index Over Time')
    return cpi_food_index_fig

def plot_cpi_food_index_income_sg(data, year = 0):
    # filter data by number of years history
    data = data.iloc[-year*12:, :]
    x = data['date']
    cpi_food_index_income_sg_fig, ax2 = plt.subplots()
    ax2.plot(x, data['CPI_SG'], label='CPI Singapore', color='red')
    ax2.plot(x, data['Food_Index_SG'], label='Food Index Singapore', color='red', linestyle='--')
    ax2.plot(x, data['income_index_SG'], label='Income Singapore', color='green')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Indexes')
    # rotate x-axis labels to make them easier to read
    plt.gcf().autofmt_xdate()
    ax2.legend()
    ax2.set_title('CPI, Food Index and Income Over Time for Singapore')
    return cpi_food_index_income_sg_fig

def plot_cpi_food_index_income_us(data, year = 0):
    data = data.iloc[-year*12:, :]
    x = data['date']
    cpi_food_index_income_us_fig, ax3 = plt.subplots()
    ax3.plot(x, data['CPI_US'], label='CPI US', color='blue')
    ax3.plot(x, data['Food_Index_US'], label='Food Index US', color='blue', linestyle='--')
    ax3.plot(x, data['income_index_US'], label='Income US', color='green')
    ax3.set_xlabel('Date')
    ax3.set_ylabel('Indexes')
    ax3.legend()
    ax3.set_title('CPI, Food Index and Income Over Time for US')
    return cpi_food_index_income_us_fig

# plt.show()

# save plot to file
# cpi_food_index_fig.savefig('cpi_food_index.png')
# cpi_food_index_income_sg_fig.savefig('cpi_food_index_income_sg.png')
# cpi_food_index_income_us_fig.savefig('cpi_food_index_income_us.png')