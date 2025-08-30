import pandas as pd
import ast

# Read the CSV file
df = pd.read_csv('output_with_download_urls.csv')

# Function to extract the first 'id' from the opinions string
def extract_opinion_id(opinions_str):
    try:
        # Convert the string to a Python list of dictionaries
        opinions_list = ast.literal_eval(opinions_str)
        # Extract the 'id' from the first dictionary in the list
        return opinions_list[0]['id']
    except (ValueError, SyntaxError, IndexError, KeyError):
        return None  # Handle cases where parsing fails or structure is unexpected

# Apply the function to the 'opinions' column
df['opinion_id'] = df['opinions'].apply(extract_opinion_id)

# Save the result to a new CSV (optional)
df.to_csv('output_with_opinion_ids_and_urls.csv', index=False)

# Show the DataFrame with the new 'opinion_id' column
print(df[['opinion_id']])