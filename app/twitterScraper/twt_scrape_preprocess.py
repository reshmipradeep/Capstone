from tweety import Twitter
import pandas as pd
import re
import string
import sys
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.stem import PorterStemmer, WordNetLemmatizer
import emoji
import contractions
from ekphrasis.classes.segmenter import Segmenter
"""
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
"""
NEGATIONS = {
        "ain't": "is not",
        "aren't": "are not",
        "can't": "cannot",
        "cant": "cannot",
        "cause": "because",
        "cuz": "because",
        "couldn't": "could not",
        "didn't": "did not",
        "didnt": "did not",
        "doesn't": "does not",
        "doesnt": "does not",
        "don't": "do not",
        "dont": "do not",
        "hadn't": "had not",
        "hadnt": "had not",
        "hasn't": "has not",
        "hasnt": "has not",
        "haven't": "have not",
        "havent": "have not",
        "isn't": "is not",
        "lol": "laugh out loud",
        "mayn't": "may not",
        "might've": "might have",
        "mightn't": "might not",
        "must've": "must have",
        "mustn't": "must not",
        "needn't": "need not",
        "nope" :'no',
        "shan't": "shall not",
        "sha'n't": "shall not",
        "shouldn't": "should not",
        "wasn't": "was not",
        "wasn": "was not",
        "weren't": "were not",
        "won't": "will not",
        "wouldn't": "would not",
        "y": "why",
        "ya": 'yes',
        "plz": "please",
        "thx": "thank",
        "thanx": "thank",
        "thanks": "thank",
        "u": "you"
    }

user_name = sys.argv[1]
print(f"Username input from app.py: {user_name}")
app = Twitter("session")
app.sign_in("something116802", "09876zaqxswedc!@#")
target_username=user_name

user = app.get_user_info(target_username)
all_tweets = app.get_tweets(user, pages=2)
# Initialize the Segmenter
seg = Segmenter()

def preprocess_tweet(tweet):
    
    # Remove URLs and mentions
    tweet = re.sub(r"http\S+|www\S+|https\S+", "", tweet, flags=re.MULTILINE)
    tweet = re.sub(r"@\w+", "", tweet)
    
    # Convert emojis to words
    tweet = emoji.demojize(tweet)
    tweet = tweet.replace(":", " ")
    tweet = tweet.replace("_", " ")
    
    # Remove special charecters and numbers
    tweet = re.sub(r"[^\w\s']", "", tweet)
    tweet = re.sub(r"\d+", "", tweet)
    
    # Tokenization
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
    tokens = tokenizer.tokenize(tweet)
      
    # Apply the contraction map
    tokens = [NEGATIONS.get(item, item) for item in tokens]
    
#     for token in tokens:
#         mapped_token = NEGATIONS.get(token, token)
#         print(f"Original token: {token}, Mapped token: {mapped_token}")

    
    # Remove stopwords
    custom_stopwords = set(["gonna",  "gotta", "us", "k",  "ok",  "he'd",  "he'll",  "here's",  "he's",  "how'd",  "how'll",  
                            "how's",  "i'd",  "i'll",  "i'm",  "im",  "i'd",  "i'll",  "i'm",  "i've",  "ive",  "it'd",  
                            "it'll",  "it's",  "let's",  "might've",  "must've",  "she'd",  "she'll",  "she's",  "should've",  
                            "so've",  "so's",  "that'd",  "that's",  "there'd",  "there's",  "they'd",  "they'll",  "they're",  
                            "they've",  "to've",  "we'd",  "we'll",  "we're",  "we've",  "what'll",  "what're",  "what's",  
                            "what've",  "when's",  "when've",  "where'd",  "where's",  "where've",  "who'll",  "who's",  
                            "who've",  "why's",  "why've",  "will've",  "would've",  "y'all",])
    
    remove_words=set(['no', 'nor', 'not', 'down', 'only', 'until', 'again', 'under', 'other', 'against'])
    stop_words = set(stopwords.words("english")).difference(remove_words).union(custom_stopwords)
    filtered_tokens = [token for token in tokens if token not in stop_words]
    
    # Extract hashtags and segment them using ekphrasis Segmenter
    hashtags = [token[1:] for token in tokens if token.startswith("#")]
    segmented_hashtags = [seg.segment(hashtag) for hashtag in hashtags]

    # Append segmented hashtags to the preprocessed tweet
    preprocessed_tokens = filtered_tokens + segmented_hashtags
    preprocessed_tweet = ' '.join(preprocessed_tokens)
    
    # Remove punctuations 
    tweet = tweet.translate(str.maketrans('', '', string.punctuation))
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    return ' '.join(lemmatized_tokens)

# Preprocess and print each tweet
for tweet in all_tweets:
    preprocessed_tweet = preprocess_tweet(tweet.text)
    print("Original tweet:", tweet.text)
    print("Preprocessed tweet:", preprocessed_tweet)
    print("-" * 50)

# Create a list to store preprocessed tweets
preprocessed_tweets = []

# Preprocess and store each tweet in the list
for tweet in all_tweets:
    preprocessed_tweet = preprocess_tweet(tweet.text)
    preprocessed_tweets.append(preprocessed_tweet)

# Create a DataFrame from the preprocessed tweets
df = pd.DataFrame({'username': [target_username] * len(preprocessed_tweets),'clean': preprocessed_tweets})
print(df)
#replacing nan values with empty string
df['clean'] = df['clean'].fillna('')

# Save the DataFrame to a CSV file
df.to_csv(r'data\preprocessed_data.csv', index=False)

print("Dataset created and saved to preprocessed_data.csv")