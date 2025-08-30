import pandas as pd
import ast

# Read the CSV file
df = pd.read_csv('District courts.csv')

# Function to extract the first 'download_url' from the opinions string
def extract_download_url(opinions_str):
    try:
        # Convert the string to a Python list of dictionaries
        opinions_list = ast.literal_eval(opinions_str)
        # Extract the 'download_url' from the first dictionary in the list
        return opinions_list[0]['download_url']
    except (ValueError, SyntaxError, IndexError, KeyError):
        return None  # Handle cases where parsing fails or structure is unexpected

# Apply the function to the 'opinions' column
df['download_url'] = df['opinions'].apply(extract_download_url)

# Save the result to a new CSV (optional)
df.to_csv('output_with_download_urls.csv', index=False)

# Show the DataFrame with the new 'download_url' column
print(df[['download_url']])