# filename: 03_analysis_and_viz.py
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the clean data
df = pd.read_csv('sample_for_labeling - sample_for_labeling.csv')

# 1. Create a SQLite database and connection
conn = sqlite3.connect('legal_analytics.db')

# 2. Load our DataFrame into a SQL table called 'civil_rights_mtd'
df.to_sql('civil_rights_mtd', conn, if_exists='replace', index=False)

# 3. Let's run some SQL queries to get insights!
print("=== OVERALL GRANT RATE ===")
query_overall = """
SELECT
    motion_granted,
    COUNT(*) AS number_of_cases,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM civil_rights_mtd), 2) AS percentage
FROM civil_rights_mtd
GROUP BY motion_granted
"""
result_overall = pd.read_sql_query(query_overall, conn)
print(result_overall)

print("\n=== GRANT RATE BY YEAR ===")
query_trend = """
SELECT
    strftime('%Y', dateFiled) AS year,
    COUNT(*) AS total_cases,
    SUM(motion_granted) AS granted_cases,
    ROUND(AVG(motion_granted), 3) AS grant_rate
FROM civil_rights_mtd
WHERE year IS NOT NULL
GROUP BY year
ORDER BY year
"""
result_trend = pd.read_sql_query(query_trend, conn)
print(result_trend)

print("\n=== GRANT RATE BY CIRCUIT (Top 5) ===")
query_circuit = """
SELECT
    circuit,
    COUNT(*) AS total_cases,
    SUM(motion_granted) AS granted_cases,
    ROUND(AVG(motion_granted), 3) AS grant_rate
FROM civil_rights_mtd
WHERE circuit IS NOT NULL AND circuit != 'Other'
GROUP BY circuit
ORDER BY total_cases DESC
LIMIT 5
"""
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# 4. Plot 1: Trend of Grant Rate Over Time
plt.figure()
# We need to convert the 'year' column from the query result to integers for a proper plot
result_trend['year'] = result_trend['year'].astype(int)
sns.lineplot(x='year', y='grant_rate', data=result_trend, marker='o', linewidth=2.5)
plt.title('Trend in Motion to Dismiss Grant Rates in Civil Rights Cases (2019-2023)')
plt.ylabel('Grant Rate')
plt.xlabel('Year')
plt.ylim(0, 1) # Grant rate is between 0 and 1
plt.tight_layout()
plt.savefig('grant_rate_trend.png')
plt.show()

# 6. Close the database connection
conn.close()