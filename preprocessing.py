import pandas as pd
import numpy as np
import datetime as dt

#################################### load data ####################################
# load CPI data
cpi_sg_data = pd.read_csv('CPI_SG.csv', header=9)
print(cpi_sg_data.head())

# load Income data
income_sg_data = pd.read_csv('Income_SG.csv', header=10)
print(income_sg_data.head())
print(income_sg_data.columns)

# load CPI US data
cpi_us_data = pd.read_excel('CPI_US.xlsx', header=11)
print(cpi_us_data.head())

# load food price US data
food_price_us_data = pd.read_excel('Food_Price_US.xlsx', header=11)
print(food_price_us_data.head())

# merge US food price and CPI data
merged_us_price_data = pd.merge(food_price_us_data, cpi_us_data, on=['Year', 'Period'], how='left')
merged_us_price_data = merged_us_price_data.rename(columns={'Value_x': 'Food_Index_US', 'Value_y': 'CPI_US'})
merged_us_price_data = merged_us_price_data[['Year', 'Period', 'Food_Index_US', 'CPI_US']]
print(merged_us_price_data.head())

# load Income US data
income_us_data = pd.read_excel('Income_US.xlsx')
print(income_us_data.head())

################################ preprocessing ####################################
################################ preprocess sg cpi data
cpi_sg_data_filtered = cpi_sg_data.loc[:, ['Data Series', 'All Items (Index)', 'All Items -> Food (Index)']]
# remove footnotes and filter to years 2000 to present
cpi_sg_data_filtered = cpi_sg_data_filtered.iloc[:309, :]
# change data series to datetime
cpi_sg_data_filtered['Data Series'] = pd.to_datetime(cpi_sg_data_filtered['Data Series'], format=' %Y %b')    

# check date differences between each subsequent row (to ensure monthly data)
# date_diff = cpi_data_filtered[['Data Series']]
# date_diff.loc[:, 'Data Series Shifted'] = date_diff.loc[:, 'Data Series'].shift(-1)
# date_diff['Date Difference'] = date_diff['Data Series'] - date_diff['Data Series Shifted']
# more_than_1_month_between_rows = date_diff.loc[date_diff['Date Difference'] > pd.Timedelta(days=31), :]
# less_than_1_month_between_rows = date_diff.loc[date_diff['Date Difference'] < pd.Timedelta(days=28), :]
# if not more_than_1_month_between_rows.empty:
#     print("Warning: There are gaps of more than 1 month between the following rows in CPI SG data:")
#     print(more_than_1_month_between_rows)
# elif not less_than_1_month_between_rows.empty:
#     print("Warning: There are gaps of less than 1 month between the following rows in CPI SG data:")
#     print(less_than_1_month_between_rows)
# else:
#     print("CPI SG data has consistent monthly intervals.")

# set date as index
cpi_sg_data_filtered = cpi_sg_data_filtered.rename(columns={'Data Series': 'date', 'All Items (Index)': 'CPI_SG', 'All Items -> Food (Index)': 'Food_Index_SG'})
# change base year to 2024-12 = 100
conversion_factor = cpi_sg_data_filtered.loc[cpi_sg_data_filtered['date'] == dt.datetime(2000, 12, 1), 'CPI_SG'].values[0] / 100
conversion_factor
cpi_sg_data_filtered['CPI_SG'] = cpi_sg_data_filtered['CPI_SG'] / conversion_factor
cpi_sg_data_filtered['Food_Index_SG'] = cpi_sg_data_filtered['Food_Index_SG'] / conversion_factor
print(cpi_sg_data_filtered.head(12))

################################ preprocess sg income data
income_sg_data_filtered = income_sg_data.loc[:, ['Data Series', 'Median Monthly Household Employment Income Per Household Member (Including Employer CPF Contributions) ']]
income_sg_data_filtered = income_sg_data_filtered.iloc[:25, :]
income_sg_data_filtered['Data Series'] = pd.to_datetime(income_sg_data_filtered['Data Series'], format=' %Y')
income_sg_data_filtered.columns = ['date', 'median_income_per_household_member_SG']
income_sg_data_filtered['income_index_SG'] = income_sg_data_filtered['median_income_per_household_member_SG'] / income_sg_data_filtered.loc[income_sg_data_filtered['date'] == dt.datetime(2000, 1, 1), 'median_income_per_household_member_SG'].values[0] * 100
print(income_sg_data_filtered.head())

# check date differences between each subsequent row (to ensure yearly data)
# date_diff_income = income_data_filtered[['Date']]
# date_diff_income.loc[:, 'Date Shifted'] = date_diff_income.loc[:, 'Date'].shift(-1)
# date_diff_income['Date Difference'] = date_diff_income['Date'] - date_diff_income['Date Shifted']
# more_than_1_year_between_rows = date_diff_income.loc[date_diff_income['Date Difference'] > pd.Timedelta(days=366), :]
# less_than_1_year_between_rows = date_diff_income.loc[date_diff_income['Date Difference'] < pd.Timedelta(days=364), :]
# if not more_than_1_year_between_rows.empty:
#     print("Warning: There are gaps of more than 1 year between the following rows in Income SG data:")
#     print(more_than_1_year_between_rows)
# elif not less_than_1_year_between_rows.empty:
#     print("Warning: There are gaps of less than 1 year between the following rows in Income SG data:")
#     print(less_than_1_year_between_rows)
# else:
#     print("Income SG data has consistent yearly intervals.")

################################ merge income_sg with cpi_sg
sg_data = pd.merge(cpi_sg_data_filtered, income_sg_data_filtered, on='date', how='left').bfill()
sg_data

################################ preprocess us cpi data
# filter to years 2000 to present
merged_us_price_data_filtered = merged_us_price_data.loc[merged_us_price_data['Year'] >= 2000, :].copy()
# merged_us_data_filtered['Period'].unique()
# remove periods that are not monthly data (i.e., S01, S02)
merged_us_price_data_filtered = merged_us_price_data_filtered.loc[merged_us_price_data_filtered['Period'].str.startswith('M'), :].copy()
# create date column and sort by date descending
merged_us_price_data_filtered['date'] = pd.to_datetime(merged_us_price_data['Year'].astype(str) + '-' + merged_us_price_data['Period'].str.slice(start=1).astype(str), format='%Y-%m')
merged_us_price_data_filtered = merged_us_price_data_filtered.drop(columns=['Year', 'Period']).sort_values(by='date', ascending=False)
# change base year to 2024-12 = 100
conversion_factor_us_cpi = merged_us_price_data_filtered.loc[merged_us_price_data_filtered['date'] == dt.datetime(2000, 12, 1), 'CPI_US'].values[0] / 100
merged_us_price_data_filtered['CPI_US'] = merged_us_price_data_filtered['CPI_US'] / conversion_factor_us_cpi
merged_us_price_data_filtered['Food_Index_US'] = merged_us_price_data_filtered['Food_Index_US'] / conversion_factor_us_cpi
print(merged_us_price_data_filtered.head(12))

# check date differences between each subsequent row (to ensure monthly data)
# date_diff_us = merged_us_data_filtered[['Date']]
# date_diff_us.loc[:, 'Date Shifted'] = date_diff_us.loc[:, 'Date'].shift(-1)
# date_diff_us['Date Difference'] = date_diff_us['Date'] - date_diff_us['Date Shifted']
# more_than_1_month_between_rows = date_diff_us.loc[date_diff_us['Date Difference'] > pd.Timedelta(days=31), :]
# less_than_1_month_between_rows = date_diff_us.loc[date_diff_us['Date Difference'] < pd.Timedelta(days=28), :]
# if not more_than_1_month_between_rows.empty:
#     print("Warning: There are gaps of more than 1 month between the following rows in CPI US data:")
#     print(more_than_1_month_between_rows)
# elif not less_than_1_month_between_rows.empty:
#     print("Warning: There are gaps of less than 1 month between the following rows in CPI US data:")
#     print(less_than_1_month_between_rows)
# else:
#     print("CPI US data has consistent monthly intervals.")

################################ preprocess us income data
income_us_data['date'] = pd.to_datetime(income_us_data['year'].astype(str), format='%Y')
income_us_data['median_income_per_household_member_US'] = income_us_data['median_income'] / income_us_data['average_size_of_household']
income_us_data['income_index_US'] = income_us_data['median_income_per_household_member_US'] / income_us_data.loc[income_us_data['year'] == 2000, 'median_income_per_household_member_US'].values[0] * 100
income_us_data_filtered = income_us_data.loc[:, ['date', 'median_income_per_household_member_US', 'income_index_US']]
print(income_us_data_filtered.head())

################################ merge income_us with cpi_us
us_data = pd.merge(merged_us_price_data_filtered, income_us_data_filtered, on='date', how='left').bfill()
us_data

################################ merge us and sg data
combined_data = pd.merge(sg_data, us_data, on='date', how='inner')
print(combined_data.head(24))

combined_data.to_csv('data.csv', index=False)