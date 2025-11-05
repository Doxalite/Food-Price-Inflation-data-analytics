import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import itertools
import warnings

warnings.filterwarnings('ignore')

''' We want to fit an ARIMA model to predict 2026 CPI_SG data
'''


data = pd.read_csv('data.csv')
data.sort_values(by = 'date', ascending = True, inplace = True)
data = data.set_index('date')

CPI_SG = data.loc[: , ['CPI_SG']]
CPI_SG.plot(title = 'CPI_SG')
plt.show() # there is an increasing trend in CPI: differencing needed to make data stationary

# first order differencing
CPI_SG['CPI_SG_1'] = CPI_SG['CPI_SG'].diff()
CPI_SG_1 = CPI_SG['CPI_SG_1'].dropna()
CPI_SG_1.plot(title = '1st order differencing CPI_SG')
plt.show() # we see no meaningful trend, data seems to be stationary

# conduct stationarity test
result = adfuller(CPI_SG_1)
result # p value = 0.0423, we can conclude data is stationary at 95% confidence

# plot ACF to determine appropriate MA(q) value
plot_acf(CPI_SG_1)
plt.show() # idk looks like correlated even up to 25

# plot PACF to determine appropriate AR(p) value
plot_pacf(CPI_SG_1)
plt.show() # maybe 12?

p = range(4)
d = range(4)
q = range(4)
pdq = list(itertools.product(p, d, q))

best_aic = np.inf
best_model = None
best_order = None

for order in pdq:
    model = ARIMA(CPI_SG_1, order = order)
    result = model.fit(method_kwargs={"maxiter": 200})
    if result.aic < best_aic:
        best_aic = result.aic
        best_order = order
        best_model = model

print(f'Best Model order: {best_order}\nAIC:{best_aic}')

model = ARIMA(CPI_SG_1, order = best_order)
model_fit = model.fit(method_kwargs={"maxiter": 200})
model_fit.summary()
# Note 1: Using maxiter of 200 because at the default maxiter of 50, the model does not converge quick enough

# Note 2: Using ARIMA here may be inaccurate. This is because our data is monthly CPI data and has seasonality 
# throughout the year (every 12 data points). We check residual plot to see if there is any seasonal pattern 
# not captured by the model.
model_fit.resid.plot()
plt.show() # we can see there is no pattern, residuals are randomly dispersed around 0.


# If we can see that ARIMA isnt able to account for the seasonality of the data, we use SARIMAX to account for 
# the seasonality. In this case, SARIMAX is not needed
# p = range(4)
# d = range(4)
# q = range(4)
# pdq = list(itertools.product(p, d, q))

# best_aic = np.inf
# best_model = None
# best_order = None

# for order in pdq:
#     model = SARIMAX(CPI_SG_1, order = order, seasonal_order=(0,0,0,12))
#     result = model.fit(maxiter=200)
#     if result.aic < best_aic:
#         best_aic = result.aic
#         best_order = order
#         best_model = model

# print(f'Best Model order: {best_order}\nAIC:{best_aic}')

# model = SARIMAX(CPI_SG_1, order = best_order, seasonal_order = (0,0,0,12))
# model_fit = model.fit(maxiter=200)
# model_fit.summary()


# Finally, we predict 2026 CPI data
predictions_monthly_2026_differenced = model_fit.predict(start=len(CPI_SG_1), end=len(CPI_SG_1)+3+11)
predictions_monthly_2026_differenced
last_original_data = CPI_SG.iloc[-1, 0]
predictions_monthly_2026 = (predictions_monthly_2026_differenced.cumsum() + last_original_data).iloc[3:]
predictions_monthly_2026
prediction_2026 = predictions_monthly_2026.mean()
cpi_2025 = CPI_SG.iloc[-9:, 0].mean()
predicted_inflation_rate_2026 = round(((prediction_2026 - cpi_2025)/cpi_2025) * 100, 2)
print(f'2025 CPI up to Sept: {cpi_2025}')
print(f'2026 CPI prediction: {prediction_2026}\nwith 2000 as base year')
print(f'Predicted inflation rate: {predicted_inflation_rate_2026}%')

pd.DataFrame([prediction_2026, predicted_inflation_rate_2026], index=['CPI', 'Inflation Rate'], columns=['2026']).T.to_csv('prediction_2026.csv')