import twint
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# vader setup
analyzer = SentimentIntensityAnalyzer()

# twint config
c = twint.Config()
c.Search = "bitcoin OR btc"
c.Hide_output = True
c.Limit = 1000

# proxy for AWS
c.Proxy_host = "51.158.68.68"
c.Proxy_port = "8761"
c.Proxy_type = "http"

# twint-pandas-specific settings
c.Pandas = True
c.Pandas_clean = True



def recent_tweets() -> float:
    twint.run.Search(c)
    tweets_df = twint.storage.panda.Tweets_df

    # init twint vars
    num_samples = 0
    sentiment_sum = 0.0

    # access tweet
    tweets_series = tweets_df.loc[:, "tweet"]

    # calculate avg sent
    for t in tweets_series:
        sentiment = analyzer.polarity_scores(t)

        # skip neutral
        if sentiment["compound"] < 0.05 and sentiment["compound"] > -0.05:
            continue
        else:
            num_samples += 1

        sentiment_sum += sentiment["compound"]

    return(sentiment_sum/num_samples)
    

if __name__ == '__main__':
    print(recent_tweets())