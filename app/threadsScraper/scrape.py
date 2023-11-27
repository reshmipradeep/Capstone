from threads_interface import ThreadsInterface
from base_interface import BaseThreadsInterface
import sys

scraper = ThreadsInterface()
base = BaseThreadsInterface()
# User ID of the user you want to retrieve information for
user_name = sys.argv[1]
print(f"Username input from app.py: {user_name}")

try:
    # Retrieve user information
    user_id=base.retrieve_user_id(user_name)
    user_data = scraper.retrieve_user(user_id)
    #print(user_data)
    user_threads = scraper.retrieve_user_threads(user_id)
    #print(user_threads)
    scraper.save_data_to_csv(user_threads, r"data\threads_data\new.csv")
except Exception as e:
    print(f"An error occurred: {str(e)}")
