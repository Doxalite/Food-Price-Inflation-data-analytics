import pandas as pd
import numpy as np

if __name__ == "__main__":
    # load CPI data
    cpi_data = pd.read_csv('CPI_SG.csv', header=9)
    print(cpi_data.head())
    
    # load Income data
    income_data = pd.read_csv('Income_SG.csv', header=10)
    print(income_data.head())