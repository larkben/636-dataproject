from bs4 import BeautifulSoup
import pandas as pd
import praw

# task list
'''
- collect reddit data from command line with scores
- data reddit data and parse with sentiment dictionary into .csv
- collect data from alpha query as .csv
- collect yfinance news article header sentiment
'''

# Reddit API credentials
client_id = '0g9lCAnzXBGm_NfCtRG1Eg'
client_secret = '_HyRrtKJxfT6MhOocqC_L6s9mhNjKQ'
user_agent = 'my_reddit_scraper/0.1 by u/spartinofarrows'

# Initialize the PRAW client
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

# Function to get comments containing a specific keyword
def get_comments_with_keyword(thread_url, keyword):
    # Load the Reddit submission (thread) by URL
    submission = reddit.submission(url=thread_url)

    # Replace "replace_more" to expand all comments
    submission.comments.replace_more(limit=None)

    # List to store comments that contain the keyword
    matching_comments = []

    # Search through each comment for the keyword
    for comment in submission.comments.list():
        if keyword.lower() in comment.body.lower():  # Case-insensitive search
            matching_comments.append({
                'author': comment.author.name if comment.author else '[deleted]',
                'comment': comment.body,
                'score': comment.score,
                'created_utc': comment.created_utc
            })

    return matching_comments

# Function to save comments to CSV
def save_comments_to_csv(comments, filename="filtered_comments.csv"):
    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(comments)
    
    # Save DataFrame to CSV
    df.to_csv(filename, index=False)
    print(f"Comments saved to {filename}")

# Example usage
if __name__ == "__main__":
    thread_url = "https://www.reddit.com/r/wallstreetbets/comments/1gh9050/weekly_earnings_thread_114_118/"  # Replace with your desired thread URL
    keyword = "ARM"  # Keyword to search for in comments

    comments = get_comments_with_keyword(thread_url, keyword)
    
    # Print the results to the console
    for idx, comment in enumerate(comments, 1):
        print(f"{idx}. Author: {comment['author']}\nScore: {comment['score']}\nComment: {comment['comment']}\n")

    # Save the comments to a CSV file
    save_comments_to_csv(comments, filename="filtered_comments.csv")

print("Hello World!")