import requests
import json
import pandas as pd
import time # to pace our API requests

# Your API Key - DO NOT UPLOAD THIS TO GITHUB. We'll use a placeholder. 
API_KEY = "`YOUR_API_KEY_HERE`" 

# Base URL for the CourtListener API's search endpoint
base_url = "https://www.courtlistener.com/api/rest/v4/search/"

# Define our search parameters.
params = {
    'q': '("motion to dismiss") AND ("42 U.S.C. § 1983" OR "Section 1983")',
    'type': 'o', # o for opinions
    'court_id': 'usdists', # district courts
    'filed_after': '2019-01-01',
    'page_size': 100, # adjust as needed, will need to paginate
    }

# Headers to authenticate with our API key
headers = {'Authorization':  f'Token {API_KEY}'} # You need to register for a free key

# List to hold all our results across all pages
all_results = []

# Function to handle pagination
def get_all_pages(url, params, headers):
    print(url)
    page = 1
    while True:
        print(f"Fetching page {page}...")
        # Make the GET request to the API
        response = requests.get(url, params=params, headers=headers)
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Error! Status code: {response.status_code}")
            print(response.text)
            break

        # Parse the JSON response
        data = response.json()
        
        # Add the results from this page to our master list
        all_results.extend(data['results'])
        
        # Check if there is a 'next' page URL in the response
        if data.get('next'):
            # Update the params to get the next page. The API provides the full URL.
            # We use the 'next' URL provided by the API itself for simplicity.
            url = data['next']
            params = {} # Clear params because the 'next' URL has them all already.
        else:
            print("No more pages found.")
            break
            
        # Be a good citizen and pause between requests to avoid overwhelming the server
        time.sleep(1) # 1 second pause
        page += 1

# Start the fetching process
get_all_pages(base_url, params, headers)

# Convert the list of results to a Pandas DataFrame
print(f"Fetched {len(all_results)} total opinions.")
df_raw = pd.DataFrame.from_records(all_results)

# Let's see what columns we have
print(df_raw.columns.tolist())

# Save the raw data to a CSV file for safekeeping
df_raw.to_csv('raw_opinions_data.csv', index=False)
print("Raw data saved to 'raw_opinions_data.csv'.")