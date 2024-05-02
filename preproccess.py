import pandas as pd
import re
import string

def clean_text(text):
    # Remove links starting with "https://"
    text = re.sub(r'https?://\S+', '', text)
    # Remove mentions starting with "@username"
    text = re.sub(r'@\w+', '', text)
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

# Load the CSV file into a DataFrame 
df = pd.read_csv('trainset.csv', encoding='latin-1', header=None)

# Clean the text in the tweet column
df.iloc[:, 5] = df.iloc[:, 5].apply(clean_text)

# Remove rows with empty tweets
df = df[df.iloc[:, 5].str.strip() != '']

# Save the cleaned DataFrame to a new CSV file
df.to_csv('cleaned_file.csv', index=False, header=False)