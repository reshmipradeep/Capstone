import tensorflow as tf
import tensorflow_hub as hub
import pandas as pd
import math

"""
tweets = [
    "Feeling joyful and excited about the weekend!",
    "Saddened by the news of recent events.",
    "Angry at the traffic jam this morning.",
    "Feeling a bit anxious about the upcoming presentation."
]

"""
twt=pd.read_csv(r"data\preprocessed_data.csv")
tweets=twt["clean"].tolist()

tweets = ['' if isinstance(tweet, float) and math.isnan(tweet) else tweet for tweet in tweets]

# Load the Universal Sentence Encoder model
use_model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

# Encode the tweets using USE
tweet_embeddings = use_model(tweets)

# Print the tweet embeddings
for i, embedding in enumerate(tweet_embeddings):
    print(f"Tweet {i + 1}: {tweets[i]}")
    print(embedding.numpy())
    print()
