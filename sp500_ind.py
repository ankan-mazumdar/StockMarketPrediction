import streamlit as st
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
import datetime
import pickle
## importing necessery library
from tensorflow import keras as keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dropout
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
@st.cache
def download_stock_data(stock_list):
    curr_date = datetime.datetime.now()
    prev_date = curr_date - datetime.timedelta(days=14)
    period_1 = int(prev_date.timestamp())
    period_2 = int(curr_date.timestamp())
    params ={
    'period1': period_1, 
    'period2': period_2,
    'events' : 'history'
     }
    stock_data = []
    for stock in stock_list:
        #user agent is an identity string which helps the server to identify about its clients
        # use your own user agent !
        response = requests.get(stock_url.format(stock),params = params, headers = 
    {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'})
        response = response.text
        response = response.split('\n')
      
        for row in response:
            row = row.split(',')
            #we need to drop the 1st row of each stock,because it contains header information
            if row!= ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'] :
                #adding the stock name / ticker, since it is not mentioned in response from request
             
                stock_data.append(row)
        
        #now let's convert into pandas dataframe
    stock_data = pd.DataFrame(stock_data, columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])
  
    #stock_data will be a list of data, so we need to convert it into pandas dataframe in future
	#stock_data['Ticker'] = sp500_ind['Ticker'].apply(lambda x : 'SP500_Ind' if x == '%5EGSPC' else x)
    return stock_data



  
def main():
	st.title("SP500 Stock Price Prediction")
	
	menu = ['Home', 'Prediction model']
	choice = st.sidebar.selectbox("Menu", menu)
	
	if choice == 'Home':
		st.subheader('Home')
	elif choice == 'Prediction model':
		st.subheader('Prediction model')
	return choice
	
if __name__ == '__main__':
	choice = main()
	
	
if choice == 'Home':
	"""In  this  project  we  will  predict  future  stock  price  of  SP500  index , using  previous  10  days  info  which  include  'Open', 'High', 'Low',' Close', 'Volume',
	A  very  imp  point  to  note  here is  that,  this  prediction  model  should  not  be  consider  as  a  solely baseline  to  invest  your  hard  money  to  invest  in  stock,  please
	make  your  own  research  before  investment"""

elif choice == 'Prediction model':
	#we will download our data from yahoo finance url
	stock_url = "https://query1.finance.yahoo.com/v7/finance/download/{}"
	
	sp500_ind = download_stock_data(['%5EGSPC'])
	data_load_state = st.text('Loading data...')
	data_load_state.text("Done! (using st.cache)")
	st.write(sp500_ind.tail(10))
	
	scaler_x = pickle.load(open('scaler_x.sav','rb'))
	scaler_y = pickle.load(open('scaler_y.sav','rb'))
	loaded_model = load_model('model.h5')
	
	X = sp500_ind[['Open','High','Low','Close','Volume']].tail(10).values
	X_scaled=scaler_x.fit_transform(np.array(X))
	
	
	X_up_scaled=scaler_x.inverse_transform(np.array(X_scaled))
	y_predict = loaded_model.predict(np.array([X_scaled]))
	return_pred = scaler_y.inverse_transform(y_predict)
	#Price tomorrow = Price today * (Return + 1)
	pred_price = X_up_scaled[-1][0] * (return_pred + 1)
	st.write("Next day prediction for S&P500 ind is ",pred_price)
	
