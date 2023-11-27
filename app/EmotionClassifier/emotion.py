import numpy as np
import tensorflow
from tensorflow import keras

# Load the trained model
loaded_model = keras.models.load_model(r'EmotionClassifier\dcnnmodel.h5')

# Load the embeddings you want to predict
new_embeddings = np.load(r"data\extracted_embeddings.npy")

emotions = ['anger', 'anticipation', 'disgust', 'fear', 'joy', 'love', 'optimism', 'pessimism', 'sadness', 'surprise', 'trust']

# Make predictions
predictions = loaded_model.predict(new_embeddings)

# Assuming your model outputs probabilities for each emotion, you can use argmax to get the overall predicted emotion
overall_prediction = np.argmax(predictions, axis=1)
emotion=[]
emotion_value=emotions[overall_prediction[0]]
# Print the overall predicted emotion
print("Overall Predicted Emotion:", emotion_value)
#Labels: {'sad': 0, 'happy': 1, 'energetic': 2, 'calm': 3}
#The emotion annotation and representation language (EARL) proposed by the Human-Machine Interaction Network on Emotion (HUMAINE) 
#https://web.archive.org/web/20080411092724/http://emotion-research.net/projects/humaine/earl

if emotion_value == 'joy' or emotion_value == 'optimism' : #Positive and lively - happy,energetic 
    emotion = "1,2"
if emotion_value == 'love' or emotion_value == 'trust': #Caring - happy,calm
    emotion = "1,3"
elif emotion_value =='pessimism' or emotion_value =='sadness': #Negative and passive - sad,calm
    emotion = "0,3"
elif emotion_value == 'surprise' or emotion_value == 'anticipation': #Reactive - energetic , calm - to reduce anxiousness
    emotion = "2,3"
elif emotion_value == 'anger' or emotion_value == 'disgust': #Negative and forceful - sad,energetic
    emotion = "0,2"
elif  emotion_value == 'fear': #Negative and not in control - sad,calm
    emotion = "0,3"
print(emotion)
with open(r"EmotionClassifier\emotion_value.txt", "w") as file:
    file.write(emotion)