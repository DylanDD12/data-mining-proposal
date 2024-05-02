import pandas as pd

# Load the CSV file into a DataFrame with 'latin-1' encoding and without header
df = pd.read_csv('cleaned_file.csv', encoding='latin-1', header=None)

# Extract all preprocessed tweets into a text file with each tweet on a new line
output_file_path = 'preprocessed_tweets.txt'

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for tweet in df.iloc[:, 5]:
        output_file.write(str(tweet).strip() + ' | ')