# 7PAM2002-0209-Data-_science_project

Project Overview
This project aims to forecast daily precipitation using a combination of traditional time-series  and AI techniques.A multivariate weather dataset (2016–2020) was used, incorporating features like temperature, humidity, wind, and atmospheric pressure. Forecasting performance was evaluated using Mean Squared Error (MSE), Mean Absolute Error (MAE), and R² score.

The models compared are:
SARIMAX (Statistical Model)
Random Forest Regressor (Machine Learning)
Stacking Regressor (Ensemble Machine Learning)
LSTM Neural Network (Deep Learning)

Research Questions

Can deep learning techniques outperform traditional and machine learning models for precipitation forecasting?
How do traditional, machine learning, and deep learning models capture temporal patterns in weather data?
Can additional meteorological features improve forecasting accuracy?

Objectives
To achieve this aim, the following objectives have been established:
•	To compare the performance of statistical, machine learning, and deep learning models for daily precipitation prediction.
•	To analyse how each model captures patterns, seasonality, and trends within the time-series data.
•	To investigate the contribution of additional meteorological variables such as temperature, humidity, and wind speed to forecasting accuracy.
•	To optimise model performance using appropriate evaluation metrics including Mean Squared Error (MSE), Mean Absolute Error (MAE), and R-squared (R²).


 Models Used
 
SARIMAX: Incorporating seasonal trends and exogenous weather features.
Random Forest: Robust ensemble learning for structured data.
Stacking Regressor: Combines Random Forest and Gradient Boosting for better generalization.
LSTM: Captures sequential dependencies for time-series data.

 Results
             	
 Random Forest (Best) MSE  - 0.0044  MAE	-0.0252   R² Score	0.9472  
 Stacking Regressor	  MSE  - 0.0087	 MAE	- 0.0270	 R² Score  0.8964 
 LSTM (After tuning)	 MSE  - 33.6111	MAE	-4.5087   R² Score0.7952  
 SARIMAX(After tuning)MSE  - 0.0425 	MAE	-0.0945   R² Score0.4901 

 Random Forest Regressor was identified as the most effective model based on R² score and low error values.

Technologies

Python 3.x
scikit-learn
statsmodels
keras 
TensorFlow
matplotlib 
seaborn
pmdarima

Setup Instructions

Clone the repository:
git clone https://github.com/nk23aco/7PAM2002-0209-Data-_science_project.git

Install the required packages:
pip install -r requirements.txt

 License
This project is licensed under the Apache 2.0 License.

Acknowledgments
Weather data sourced from Weather Underground via Kaggle.
Libraries used: Scikit-Learn, Statsmodels, TensorFlow/Keras, pmdarima.
