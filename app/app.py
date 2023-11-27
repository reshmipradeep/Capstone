from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import subprocess
import csv
import pandas as pd
import numpy as np

app = Flask(__name__)
app.secret_key = "manbearpig_MUDMAN888"

# Set up Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

user_data = pd.read_excel(r'data\user_data.xlsx')

# User class for Flask-Login
class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    user = User()
    user.id = user_id
    return user

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check if the username exists in the user_data DataFrame
        user_query = user_data[(user_data['username'] == username)]
        
        if not user_query.empty:
            # Check if the provided password matches the stored password
            user = user_query.iloc[0]
            if user['password'] == password:
                user_obj = User()
                user_obj.id = user['user_id']
                login_user(user_obj)
                
                # Convert user ID to a standard Python integer before storing in session
                session['user_id'] = int(user['user_id'])
                
                return redirect(url_for('main'))
            else:
                flash("Invalid password. Please try again.")
        else:
            flash("Invalid username. Please try again.")
    
    return render_template("login.html")

@app.route("/register", methods=['POST', 'GET'])
def register():
    global user_data
    alert_message = None  # Initialize alert_message
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check if the username already exists
        if username in user_data['username'].values:
            alert_message = "Username already exists. Please choose a different one."
        else:
            # Generate a unique user ID
            user_id = user_data['user_id'].max() + 1
            # Add the new user to the user_data DataFrame
            new_user = {'user_id': user_id, 'username': username, 'password': password}
            #user_data = user_data.append(new_user, ignore_index=True)
            user_data = pd.concat([user_data, pd.DataFrame([new_user])])
            # Save the updated user_data DataFrame to the Excel file
            user_data.to_excel(r'data\user_data.xlsx', index=False)
            
            flash("Registration successful! You can now log in.")
            return redirect(url_for('login'))
    
    return render_template("register.html", alert_message=alert_message)

@app.route("/main", methods=['POST', 'GET'])
@login_required
def main():
    flash("Would you like to use")
    user_choice = request.form.get('user_type')  # Retrieve user choice from the form
    print(user_choice)
    return render_template("main.html", user_choice=user_choice)

@app.route("/username", methods=['POST', 'GET'])
@login_required
def username():
    user_choice = request.form.get('user_type')  # Retrieve user type from the form
    return render_template("username.html", user_type=user_choice)

@app.route("/recommend", methods=['POST', 'GET'])
@login_required
def recommend():
    user_choice = request.form.get('user_type')  # Retrieve user choice from the form
    username_input = request.form.get('username_input')  # Retrieve username from the form
    # Retrieve user ID from the session
    user_id = session.get('user_id')
    if user_id is None:
        flash("User not logged in. Please log in.")
        return redirect(url_for('login'))
    
    if username_input is None:
        flash("Please enter your username")
        return render_template("username.html")

    if user_choice == 'twitter':
        print("twitter chosen")
        #scrape tweets and preprocess
        subprocess.run(["python", r"twitterScraper\twt_scrape_preprocess.py", username_input])

    elif user_choice == 'threads':
        print("threads chosen")
        #scrape threads
        subprocess.run(["python", r"threadsScraper\scrape.py", username_input])
        #preprocessing threads
        subprocess.run(["python", r"preprocessor\preprocessing.py", r"data\threads_data\new.csv"])

    #generating word embeddings and combining them
    subprocess.run(["python", r"embeddings\combiner.py", "preprocessed_data.csv"])
    #running emotion classifier
    subprocess.run(["python", r"EmotionClassifier\emotion.py"], bufsize=0)

    #read emotion
    with open(r"EmotionClassifier\emotion_value.txt", "r") as file:
        emotion = file.read().strip()
    
    session['emotion'] = emotion
    #getting recommended songs
    subprocess.run(["python", r"MusicRecommender\hybrid.py", emotion, str(user_id)])

    with open(r'data\music_data\recommendations.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        data = list(csvreader)

    return render_template("recommend.html", data=data, emotion=emotion)

@app.route("/submit_ratings", methods=['POST'])
@login_required
def submit_ratings():
    emotion = session.get('emotion') #"1,2"
    emotion_list=[int(e) for e in emotion.strip().split(',')] #[1,2]

    if request.method == 'POST':
        # Process the submitted ratings
        ratings = request.form.getlist('ratings[]')
        print("Received ratings:", ratings)
        recommendations_file = r'data\music_data\recommendations.csv'

        with open(recommendations_file, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            song_data = list(csvreader)
            song_data = song_data[1:]
        # Get user ID from the session
        user_id = session.get('user_id')
        # Append data to the existing Excel sheet
        ratings_file = r'data\music_data\songratings.xlsx' 
        df = pd.read_excel(ratings_file)

        pattern = np.repeat(emotion_list, 3)[:len(ratings)]
        emotion_pattern=np.concatenate((pattern,pattern))
        #print(emotion_pattern)

        for i in range(min(len(song_data), len(ratings))):  # loop doesn't go out of bounds check
            song_info = song_data[i]
            rating = float(ratings[i])
            emotion_value = emotion_pattern[i % len(emotion_pattern)]
            df = pd.concat([df, pd.DataFrame([{'Emotion': emotion_value,'Songname': song_info[0], 'Rating': rating, 'uri': song_info[1], 'Userid': user_id}])], ignore_index=True)
        # Create the alternating pattern for the "Emotion" column
        print(df)
        # Save the updated DataFrame to the Excel file
        df.to_excel(ratings_file, index=False)

        print("Ratings stored successfully.")
        # Implement logic to store or process the ratings as needed
        return render_template("thankyou.html")

@app.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()
    logout_user()
    print("Logged out successfully")
    return redirect(url_for('home'))