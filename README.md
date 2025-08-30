Project Overview

This project analyzes trends in federal district court rulings on Motions to Dismiss in civil rights cases brought under 42 U.S.C. § 1983. It mimics the core workflow of a Legal Data Analyst at Lex Machina, involving data acquisition via API, manual legal review, SQL analysis, and visualization.
Prerequisites

    Python 3.8+ installed on your system.

    A free CourtListener API key.

    Basic knowledge of the command line/terminal.

Setup & Installation

    Clone the repository:
    bash

git clone <your-repo-url>
cd <your-repo-name>

Create a virtual environment (recommended):
bash

# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

Install the required Python packages:
bash

    pip install -r requirements.txt

    (The requirements.txt file should contain: requests pandas matplotlib seaborn)

Configuration

    Get your API Key:

        Register for a free account at CourtListener.com.

        Navigate to your profile's API Tokens section and generate a new token.

    Set your API Key:

        Open the 01_data_acquisition.py script.

        Find the line that says API_KEY = "YOUR_API_KEY_HERE".

        Replace the placeholder text with your actual API key, keeping it inside the quotes.

        ⚠️ Important: Add api_key.py to your .gitignore file to avoid accidentally committing your secret key to GitHub.

Usage: Running the Analysis Pipeline

Execute the scripts in the following order:

1. Data Acquisition
This script fetches raw metadata for relevant court opinions from the CourtListener API.
bash

python 01_data_acquisition.py

    What it does: Searches for opinions related to "motion to dismiss" and "42 U.S.C. § 1983". The results are saved to raw_opinions_data.csv.

    Note: The API's court filter can be unreliable. This script fetches a broad dataset and filters for district courts programmatically in the next step.

2. Data Cleaning & Sampling
This script fetches the full text for each opinion and prepares a sample for manual review.
bash

python 02_data_cleaning.py

    What it does:

        Loads raw_opinions_data.csv.

        Makes individual API calls to fetch the full text (plain_text) for each opinion using its cluster_id.

        Creates a manageable random sample of opinions and saves it to sample_for_labeling.csv.

    Expectation: This step will take some time due to rate-limiting pauses between API calls.

3. Manual Labeling (Critical Step)
This is where you apply your legal expertise. This step cannot be automated.

    Open sample_for_labeling.csv in the spreadsheet software of your choice.

    For each row, read the plain_text of the judicial opinion.

    In the motion_granted column, label the outcome:

        1: Motion to Dismiss was Granted.

        0: Motion to Dismiss was Denied.

        -1: Outcome is unclear or opinion is irrelevant (will be filtered out).

    Save your changes to the CSV file.

4. Analysis & Visualization
This script analyzes your labeled data, runs SQL queries, and generates visualizations.
bash

python 03_analysis_and_viz.py

    What it does:

        Loads your manually labeled data from sample_for_labeling.csv.

        Filters out rows labeled -1.

        Performs SQL analysis to calculate grant rates, trends over time, and variations by circuit.

        Generates plots (grant_rate_trend.png, grant_rate_by_circuit.png) and saves them in the repository.

        Prints key findings to the console.

Files Overview

    01_data_acquisition.py: Fetches data from the CourtListener API.

    02_data_cleaning.py: Prepares data for manual labeling by fetching full text.

    03_analysis_and_viz.py: Performs data analysis and creates visualizations.

    sample_for_labeling.csv: Created by Step 2; used for manual labeling in Step 3.

    requirements.txt: List of Python dependencies.

    .gitignore: Specifies files to exclude from version control (e.g., api_key.py, *.csv).

Troubleshooting & Notes

    API Rate Limiting: The CourtListener API has strict rate limits for free tiers. If scripts fail with 429 or 401 errors, wait an hour before trying again.

    No Results Found: If the acquisition script finds zero results, try simplifying the search query in 01_data_acquisition.py (e.g., just "motion to dismiss") to test the connection.

    Column Errors: If you encounter a KeyError, run print(df.columns.tolist()) in your script to see the exact column names returned by the API and adjust your code accordingly.
