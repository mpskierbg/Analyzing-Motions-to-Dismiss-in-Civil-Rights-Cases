import pandas as pd
import requests
import time

# Load the raw data we saved from the acquisition script
df = pd.read_csv('output_with_opinion_ids_and_urls.csv')  # Or 'district_court_opinions_sample.csv'

print("Columns in raw data:", df.columns.tolist())

# 1. Select relevant columns from what we actually have.
columns_we_need = [
    'opinion_id', 'caseName', 'court', 'dateFiled', 'download_url', 'docketNumber'
]
# Check which of these columns actually exist in our DataFrame
available_columns = [col for col in columns_we_need if col in df.columns]
df = df[available_columns]

print("Using columns:", available_columns)

# 2. Convert 'dateFiled' to a datetime object if it exists
if 'dateFiled' in df.columns:
    df['dateFiled'] = pd.to_datetime(df['dateFiled'], errors='coerce') # Use 'coerce' to handle invalid dates gracefully
else:
    print("Warning: 'dateFiled' column not found. Creating a placeholder.")
    df['dateFiled'] = None

# 3. Drop duplicate opinions based on the 'id'
df = df.drop_duplicates(subset=['opinion_id'])

# 4. Create a new column for the full text and the outcome label.
df['plain_text'] = None  # We will fetch this
df['motion_granted'] = None  # We will label this manually

# 5. FETCH THE FULL TEXT FOR EACH OPINION
# This step is necessary because the search results don't include it.
API_KEY = "19e2018c0a5473097f90a331c8ca6efb1ecc3eeb"  # <<< REPLACE THIS WITH YOUR ACTUAL KEY
headers = {'Authorization': f'Token {API_KEY}'}

def fetch_opinion_text(opinion_id):
    """Fetches the full text for a given opinion_id from the CourtListener API."""
    if pd.isna(opinion_id):
        return None
    url = f"https://www.courtlistener.com/api/rest/v4/opinions/{opinion_id}/"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # The full text is often in the 'plain_text' field of the opinion endpoint
            return data.get('plain_text') or data.get('html') or data.get('html_lawbox') or "Text not available"
        else:
            print(f"Error fetching opinion {opinion_id}: Status {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed for opinion {opinion_id}: {e}")
        return None
    time.sleep(0.5)  # Be polite to the API between requests

print("\nFetching full text for opinions. This may take a few minutes...")
# Apply the function to each row to get the text. This makes multiple API calls.
df['plain_text'] = df['opinion_id'].apply(fetch_opinion_text)

# 6. Check if we successfully got text for most opinions
successful_fetches = df['plain_text'].notna().sum()
print(f"Successfully fetched text for {successful_fetches} out of {len(df)} opinions.")

# 7. For this portfolio project, let's ensure we have a good sample to label.
# Drop rows where we couldn't fetch the text.
df = df[df['plain_text'].notna()].copy()

# 8. Take a random sample of opinions to manually label.
# A smaller, well-labeled sample is better than a large, poorly-labeled one.
SAMPLE_SIZE = min(100, len(df))  # Let's start with 100 for manageability
df_sample = df.sample(n=SAMPLE_SIZE, random_state=42)

# 9. Save this sample to a new CSV file. This is the file you will MANUALLY label.
# We save the critical columns: the identifiers, the text, and an empty column for our label.
output_filename = 'sample_for_labeling_with_text.csv'
df_sample = df.sample(n=500, random_state=42) # random_state for reproducibility

# Save this sample to a new CSV file. This is the file you will MANUALLY label.
df_sample.to_csv('sample_for_labeling.csv', index=False)
print("Sample of 500 opinions saved to 'sample_for_labeling.csv'. Now for the manual work!")