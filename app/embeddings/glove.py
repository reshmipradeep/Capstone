import numpy as np
import os

# Define the path to the GloVe embeddings file
GLOVE_DIR = r'embeddings'  # Change this to the directory containing your GloVe embeddings file
GLOVE_FILE = 'glove.twitter.27B.25d.txt'  # Change this to your GloVe file name

# Load pre-trained GloVe embeddings into a dictionary
def load_glove_embeddings():
    embeddings = {}
    with open(os.path.join(GLOVE_DIR, GLOVE_FILE), 'r', encoding='utf-8') as f:
        for line in f:
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            embeddings[word] = coefs
    return embeddings

# Function to get GloVe embeddings for a list of threads
def get_glove_embeddings_for_threads(threads, embeddings):
    thread_embeddings_matrix = []
    for thread in threads:
        preprocessed_thread = thread.lower().split()  # Simple preprocessing (lowercase and split)
        thread_embeddings = []
        for word in preprocessed_thread:
            if word in embeddings:
                word_embedding = embeddings[word]
                thread_embeddings.append(word_embedding)
            else:
                # Handle out-of-vocabulary words (e.g., skip or use a default vector)
                pass
        thread_embeddings_matrix.append(np.mean(thread_embeddings, axis=0))  # Average word embeddings for the thread
    return np.array(thread_embeddings_matrix)

# List of 10 threads
threads = r"data\preprocessed_data.csv"

# Load pre-trained GloVe embeddings
glove_embeddings = load_glove_embeddings()

# Get GloVe embeddings for the list of threads
thread_embeddings_matrix = get_glove_embeddings_for_threads(threads, glove_embeddings)
print(thread_embeddings_matrix)

# thread_embeddings_matrix is a matrix where each row represents a thread's embeddings
