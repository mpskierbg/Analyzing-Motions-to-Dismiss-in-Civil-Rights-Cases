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
