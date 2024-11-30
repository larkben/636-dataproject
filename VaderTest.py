import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import datetime
from nltk.classify import NaiveBayesClassifier
from nltk import classify
import nltk

# Download necessary NLTK resources
nltk.download('vader_lexicon')

# Function to convert date to unix timestamp
def date_to_unix(date_str, date_format="%Y-%m-%d %H:%M:%S"):
    try:
        dt = datetime.strptime(date_str, date_format)
        return dt.timestamp()
    except ValueError:
        return None  # Handle invalid date formats gracefully

# Function to analyze sentiment using VADER
def analyze_sentiment_vader(comment):
    sentiment = sia.polarity_scores(comment)
    compound_score = sentiment['compound']
    if compound_score > 0.05:
        return "Positive"
    elif compound_score < -0.05:
        return "Negative"
    else:
        return "Neutral"

# Initialize VADER Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

# 1. Load Data
try:
    reddit_data = pd.read_csv('/workspaces/636-dataproject/data/combined_reddit.csv')  # Scraped Reddit posts
    stock_data = pd.read_csv('/workspaces/636-dataproject/data/combined_prices.csv')   # Historical stock data
    news_data = pd.read_csv('/workspaces/636-dataproject/data/combine_news.csv')       # News headlines
except FileNotFoundError as e:
    print(f"Error: {e}")
    exit()

# 2. Preprocessing
# Analyze sentiment for Reddit and News data
reddit_data['sentiment'] = reddit_data['comment'].apply(lambda x: analyze_sentiment_vader(str(x)))
news_data['sentiment'] = news_data['Summary'].apply(lambda x: analyze_sentiment_vader(str(x)))

# Handle numeric conversions and missing values in stock data
stock_data['Volume'] = stock_data['Volume'].apply(lambda x: float(str(x).replace(",", "")) if pd.notnull(x) else 0)
stock_data['Open'] = stock_data['Open'].fillna(0)
stock_data['Close'] = stock_data['Close'].fillna(0)
stock_data['Volume'] = stock_data['Volume'].fillna(0)

# Debugging: Check dataset lengths
print(f"Reddit Sentiments: {len(reddit_data['sentiment'])}, News Sentiments: {len(news_data['sentiment'])}")

# Scale Stock Data Features
scaler = StandardScaler()
stock_data_scaled = scaler.fit_transform(stock_data[['Open', 'Close', 'Volume']])

# Create stock labels based on the closing price
threshold = 0
stock_labels = np.where(stock_data_scaled[:, 1] > threshold, 'Increase', 'Decrease')

# 3. Feature Engineering
# Align lengths by trimming datasets to the minimum length
min_length = min(len(reddit_data), len(news_data), len(stock_labels))
reddit_sentiment_trimmed = reddit_data['sentiment'].values[:min_length]
news_sentiment_trimmed = news_data['sentiment'].values[:min_length]
stock_labels_trimmed = stock_labels[:min_length]

# Combine Reddit and News Sentiment as features
combined_features = np.vstack([reddit_sentiment_trimmed, news_sentiment_trimmed]).T

# Convert categorical sentiment to numerical for NaiveBayesClassifier
def sentiment_to_numeric(sentiment):
    return {
        'Positive': 1,
        'Negative': -1,
        'Neutral': 0
    }.get(sentiment, 0)

combined_features = np.array([[sentiment_to_numeric(x) for x in feature] for feature in combined_features])

# 4. Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(combined_features, stock_labels_trimmed, test_size=0.3, random_state=42)

# Prepare data for NaiveBayesClassifier
train_data = [({f'feature_{i}': X_train[j][i] for i in range(len(X_train[j]))}, y_train[j]) for j in range(len(X_train))]
test_data = [({f'feature_{i}': X_test[j][i] for i in range(len(X_test[j]))}, y_test[j]) for j in range(len(X_test))]

# 5. Train the NaiveBayesClassifier
classifier = NaiveBayesClassifier.train(train_data)

# 6. Evaluation
# Calculate accuracy
accuracy = classify.accuracy(classifier, test_data)
print(f"Accuracy: {accuracy:.2f}")

# Generate predictions and classification report
y_pred = [classifier.classify({f'feature_{i}': x[i] for i in range(len(x))}) for x in X_test]
print(classification_report(y_test, y_pred))

# Show most informative features
classifier.show_most_informative_features()
