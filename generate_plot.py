import plotly
from db_controller import db_conn
import plotly.graph_objs as go
import pandas as pd

connection = db_conn().connect()
disch_lookups = pd.read_sql( """SELECT time, magnitude, country_de FROM earthquakes """, connection )


# print(disch_lookups)   

df = pd.DataFrame()
data_us = disch_lookups[disch_lookups['country_de'].isin(["United States"])]
data_chile = disch_lookups[disch_lookups['country_de'].isin(["Chile"])]
data_japan = disch_lookups[disch_lookups['country_de'].isin(["Japan"])]
# print(type(data_us['time'].iloc[-1]))





settings = {
    "data": [go.Scatter(x=(pd.to_datetime(pd.to_numeric(data_us['time']), unit='ms')).tolist(), y=data_us['magnitude'].tolist(), name="United States"), 
            go.Scatter(x=(pd.to_datetime(pd.to_numeric(data_chile['time']), unit='ms')).tolist(), y=data_chile['magnitude'].tolist(), name="Chile"),
            go.Scatter(x=(pd.to_datetime(pd.to_numeric(data_japan['time']), unit='ms')).tolist(), y=data_japan['magnitude'].tolist(), name="Japan")],
    "layout": go.Layout(title="Magnitude Days& Countries")

}
# generates plot using plotly on offline
plotly.offline.plot(settings, auto_open=False, filename="./templates/plt.html")
print("Complete. Generated plot at templates/plt.html")
