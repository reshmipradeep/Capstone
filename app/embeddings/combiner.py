import numpy as np

# Assuming you have three sets of embeddings/feature arrays:
import use
import glove
import tfidf

glove_embeddings = glove.thread_embeddings_matrix  # Shape: (num_tweets, num_dimensions)
tfidf_vectors = tfidf.tfidf_vectors_dense  # Shape: (num_tweets, num_dimensions)
use_embeddings = use.tweet_embeddings  # Shape: (num_tweets, num_dimensions)

max_tweets = max(glove_embeddings.shape[0], tfidf_vectors.shape[0], use_embeddings.shape[0])

# Pad the arrays with zeros to match the maximum number of tweets
glove_embeddings = np.pad(glove_embeddings, ((0, max_tweets - glove_embeddings.shape[0]), (0, 0)), mode='constant')
tfidf_vectors = np.pad(tfidf_vectors, ((0, max_tweets - tfidf_vectors.shape[0]), (0, 0)), mode='constant')
use_embeddings = np.pad(use_embeddings, ((0, max_tweets - use_embeddings.shape[0]), (0, 0)), mode='constant')
# Stack the arrays along a new dimension (axis 1)
stacked_embeddings = np.hstack((glove_embeddings, tfidf_vectors, use_embeddings))

# The resulting shape will be (num_tweets, num_dimensions* 3) where 3 represents the number of embeddings/features stacked.
np.save(r"data\extracted_embeddings.npy", stacked_embeddings)

