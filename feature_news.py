import pandas as pd
import textblob
from textblob import TextBlob
import re
from datetime import datetime

# Load the data file (replace with your combined news/comments file path)
data_file = "/workspaces/636-dataproject/data/combine_news.csv"
df = pd.read_csv(data_file)

# Define feature extraction functions
def extract_sentiment_polarity(text):
    """
    Analyze the sentiment and polarity of a given text.
    Returns:
    - Sentiment: Positive, Negative, Neutral
    - Polarity Score: Float between -1 (negative) and 1 (positive)
    """
    blob = TextBlob(str(text))  # Convert to string in case of NaNs
    polarity = blob.sentiment.polarity
    sentiment = (
        "Positive" if polarity > 0 else "Negative" if polarity < 0 else "Neutral"
    )
    return sentiment, polarity


def extract_keywords(text):
    """
    Extract keywords (e.g., stock symbols or capitalized words) from the text.
    - Keywords are identified as words with all uppercase letters.
    """
    keywords = re.findall(r"\b[A-Z]{2,}\b", str(text))  # Capitalized words
    return ", ".join(keywords) if keywords else None


def calculate_comment_length(text):
    """
    Calculate the length of the given text.
    """
    return len(str(text))


def extract_time_features(date_string):
    """
    Extract day of the week and time of day from the date string.
    Expects the date in the format 'Month Day, Year' or ISO format.
    """
    try:
        date_obj = datetime.strptime(date_string, "%B %d, %Y")
    except ValueError:
        try:
            date_obj = datetime.strptime(date_string, "%Y-%m-%d")
        except ValueError:
            return None, None
    day_of_week = date_obj.strftime("%A")
    time_of_day = date_obj.strftime("%H:%M") if hasattr(date_obj, "time") else None
    return day_of_week, time_of_day


# Apply feature extraction to the dataset
df[["sentiment", "polarity_score"]] = df["Summary"].apply(
    lambda x: pd.Series(extract_sentiment_polarity(x))
)
df["keywords"] = df["Summary"].apply(extract_keywords)
df["comment_length"] = df["Summary"].apply(calculate_comment_length)
df[["day_of_week", "time_of_day"]] = df["Published"].apply(
    lambda x: pd.Series(extract_time_features(x))
)

# Save the extracted features to a new CSV file
output_file = "data/extracted_features.csv"
df.to_csv(output_file, index=False)
print(f"Feature extraction completed. Results saved to {output_file}")

# Display a sample of the extracted features
print(df.head())
