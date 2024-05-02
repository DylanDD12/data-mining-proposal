import pandas as pd
import re

# Load the CSV file into a DataFrame with 'latin-1' encoding and without header
df = pd.read_csv('Wiki List of Terms.csv', encoding='latin-1', header=None)

# Extract terms from the first column, remove commas, and filter out those that are only one character long,
# not empty, and not NaN
terms = [str(term).strip().replace(',', '') for term in df.iloc[:, 0] if pd.notna(term) and str(term).strip() and len(str(term).strip()) > 1]

# Remove slashes, split words into new lines, and remove anything enclosed in brackets
filtered_terms = []
for term in terms:
    # Remove slashes
    term = term.replace('/', ' ')
    # Split words into new lines
    words = term.split()
    # Remove anything enclosed in brackets
    cleaned_words = [re.sub(r'\(.*?\)', '', word) for word in words]
    # Filter out terms that are two letters or shorter
    cleaned_words = [word.strip() for word in cleaned_words if len(word.strip()) > 3]
    filtered_terms.extend(cleaned_words)

# Write the filtered terms to a text file
output_file_path = 'filtered_terms.txt'
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for term in filtered_terms:
        output_file.write(term + '\n')