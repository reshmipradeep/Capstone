import collaborative
import joblib
import random
import pandas as pd
import numpy as np
import requests
import base64
from sklearn.preprocessing import MinMaxScaler

#content_based model
model_file_path = r'MusicRecommender\content_model.h5'

#music dataset
data1 = pd.read_csv(r"data\music_data\278k_labelled_uri.csv", index_col='Unnamed: 0')
data = data1.drop('uri', axis=1)
X = data.copy()
X.drop(columns=['labels'], inplace=True)
y = data['labels']
scaler = MinMaxScaler()
X = scaler.fit_transform(X)
from sklearn.model_selection import train_test_split
X_train, X_valid, y_train, y_valid = train_test_split(X,y,stratify=y,train_size=0.8,test_size=0.2,random_state=0)
X_test = X_valid

loaded_model = joblib.load(model_file_path)

def get_title_from_uri(uri):
    try:
        # Extract the track ID from the URI
        track_id = uri.split(':')[-1]

        # Spotify API endpoint for track information
        url = f"https://api.spotify.com/v1/tracks/{track_id}"

        # Set the authorization header with the access token
        headers = {"Authorization": f"Bearer {access_token}"}

        # Send a GET request to the Spotify API
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            track_info = response.json()
            return track_info['name']
        else:
            return f"Error fetching title for {uri}: {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

# Spotify Client ID and Client Secret
client_id = "950e9791a5b14b5cb7eeb01b60c9c883"
client_secret = "bd629b8f00c1421095f418dae8dfe901"

# Encode the client ID and client secret in Base64 format
credentials = f"{client_id}:{client_secret}"
credentials_base64 = base64.b64encode(credentials.encode()).decode()

# Spotify Accounts service endpoint for obtaining a token
token_url = "https://accounts.spotify.com/api/token"

# Define the grant type for client credentials flow
data = {"grant_type": "client_credentials"}

# Set the headers with the Base64-encoded credentials
headers = {"Authorization": f"Basic {credentials_base64}"}

# use the loaded_model for making predictions
predicted_labels = loaded_model.predict(X_valid)
content_rec = []

for em in collaborative.emotion_list:
    emotion_input=int(em)

    predicted_confidence_scores = loaded_model.predict_proba(X_valid)[:,emotion_input]
    confidence_threshold = 0.7
    predicted_label_indices = np.where((predicted_labels == emotion_input) & (predicted_confidence_scores >= confidence_threshold))[0]
    label_2_uris = data1.loc[predicted_label_indices, 'uri'].tolist()
    random.shuffle(label_2_uris)

    # Define the number of songs to recommend
    num_recommendations = 3
    recommended_uris = random.sample(label_2_uris, min(num_recommendations, len(label_2_uris)))

    # Make a POST request to obtain a new access token
    response = requests.post(token_url, data=data, headers=headers)

    if response.status_code == 200:
        # Extract the access token from the response
        access_token = response.json()["access_token"]

        # Display the URIs for the recommended songs along with their titles
        for uri in recommended_uris:
            title = get_title_from_uri(uri)
            content_rec.append({"Title": title, "URI": uri})

# Combine the lists
final_rec=content_rec + collaborative.colab_rec
for x in final_rec:
    print (x)
    
# Save the recommendations to a CSV file
output_df = pd.DataFrame(final_rec)
output_csv_path = r'data\music_data\recommendations.csv'
output_df.to_csv(output_csv_path, index=False)
print(f"Recommendations saved to recommendations.csv")