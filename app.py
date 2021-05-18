from fetch_data import recent_tweets
from flask import Flask
from joblib import dump, load
from sklearn import linear_model
import numpy as np

import psycopg2
from pytrends.request import TrendReq
import threading
from datetime import datetime
import sys
import os

# postgres init
conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="24062001",
    host="coin-prices.cr8uycnutjeo.us-east-2.rds.amazonaws.com",
    port='5432'
)
cur = conn.cursor()

# flask init
app = Flask(__name__)

# ml model load
s = load('elasticnet.joblib')

# pytrends init
kw_list = ["bitcoin"]
pytrends = TrendReq(hl='en-US')
pytrends.build_payload(kw_list, timeframe='now 1-d')

def insert_entry():
    # twint
    avg_sentiment = recent_tweets()

    # time
    datetime_str_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # gtrend
    pytrend_df = pytrends.interest_over_time()
    google_series = pytrend_df.loc[:, "bitcoin"]
    google_trend_avg = google_series.mean()

    # predict
    data_in = np.array([avg_sentiment, google_trend_avg])
    predicted_px = s.predict(data_in.reshape(1, -1))[0]

    # insert
    cur.execute("INSERT INTO coin_prices (time, predicted_px) VALUES (%s, %s)", (datetime_str_now, predicted_px))
    conn.commit()

    print('>>> DB INSERT DONE')


@app.route('/predict')
def get_prediction():
    t = threading.Thread(target=insert_entry)

    cur.execute("SELECT * FROM coin_prices ORDER BY time DESC LIMIT 2")
    result = cur.fetchall()

    latest_price = result[0][1]
    prev_price = result[1][1]
    
    price_diff = latest_price - prev_price

    t.start()
    return str(price_diff)