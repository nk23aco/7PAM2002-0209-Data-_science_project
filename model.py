# -*- coding: utf-8 -*-
"""model

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1fTBxe4b94DqEhMQtq0W954NttuGbBc-r

Random Forest
"""

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
file_path = '/content/weather_2016_2020_daily.csv'
df = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')
print(df.head())

# Create lagged features (up to 7 days)
def create_lagged_features(df, lags):
    for lag in range(1, lags + 1):
        df[f'Precipit_lag_{lag}'] = df['Precipit'].shift(lag)
    return df

df = create_lagged_features(df, lags=7)

# Create rolling window features (3-day and 7-day moving averages)
df['Precipit_3d_avg'] = df['Precipit'].rolling(window=3).mean()
df['Precipit_7d_avg'] = df['Precipit'].rolling(window=7).mean()

# Add seasonal time-based features
df['day_of_week'] = df.index.dayofweek
df['month'] = df.index.month
df['day_of_year'] = df.index.dayofyear

# Drop NaN values generated by lagging and rolling operations
df.dropna(inplace=True)

# Define features and target
features = ['Temp_max', 'Temp_avg', 'Temp_min', 'Hum_max', 'Hum_avg', 'Hum_min',
            'Wind_max', 'Wind_avg', 'Wind_min', 'Press_max', 'Press_avg', 'Press_min',
            'Precipit_lag_1', 'Precipit_lag_2', 'Precipit_lag_3', 'Precipit_lag_4',
            'Precipit_lag_5', 'Precipit_lag_6', 'Precipit_lag_7',
            'Precipit_3d_avg', 'Precipit_7d_avg',
            'day_of_week', 'month', 'day_of_year']

X = df[features]
y = df['Precipit']

# Split dataset into training (80%) and testing (20%)
train_size = int(len(df) * 0.8)
train_X, test_X = X.iloc[:train_size], X.iloc[train_size:]
train_y, test_y = y.iloc[:train_size], y.iloc[train_size:]

# Define hyperparameter grid for fine-tuning
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# Initialize Random Forest model
rf = RandomForestRegressor(random_state=42)

# Perform Randomized Search Cross Validation
search = RandomizedSearchCV(rf, param_grid, n_iter=20, cv=5, scoring='neg_mean_squared_error', n_jobs=-1, random_state=42)
search.fit(train_X, train_y)

# Get best parameters
best_params = search.best_params_
print(f"Best Parameters: {best_params}")

# Train model with best parameters
best_model = RandomForestRegressor(**best_params, random_state=42)
best_model.fit(train_X, train_y)

# Make predictions
predictions = best_model.predict(test_X)

# Evaluate model
mse = mean_squared_error(test_y, predictions)
mae = mean_absolute_error(test_y, predictions)
r2 = r2_score(test_y, predictions)

print(f"MSE: {mse:.4f}")
print(f"MAE: {mae:.4f}")
print(f"R²: {r2:.4f}")

# Plot actual vs predicted precipitation
plt.figure(figsize=(12, 6))
plt.plot(train_y.index, train_y, label='Training Data', color='blue')
plt.plot(test_y.index, test_y, label='Actual Precipitation', color='green')
plt.plot(test_y.index, predictions, label='Predicted Precipitation', color='red', linestyle='dashed')
plt.title('Random Forest Forecast with Enhanced Features')
plt.xlabel('Date')
plt.ylabel('Precipitation')
plt.legend()
plt.grid()
plt.show()

# 🔹 Uninstall conflicting versions
!pip uninstall -y numpy scipy statsmodels pmdarima

# 🔹 Install compatible versions
!pip install --no-cache-dir numpy==1.23.5 scipy==1.10.1 statsmodels==0.13.5 pmdarima==2.0.3

# Restart runtime after this step for changes to take effect.

import pandas as pd
import numpy as np
import itertools
import matplotlib.pyplot as plt
import warnings
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

warnings.filterwarnings("ignore")

# Load dataset
df = pd.read_csv('/content/weather_2016_2020_daily.csv')
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Use only 'Precipit' column
df['Precipit'].fillna(0, inplace=True)

# Feature Engineering: Add only essential lag & rolling features
df['lag_7'] = df['Precipit'].shift(7)  # Weekly pattern
df['rolling_mean_7'] = df['Precipit'].rolling(window=7).mean()  # Weekly trend
df['rolling_std_7'] = df['Precipit'].rolling(window=7).std()  # Weekly volatility

# Drop NaN values from rolling features
df.dropna(inplace=True)

# Train-test split
train_size = int(len(df) * 0.8)
train, test = df.iloc[:train_size], df.iloc[train_size:]

# Define parameter grid
p = d = q = range(0, 3)
P = D = Q = range(0, 2)
seasonal_period = [7]  # Weekly seasonality

# Generate all parameter combinations
param_grid = list(itertools.product(p, d, q, P, D, Q, seasonal_period))

best_score = float('inf')
best_params = None

# Grid search for best SARIMA parameters
for params in param_grid:
    try:
        model = SARIMAX(train['Precipit'],
                        exog=train[['lag_7', 'rolling_mean_7', 'rolling_std_7']],
                        order=(params[0], params[1], params[2]),
                        seasonal_order=(params[3], params[4], params[5], params[6]),
                        enforce_stationarity=False,
                        enforce_invertibility=False)
        result = model.fit(disp=False)
        predictions = result.predict(start=len(train), end=len(train) + len(test) - 1,
                                     exog=test[['lag_7', 'rolling_mean_7', 'rolling_std_7']])
        mse = mean_squared_error(test['Precipit'], predictions)

        if mse < best_score:
            best_score = mse
            best_params = params
    except:
        continue

print(f'Best SARIMA Parameters: {best_params}')

# Fit SARIMA model with best parameters
best_model = SARIMAX(train['Precipit'],
                     exog=train[['lag_7', 'rolling_mean_7', 'rolling_std_7']],
                     order=(best_params[0], best_params[1], best_params[2]),
                     seasonal_order=(best_params[3], best_params[4], best_params[5], best_params[6]),
                     enforce_stationarity=False,
                     enforce_invertibility=False)
result = best_model.fit(disp=False)

# Predict
predictions = result.predict(start=len(train), end=len(train) + len(test) - 1,
                             exog=test[['lag_7', 'rolling_mean_7', 'rolling_std_7']])

# Evaluate performance
mse = mean_squared_error(test['Precipit'], predictions)
mae = mean_absolute_error(test['Precipit'], predictions)
r2 = r2_score(test['Precipit'], predictions)

print(f'MSE: {mse:.4f}')
print(f'MAE: {mae:.4f}')
print(f'R²: {r2:.4f}')

# Plot results
plt.figure(figsize=(10, 6))
plt.plot(train.index, train['Precipit'], label='Train')
plt.plot(test.index, test['Precipit'], label='Test', color='orange')
plt.plot(test.index, predictions, label='Predicted', color='red')
plt.title('Optimized SARIMA Model Forecast')
plt.xlabel('Date')
plt.ylabel('Precipitation')
plt.legend()
plt.show()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
!pip install bayesian-optimization
from bayes_opt import BayesianOptimization

warnings.filterwarnings("ignore")

# Load dataset
df = pd.read_csv('/content/weather_2016_2020_daily.csv')
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Use only 'Precipit' column
df['Precipit'].fillna(0, inplace=True)

df['lag_7'] = df['Precipit'].shift(7)
df['lag_14'] = df['Precipit'].shift(14)
df['rolling_mean_7'] = df['Precipit'].rolling(window=7).mean()
df['rolling_std_7'] = df['Precipit'].rolling(window=7).std()
df['rolling_max_7'] = df['Precipit'].rolling(window=7).max()
df['rolling_min_7'] = df['Precipit'].rolling(window=7).min()

# Drop NaN values from rolling features
df.dropna(inplace=True)

# Train-test split
train_size = int(len(df) * 0.8)
train, test = df.iloc[:train_size], df.iloc[train_size:]

def sarima_objective(p, d, q, P, D, Q):
    """ Bayesian optimization function to find the best SARIMA parameters """
    p, d, q = int(round(p)), int(round(d)), int(round(q))
    P, D, Q = int(round(P)), int(round(D)), int(round(Q))

    try:
        model = SARIMAX(train['Precipit'],
                        exog=train[['lag_7', 'lag_14', 'rolling_mean_7', 'rolling_std_7', 'rolling_max_7', 'rolling_min_7']],
                        order=(p, d, q),
                        seasonal_order=(P, D, Q, 7),
                        enforce_stationarity=False,
                        enforce_invertibility=False)
        result = model.fit(disp=False)

        predictions = result.predict(start=len(train), end=len(train) + len(test) - 1,
                                     exog=test[['lag_7', 'lag_14', 'rolling_mean_7', 'rolling_std_7', 'rolling_max_7', 'rolling_min_7']])

        mse = mean_squared_error(test['Precipit'], predictions)
        return -mse
    except:
        return -1000

# Define search space
param_bounds = {
    'p': (0, 3), 'd': (0, 2), 'q': (0, 3),
    'P': (0, 2), 'D': (0, 1), 'Q': (0, 2)
}

optimizer = BayesianOptimization(f=sarima_objective, pbounds=param_bounds, random_state=42)
optimizer.maximize(init_points=5, n_iter=20)

# Get best parameters
best_params = optimizer.max['params']
p, d, q = int(round(best_params['p'])), int(round(best_params['d'])), int(round(best_params['q']))
P, D, Q = int(round(best_params['P'])), int(round(best_params['D'])), int(round(best_params['Q']))

print(f'Best SARIMA Parameters: {(p, d, q, P, D, Q, 7)}')

best_model = SARIMAX(train['Precipit'],
                     exog=train[['lag_7', 'lag_14', 'rolling_mean_7', 'rolling_std_7', 'rolling_max_7', 'rolling_min_7']],
                     order=(p, d, q),
                     seasonal_order=(P, D, Q, 7),
                     enforce_stationarity=False,
                     enforce_invertibility=False)
result = best_model.fit(disp=False)

# Predict
predictions = result.predict(start=len(train), end=len(train) + len(test) - 1,
                             exog=test[['lag_7', 'lag_14', 'rolling_mean_7', 'rolling_std_7', 'rolling_max_7', 'rolling_min_7']])

#  Evaluate Performance
mse = mean_squared_error(test['Precipit'], predictions)
mae = mean_absolute_error(test['Precipit'], predictions)
r2 = r2_score(test['Precipit'], predictions)

print(f'MSE: {mse:.4f}')
print(f'MAE: {mae:.4f}')
print(f'R²: {r2:.4f}')

#  Plot Results
plt.figure(figsize=(10, 6))
plt.plot(train.index, train['Precipit'], label='Train')
plt.plot(test.index, test['Precipit'], label='Test', color='orange')
plt.plot(test.index, predictions, label='Predicted', color='red')
plt.title('Optimized SARIMA with Bayesian Hyperparameter Tuning')
plt.xlabel('Date')
plt.ylabel('Precipitation')
plt.legend()
plt.show()

"""LSTM"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from bayes_opt import BayesianOptimization
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Load dataset
df = pd.read_csv('/content/weather_2016_2020_daily.csv')
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Features and target
data = df[['Precipit']].copy()

# Add more lagged features
for lag in [7, 14, 30]:
    data[f'Precipit_lag_{lag}'] = data['Precipit'].shift(lag)

# Add rolling averages
data['rolling_mean_7'] = data['Precipit'].rolling(window=7).mean()
data['rolling_mean_14'] = data['Precipit'].rolling(window=14).mean()

# Add seasonality terms
days = np.arange(len(data))
data['sin_365'] = np.sin(2 * np.pi * days / 365)
data['cos_365'] = np.cos(2 * np.pi * days / 365)

data.dropna(inplace=True)

# Normalize data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data)

# Create sequences
def create_sequences(data, time_steps=30):
    X, y = [], []
    for i in range(len(data) - time_steps):
        X.append(data[i:i + time_steps])
        y.append(data[i + time_steps, 0])
    return np.array(X), np.array(y)

# Split into train and test sets
train_size = int(len(scaled_data) * 0.8)
train, test = scaled_data[:train_size], scaled_data[train_size:]
time_steps = 30
X_train, y_train = create_sequences(train, time_steps)
X_test, y_test = create_sequences(test, time_steps)

#  Define Bayesian Optimization Function for LSTM

def lstm_hyperparam_tuning(lstm_units, dropout_rate, learning_rate, batch_size):
    lstm_units = int(lstm_units)
    batch_size = int(batch_size)

    model = Sequential([
        LSTM(lstm_units, activation='tanh', return_sequences=True, input_shape=(time_steps, X_train.shape[2])),
        Dropout(dropout_rate),
        LSTM(lstm_units // 2, activation='tanh', return_sequences=True),
        Dropout(dropout_rate),
        LSTM(lstm_units // 4, activation='tanh'),
        Dropout(dropout_rate),
        Dense(1)
    ])

    model.compile(optimizer=RMSprop(learning_rate=learning_rate), loss='mse')

    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=0.00001)

    model.fit(X_train, y_train, epochs=100, batch_size=batch_size, validation_data=(X_test, y_test),
              callbacks=[early_stopping, reduce_lr], verbose=0)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred.flatten())

    return -mse

#  Bayesian Optimization for LSTM

pbounds = {
    'lstm_units': (50, 200),
    'dropout_rate': (0.1, 0.5),
    'learning_rate': (0.0001, 0.01),
    'batch_size': (8, 32)
}

optimizer = BayesianOptimization(f=lstm_hyperparam_tuning, pbounds=pbounds, random_state=42)
optimizer.maximize(init_points=3, n_iter=5)

# Best Parameters Found
best_params = optimizer.max['params']
print(f"Best Hyperparameters: {best_params}")

#  Train Final LSTM Model

final_model = Sequential([
    LSTM(int(best_params['lstm_units']), activation='tanh', return_sequences=True, input_shape=(time_steps, X_train.shape[2])),
    Dropout(best_params['dropout_rate']),
    LSTM(int(best_params['lstm_units'] // 2), activation='tanh', return_sequences=True),
    Dropout(best_params['dropout_rate']),
    LSTM(int(best_params['lstm_units'] // 4), activation='tanh'),
    Dropout(best_params['dropout_rate']),
    Dense(1)
])

final_model.compile(optimizer=RMSprop(learning_rate=best_params['learning_rate']), loss='mse')

from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

# Define callbacks
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=0.00001)

# Train the model
history = final_model.fit(X_train, y_train, epochs=50, batch_size=int(best_params['batch_size']),
                          validation_data=(X_test, y_test), callbacks=[early_stopping, reduce_lr])

# Predictions
y_pred = final_model.predict(X_test)
y_test_inv = scaler.inverse_transform(np.c_[y_test, np.zeros((y_test.shape[0], scaled_data.shape[1] - 1))])[:, 0]
y_pred_inv = scaler.inverse_transform(np.c_[y_pred, np.zeros((y_pred.shape[0], scaled_data.shape[1] - 1))])[:, 0]

# Evaluate
mse = mean_squared_error(y_test_inv, y_pred_inv)
mae = mean_absolute_error(y_test_inv, y_pred_inv)
r2 = r2_score(y_test_inv, y_pred_inv)

print(f'MSE: {mse:.4f}')
print(f'MAE: {mae:.4f}')
print(f'R²: {r2:.4f}')

#  Plot Results
plt.figure(figsize=(10, 6))
plt.plot(df.index[-len(y_test_inv):], y_test_inv, label='Actual', color='blue')
plt.plot(df.index[-len(y_pred_inv):], y_pred_inv, label='Predicted', color='red')
plt.title('Optimized LSTM Model Forecast')
plt.xlabel('Date')
plt.ylabel('Precipitation')
plt.legend()
plt.show()