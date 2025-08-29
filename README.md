# Analyzing-Motions-to-Dismiss-in-Civil-Rights-Cases
This project directly addresses "Analyze rulings in federal district court" and "Identify trends using Lex Machina data."

Objective: To analyze the success rates of motions to dismiss in federal civil rights cases (e.g., Section 1983 cases) over the past 5 years and identify any relevant trends.

Data Acquisition:
* Source: We will use the CourtListener API (Free, from the Free Law Project). It has a vast collection of federal district court opinions.
* Method: We'll write a Python script to query the API for opinions from the last 5 years that contain specific keywords: "motion to dismiss", "1983", "civil rights", "42 U.S.C. § 1983".
* Code Snippet (Acquisition):
```python
import requests
import json
import pandas as pd
 base_url = "https://www.courtlistener.com/api/rest/v3/search/"
    params = {
        'q': '("motion to dismiss") AND ("1983" OR "civil rights")',
        'type': 'o', # o for opinions
        'court': 'dists', # district courts
        'filed_after': '2019-01-01',
        'page_size': 100, # adjust as needed, will need to paginate
    }
    headers = {'Authorization': 'Token YOUR_API_KEY_HERE'} # You need to register for a free key

    response = requests.get(base_url, params=params, headers=headers)
    data = response.json()
    results = data['results']
    # ... (code to handle pagination and extract the relevant fields)
    df = pd.DataFrame.from_records(results)
    df.to_csv('civil_rights_mtd_opinions.csv', index=False)
```

