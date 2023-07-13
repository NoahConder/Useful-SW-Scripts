import base64
import pandas as pd
import requests
from datetime import datetime, timedelta

# TODO: UPDATE WITH YOUR CREDENTIALS
ProjectID = "Project ID Goes Here"
AuthToken = "API Token Goes Here"
SpaceURL = "Your-Space-Name-Goes-Here.signalwire.com"

# Converts your credentials into base64
auth_byte = f"{ProjectID}:{AuthToken}".encode("ascii")
base64_byte = base64.b64encode(auth_byte)
base64_auth = base64_byte.decode("ascii")

# API Request
url = f"https://{SpaceURL}/api/voice/logs"
params = {
    "page_size": 1000,
    "created_at[gte]": (datetime.now() - timedelta(days=60)).isoformat()  # Filter for the last two months
}
headers = {
    'Accept': 'application/json',
    'Authorization': f'Basic {base64_auth}'
}

calls_list = []

# Make the initial API request
print("Making API request...")
response = requests.get(url, headers=headers, params=params)
data = response.json()
calls = data['data']
calls_list.extend(calls)
print("API request successful. Retrieved", len(calls), "calls.")

# Pagination
while 'next' in data['links']:
    next_url = data['links']['next']
    response = requests.get(next_url, headers=headers)
    data = response.json()
    calls = data['data']
    calls_list.extend(calls)
    print("Retrieved", len(calls), "calls.")

# Create DataFrame from the list
calls_df = pd.DataFrame(calls_list, columns=['id', 'from', 'to', 'duration', 'charge_details'])

calls_df.to_csv("calls.csv", index=False)

print("Calls have been successfully saved to the CSV.")
