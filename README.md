# Capstone Project: Music Recommender System with Sentiment Analysis

## Overview
This is the repository for Batch34's Capstone Project, focused on creating a music recommendation system with sentiment analysis. The primary goal is to classify the emotions expressed in Twitter user tweets using machine learning and natural language processing techniques. The system then employs a hybrid approach, combining content-based and collaborative filtering methods, to provide personalized music recommendations based on the identified emotions.

## Project Components

### 1. Scraping Data
User's data is scraped from threads or twitter (X) based on the user's choice. The retrieved data then undergoes preprocessing like stop-word removal, tokenization, handling hastags, etc.

### 2. Word Embeddings
The project utilizes cutting-edge methods, including:
- Term Frequency-Inverse Document Frequency (TF-IDF)
- GloVe Embeddings
- Universal Sentence Encoder

These methods are employed to extract useful features from user tweets.

### 3. Emotion Classification
A deep convolutional neural network (DCNN) is employed to classify emotions in tweets. The model is trained on a labeled dataset of tweets annotated with emotion labels, covering categories such as joy, sadness, anger, etc.

### 4. Music Recommendation
The project adopts a hybrid strategy that combines collaborative filtering with content-based recommendation. This strategy leverages the emotional context extracted from tweets to produce tailored music recommendations.

## Implementation Details

- **Tweet and Music Data:** The project is tested using a substantial dataset of tweets and music data.  
- **Evaluation:** Findings from the testing phase indicate promising improvements in music recommendation accuracy compared to conventional approaches.

## Potential Impact
The inclusion of emotional context from user tweets has the potential to enhance the user experience of music recommendation systems. Additionally, the project contributes to the fields of Natural Language Processing (NLP) and machine learning by exploring cutting-edge methods for music recommendation using social media data.

## How to Run
- 1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/your-repository.git
- 2. **Install Dependencies:**
   ```bash
   cd app
   pip install -r requirements.txt
- 3. **Run the App:**
   ```bash
   flask run
- 4. **Access the Application:**
Open your web browser and go to [http://localhost:8000](http://localhost:8000)

## Contributors
- PES2UG20CS900 [Alekhya Sundari R Nanduri](https://github.com/alekhyananduri)
- PES2UG20CS905 [D Mrudula](https://github.com/Dmrudula)
- PES2UG20CS910 [Harshitha Golla](https://github.com/harshithagolla)
- PES2UG20CS270 [Reshmi Pradeep](https://github.com/reshmipradeep)

