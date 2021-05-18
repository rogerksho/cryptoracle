# cryptoracle-api
this is a flask-gunicorn based API which utilizes a [trained machine learning model](https://github.com/rogerksho/crypto-social-model) to predict bitcoin price changes based on recent google trend data and sentiment data based on recent tweets about bitcoin. 

because the twitter crawler takes a long time to pull, i've opted to use AWS RDS to store each predicted price, so the API works like this:
1. return the most recently stored predicted price change
2. start a new thread to collect data from google/twitter and run the trained model on it (pseudo-async)
3. upload predictions to database when data collection and prediction is finished 

this whole application is packaged into a [docker image](https://hub.docker.com/r/rogerho/python-machine-learn-twint) for easy deployment on any virtual machines on the cloud (e.g. AWS EC2).

this API is intended to be used with another project which consists of a single page application (SPA) which displays the predictions in an easily digestible way (currently in development).

