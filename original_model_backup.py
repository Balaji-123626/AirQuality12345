import numpy as np
import pandas as pd

#loading the data from csv file to pandas Dataframe
air_quality_data=pd.read_csv("/content/AirQualityUCI.csv")

#Print 1st 5 rows of Dataframe
air_quality_data.head()

#Removing those ; in data
air_quality_data=pd.read_csv("/content/AirQualityUCI.csv",sep=";",decimal=",")

air_quality_data.head()

#Deleting  the last 2 columns from Dataframe as they  are empty
air_quality_data=air_quality_data.iloc[:,:-2]

air_quality_data.head()

air_quality_data.tail()

air_quality_data.shape


air_quality_data.loc[9357]

#Taking 9357th Row Alone From The Dataframe
air_quality_data=air_quality_data.head(9357)

air_quality_data.head()

air_quality_data.tail()

air_quality_data.shape

#Getting Some Info About the Data
air_quality_data.info()


#Checking Number Of missing Values
air_quality_data.isnull().sum()

#This above output Shows There Are No Missing Values In dataset But actually the missing Values are Taggged with "-200"
#This is Even Described in The UCI Repository Documentation

#Counting How Many Number of Times -200 Appears in data
air_quality_data.isin([-200]).sum(axis=0)

#Handling The Missing Values (Converting All -200 TO NaN )
air_quality_data.replace(-200, np.nan, inplace=True)

air_quality_data.isnull().sum()

air_quality_data.tail()

air_quality_data.mean(numeric_only=True)
#Replacing Missing Values With Mean Value
air_quality_data = air_quality_data.fillna(air_quality_data.mean(numeric_only=True))
air_quality_data.tail()

air_quality_data.tail()

air_quality_data.isnull().sum()



#Forecasting With FB Prophet Algorithm
FB_Prophet_documenatation:"https://facebook.github.io/prophet/docs/ quick_start.html"

#Converting Date from DD/MM/YY To YY/MM/DD
air_quality_data["Date"] = pd.to_datetime(air_quality_data["Date"], format="%d/%m/%Y")

print(air_quality_data["Date"])


time_info = air_quality_data["Time"]

print(time_info)

time_info = time_info.apply(lambda x: x.replace(".", ":"))

print(type(air_quality_data["Date"]))
print(type(time_info))

#Combining 2 series to Pandas Dataframe
date_time=pd.concat([air_quality_data["Date"],time_info],axis=1)

air_quality_data["Date"].head()

time_info.shape


#Combining date nd time  to one Dataframe
date_time["ds"] = date_time["Date"].astype(str) + " " + date_time["Time"].astype(str)


date_time.head()
date_time.info()

#We have to Convert ds from object datatype to date time format
data=pd.DataFrame()

data["ds"] = pd.to_datetime(date_time["ds"])

data.head()

data["y"]=air_quality_data["CO(GT)"]

data.head()

data["y"]=air_quality_data["CO(GT)"]
data.head()

!pip install Prophet

from prophet import Prophet

#Training The Model
model = Prophet()
model.fit(data)

future = model.make_future_dataframe(periods=365, freq="H")
future.tail()

forecast = model.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

fig1 = model.plot(forecast)

fig2 = model.plot_components(forecast)
