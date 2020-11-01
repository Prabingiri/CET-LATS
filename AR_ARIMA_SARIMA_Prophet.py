#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import matplotlib.pyplot as plt
from fbprophet import Prophet
import logging

logging.getLogger().setLevel(logging.ERROR)


# In[2]:


# a function that take the data out of the whole dataset based on the given lat & lon
def dataExtractor(lat, lon):
    data = pd.read_csv("myRes.csv")
    column_names = data.columns
    dates = column_names[3:]
    
    temp_df = pd.DataFrame(columns=['date', 'temp'])
    temp_df['date'] = dates
    temp_df['date'] = pd.to_datetime(temp_df['date'])
    temperature = data[(data['LAT'] == lat) & (data['LON'] == lon)]
    temperature_value = temperature.iloc[0, 3:].values
    temp_df['temp'] = temperature_value
    temp_df = temp_df.rename(columns={'date': 'ds', 'temp': 'y'})
    return temp_df


# # Prophet Model

# In[3]:


def prophet_model(lat, lon, prediction_time_window):
    temp_df = dataExtractor(lat, lon)
    
    # Split the data to train and test data
    # i.e. Take data of the 11 months as training data and last month as the test data
    prediction_size = prediction_time_window
    train_data = temp_df[:-prediction_size]
    test_data = temp_df[-prediction_size:]
    model = Prophet()
    model.fit(train_data)
    future = model.make_future_dataframe(periods=prediction_size)
    forecast = model.predict(future)
    model.plot(forecast)
    t = model.plot_components(forecast)
    
    def make_comparison_dataframe(historical, forecast):
        return forecast.set_index('ds')[['yhat', 'yhat_lower', 'yhat_upper']].join(historical.set_index('ds'))
    
    comparison_dataframe = make_comparison_dataframe(temp_df, forecast)
    
    axis_font = {'fontname':'Arial', 'size':'14'}
    plt.figure(figsize=(14, 8))
    plt.plot(comparison_dataframe['yhat'], label='Predicted value')
    plt.plot(comparison_dataframe['yhat_lower'], label='Lower bound prediction')
    plt.plot(comparison_dataframe['yhat_upper'], label='Upper bound prediction')
    plt.plot(comparison_dataframe['y'], label='Actual temperature', )
    plt.xlabel('Date', fontsize=25)
    plt.ylabel('Temperature', fontsize=25)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=25)
    plt.legend(fontsize=25)
    plt.tight_layout()
    plt.savefig('Comparison.png', dpi=600)
    plt.show()


# In[4]:


lat = 78.250
lon = 22.817
prophet_model(lat, lon, 30)


# # AutoRegression (AR) Model

# In[5]:


from statsmodels.tsa.ar_model import AutoReg
from sklearn.metrics import mean_squared_error
from math import sqrt

def AR_model(lat, lon, prediction_time_window):
    # load dataset
    temp_df = dataExtractor(lat, lon)
    
    # Date time temperature has two columns. The first column is the dates (01-01-2019 to 30-12-2019) and the second column
    # is the temperature. All these data are from one station.
    series = temp_df.set_index(['ds']).squeeze()
    # split dataset
    X = series.values
    
    train, test = X[1:len(X) - prediction_time_window], X[len(X) - prediction_time_window:]
    # train autoregression
    model = AutoReg(train, lags=prediction_time_window)
    model_fit = model.fit()
    print('Coefficients: %s' % model_fit.params)
    # make predictions
    predictions = model_fit.predict(start=len(train), end=len(train)+len(test)-1, dynamic=False)
    for i in range(len(predictions)):
        print('predicted=%f, expected=%f' % (predictions[i], test[i]))
    rmse = sqrt(mean_squared_error(test, predictions))
    print('Test RMSE: %.3f' % rmse)
    # plot results
    plt.plot(test, label='Test data')
    plt.plot(predictions, color='red', label='Predicted values')
    plt.ylabel('Temperature')
    plt.xlabel('Number of days in future')
    plt.legend()
    plt.show()


# In[6]:


lat = 78.250
lon = 22.817
AR_model(lat, lon, 90)


# # ARIMA Model

# In[7]:


from statsmodels.tsa.arima_model import ARIMA


# In[8]:


def ARIMA_model(lat, lon, prediction_time_window):
    # load dataset
    temp_df = dataExtractor(lat, lon)
    series = temp_df.set_index(['ds']).squeeze()
    X = series.values
    train, test = X[: len(X) - prediction_time_window], X[len(X) - prediction_time_window:]
    history = [x for x in train]
    predictions = list()
    for t in range(len(test)):
        model = ARIMA(history, order=(5,1,0))
        model_fit = model.fit(disp=0)
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)
        print('predicted=%f, expected=%f' % (yhat, obs))
    error = mean_squared_error(test, predictions)
    print('Test MSE: %.3f' % error)
    # plot
    plt.plot(test)
    plt.plot(predictions, color='red')
    plt.show()


# In[9]:


lat = 78.250
lon = 22.817
ARIMA_model(lat, lon, 90)


# # SARIMA Model

# Seasonal ARIMA model.

# In[10]:


temp_df = dataExtractor(lat, lon)
print(temp_df)
series = temp_df.set_index(['ds']).squeeze()
print(series)
X = series.values
X


# In[25]:


def SARIMA(lat, lon, prediction_time_window):
    temp_df = dataExtractor(lat, lon)
    series = temp_df.set_index(['ds']).squeeze()
    X = series.values
    model = sm.tsa.statespace.SARIMAX(series,
                                order=(0, 0, 1),
                                seasonal_order=(1, 1, 1, 12),
                                enforce_stationarity=False,
                                enforce_invertibility=False)
    results = model.fit()
    print(results.summary().tables[1])
    results.plot_diagnostics(figsize=(18, 8))
    plt.show()
    
    pred = results.get_prediction(start=series.index[-1] + pd.DateOffset(-1 * prediction_time_window), dynamic=False)
    pred_ci = pred.conf_int()
    ax = series['2019-':].plot(label='observed')
    pred.predicted_mean.plot(ax=ax, label='Forecast', alpha=.7)
    ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.2)
    ax.set_xlabel('Date')
    ax.set_ylabel('Temperature')
    plt.legend()
    plt.title('Forecasting Using SARIMA')
    plt.tight_layout()
    plt.savefig('SARIMA.png', dpi=600)
    plt.show()
    
    y_forecasted = pred.predicted_mean
    y_truth = series['2019-12-01':]
    mse = ((y_forecasted - y_truth) ** 2).mean()
    print('The Mean Squared Error is {}'.format(round(mse, 2)))
    print('The Root Mean Squared Error is {}'.format(round(np.sqrt(mse), 2)))


# In[26]:


lat = 78.250
lon = 22.817
SARIMA(lat, lon, 30)


# In[ ]:




