import pandas as pd
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import wordnet

nltk.download('vader_lexicon')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

def read_bad_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip().lower() for line in file]

def find_tweets_for_term(term, sentences):
    tweets = []
    regex = re.compile(r'\b{}\b'.format(re.escape(term)))
    for sentence in sentences:
        if regex.search(sentence.lower()):
            tweets.append(sentence)
    return tweets

def analyze_term(csv_file_path, term):
    # Read sentences from CSV file
    df = pd.read_csv(csv_file_path)

    # Extract sentences from the sixth column
    sentences = df.iloc[:, 5].dropna().astype(str).tolist()

    # Find tweets containing the given term
    term_tweets = find_tweets_for_term(term.lower(), sentences)

    # Initialize sentiment analyzer
    sid = SentimentIntensityAnalyzer()

    # Collect sentiment scores for each tweet containing the term
    sentiment_scores = []
    for tweet in term_tweets:
        sentiment = sid.polarity_scores(tweet)
        sentiment_scores.append((sentiment['compound'], tweet))

    # Compute average sentiment score
    avg_sentiment = sum(score[0] for score in sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.0

    # Find highest and lowest sentiment tweets
    if sentiment_scores:
        highest_sentiment_tweet = max(sentiment_scores, key=lambda x: x[0])[1]
        lowest_sentiment_tweet = min(sentiment_scores, key=lambda x: x[0])[1]
    else:
        highest_sentiment_tweet = "No tweets found"
        lowest_sentiment_tweet = "No tweets found"

    return avg_sentiment, len(term_tweets), highest_sentiment_tweet, lowest_sentiment_tweet

# Usage
csv_file_path = 'cleaned_file.csv'
term = input("Enter the term to analyze: ")

# Analyze term for the original term
avg_sentiment, term_count, highest_sentiment_tweet, lowest_sentiment_tweet = analyze_term(csv_file_path, term)

# Get synonyms for the term
synonyms = set()
for syn in wordnet.synsets(term):
    for lemma in syn.lemmas():
        synonym = lemma.name().lower()
        if synonym != term.lower():  # Exclude the term itself from synonyms
            synonyms.add(synonym)

# Analyze term for each synonym
synonym_counts = {}
for synonym in synonyms:
    count = analyze_term(csv_file_path, synonym)[1]
    synonym_counts[synonym] = count

# Print analysis results
print(f"1. Average sentiment for tweets containing the term '{term}': {avg_sentiment}")
print(f"2. Total occurrences of the term '{term}': {term_count}")
print(f"3. Highest sentiment tweet for the term '{term}': {highest_sentiment_tweet}")
print(f"4. Lowest sentiment tweet for the term '{term}': {lowest_sentiment_tweet}")
print(f"5. Synonyms for the term '{term}':")
for synonym, count in synonym_counts.items():
    print(f"   - '{synonym}' ({count} occurrences)")