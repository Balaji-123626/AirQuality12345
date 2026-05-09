import numpy as np
import pandas as pd
from prophet import Prophet
import os

def train_and_forecast(csv_path="./AirQualityUCI.csv", periods=24):
    """
    Trains the Prophet model using the existing logic and forecasts future AQI.
    This logic has been preserved exactly as requested.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset {csv_path} not found. Please place it in the project root.")

    #loading the data from csv file to pandas Dataframe
    #Removing those ; in data
    air_quality_data=pd.read_csv(csv_path,sep=";",decimal=",")

    #Deleting  the last 2 columns from Dataframe as they  are empty
    air_quality_data=air_quality_data.iloc[:,:-2]

    #Taking 9357th Row Alone From The Dataframe
    air_quality_data=air_quality_data.head(9357)

    #Handling The Missing Values (Converting All -200 TO NaN )
    air_quality_data.replace(-200, np.nan, inplace=True)

    #Replacing Missing Values With Mean Value
    air_quality_data = air_quality_data.fillna(air_quality_data.mean(numeric_only=True))

    #Converting Date from DD/MM/YY To YY/MM/DD
    air_quality_data["Date"] = pd.to_datetime(air_quality_data["Date"], format="%d/%m/%Y")

    time_info = air_quality_data["Time"]
    time_info = time_info.apply(lambda x: x.replace(".", ":"))

    #Combining 2 series to Pandas Dataframe
    date_time=pd.concat([air_quality_data["Date"],time_info],axis=1)

    #Combining date nd time  to one Dataframe
    date_time["ds"] = date_time["Date"].astype(str) + " " + date_time["Time"].astype(str)

    #We have to Convert ds from object datatype to date time format
    data=pd.DataFrame()
    data["ds"] = pd.to_datetime(date_time["ds"])

    data["y"]=air_quality_data["CO(GT)"]

    #Training The Model
    model = Prophet()
    model.fit(data)

    future = model.make_future_dataframe(periods=periods, freq="H")
    forecast = model.predict(future)

    return model, forecast, data
