from sklearn.feature_extraction.text import TfidfVectorizer
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
# Initialize the TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer()

# Fit and transform the tweets to compute TF-IDF vectors
tfidf_vectors = tfidf_vectorizer.fit_transform(tweets)

# Get the feature names (words) corresponding to each column in the TF-IDF matrix
feature_names = tfidf_vectorizer.get_feature_names_out()

# Convert TF-IDF vectors to a dense array for easier handling
tfidf_vectors_dense = tfidf_vectors.toarray()

# Print the TF-IDF vectors and feature names for reference
print("TF-IDF Vectors: \n")
print(tfidf_vectors_dense)
print("\n \nFeature Names:")
print(feature_names)
