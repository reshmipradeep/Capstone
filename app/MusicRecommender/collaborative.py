# Import necessary libraries
import sys
import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds
from scipy.sparse import csr_matrix

# Load the dataset into a DataFrame with the appropriate encoding
file_path = r'data\music_data\songratings.xlsx'
df = pd.read_excel(file_path, engine='openpyxl')

# Set the emotion_input and user_id_input
colab_rec=[]
emotion=sys.argv[1] #eg: "0,3"
emotion_list = [int(e) for e in emotion.strip().split(',')] #eg: [0,3]

user_id = sys.argv[2] 
user_id_input = int(user_id)

for em in emotion_list:
    emotion_input=int(em)

    # Check if the entered emotion is valid
    if emotion_input in df['Emotion'].unique():
        # Filter the DataFrame to only include rows with the entered emotion
        if user_id_input in df['Userid'].unique() and any(df['Userid'] == user_id_input):
            filtered_df = df[df['Emotion'] == emotion_input]
            # Handle duplicates
            filtered_df = filtered_df.drop_duplicates(subset=['Userid', 'Songname'])

            # Create a user-item matrix
            user_item_matrix = filtered_df.pivot(index='Userid', columns='Songname', values='Rating').fillna(0)

            # Convert the DataFrame to a sparse matrix
            sparse_matrix = csr_matrix(user_item_matrix.values)

            # Determine the maximum allowed value for k based on the minimum dimension of the matrix
            max_k = min(sparse_matrix.shape) - 1

            # Choose an appropriate value for k based on the determined maximum
            k = max(1, min(2, max_k))

            # Apply SVD for user-item collaborative filtering
            U, Sigma, Vt = svds(sparse_matrix, k=k)

            # Check if the entered user ID is in the list of unique user IDs and has interactions in the specified emotion
            user_index = np.where(user_item_matrix.index == int(user_id_input))[0]
            # Check if the user index is found
            if user_index.size > 0:
                user_index = user_index[0]

                # Predict ratings for the specified user
                user_predicted_ratings = np.dot(np.dot(U[user_index, :], np.diag(Sigma)), Vt)

                # Get indices of top 3 songs with the highest predicted ratings
                top_song_indices = np.argsort(user_predicted_ratings)[::-1][:3]

                # Get the corresponding song names
                user_item_recommendations = user_item_matrix.columns[top_song_indices]

                # Store unique songs and their URIs
                unique_songs = set()
                colab_songs = []
                # Display the recommendations with user IDs
                print("User-Item Collaborative Filtering Recommendations for emotion ", em)
                for song in user_item_recommendations:
                    if song not in unique_songs:
                        uri = filtered_df.loc[filtered_df['Songname'] == song, 'uri'].values[0]
                        colab_songs.append({'Title': song, 'URI': uri})
                        unique_songs.add(song)
                #print(colab_songs)
            else:
                colab_songs = []  # Reset the recommendations list for item-item filtering

                # Filter the DataFrame to only include rows with the entered emotion
                filtered_df = df[df['Emotion'] == int(emotion_input)]
                # Handle duplicates
                filtered_df = filtered_df.drop_duplicates(subset=['Userid', 'Songname'])

                # Create an item-item matrix
                item_item_matrix = filtered_df.pivot(index='Songname', columns='Userid', values='Rating').fillna(0)

                # Transpose the matrix for item-item collaborative filtering
                item_item_matrix = item_item_matrix.T

                # Convert the DataFrame to a sparse matrix
                sparse_matrix = csr_matrix(item_item_matrix.values)

                # Determine the maximum allowed value for k based on the minimum dimension of the matrix
                max_k = min(sparse_matrix.shape) - 1

                # Choose an appropriate value for k based on the determined maximum
                k = max(1, min(2, max_k))

                try:
                    # Apply SVD for item-item collaborative filtering
                    U, Sigma, Vt = svds(sparse_matrix, k=k)

                    # Get indices of top 3 songs with the highest predicted ratings based on item-item similarity
                    top_song_indices = np.argsort(np.dot(np.dot(U, np.diag(Sigma)), Vt)[:, 0])[::-1][:3]

                    # Get the corresponding song names
                    item_item_recommendations = item_item_matrix.columns[top_song_indices]
                    
                    # Display the recommendations with user IDs
                    print("Item-Item Collaborative Filtering Recommendations for emotion ", em)
                    for song in item_item_recommendations:
                        uri = df.loc[(df['Songname'] == song) & (df['Emotion'] == int(emotion_input)), 'uri'].values[0]
                        user_ids = list(filtered_df[filtered_df['Songname'] == song]['Userid'])
                        colab_songs.append({'Title': song, 'URI': uri})
                    #print(colab_songs)

                except ValueError as e:
                    print(f"Error in Item-Item Collaborative Filtering: {e}")
        else:
            # Item-Item Collaborative Filtering
            colab_songs = []  # Reset the recommendations list for item-item filtering

            # Filter the DataFrame to only include rows with the entered emotion
            filtered_df = df[df['Emotion'] == int(emotion_input)]
            # Handle duplicates
            filtered_df = filtered_df.drop_duplicates(subset=['Userid', 'Songname'])

            # Create an item-item matrix
            item_item_matrix = filtered_df.pivot(index='Songname', columns='Userid', values='Rating').fillna(0)

            # Transpose the matrix for item-item collaborative filtering
            item_item_matrix = item_item_matrix.T

            # Convert the DataFrame to a sparse matrix
            sparse_matrix = csr_matrix(item_item_matrix.values)

            # Determine the maximum allowed value for k based on the minimum dimension of the matrix
            max_k = min(sparse_matrix.shape) - 1

            # Choose an appropriate value for k based on the determined maximum
            k = max(1, min(2, max_k))

            try:
                # Apply SVD for item-item collaborative filtering
                U, Sigma, Vt = svds(sparse_matrix, k=k)

                # Get indices of top 3 songs with the highest predicted ratings based on item-item similarity
                top_song_indices = np.argsort(np.dot(np.dot(U, np.diag(Sigma)), Vt)[:, 0])[::-1][:3]

                # Get the corresponding song names
                item_item_recommendations = item_item_matrix.columns[top_song_indices]
                
                # Display the recommendations with user IDs
                print("Item-Item Collaborative Filtering Recommendations for emotion ",em)
                for song in item_item_recommendations:
                    uri = df.loc[(df['Songname'] == song) & (df['Emotion'] == int(emotion_input)), 'uri'].values[0]
                    user_ids = list(filtered_df[filtered_df['Songname'] == song]['Userid'])
                    colab_songs.append({'Title': song, 'URI': uri})
                #print(colab_songs)

            except ValueError as e:
                print(f"Error in Item-Item Collaborative Filtering: {e}")
            
    else:
        print(f"Invalid emotion: {emotion_input}")
    colab_rec.extend(colab_songs)
#print(colab_rec)