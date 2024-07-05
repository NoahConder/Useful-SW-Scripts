import requests
import pandas as pd
import base64

# TODO Define the parameters
target_number = "+15553035555"
date = "2024-04-30"
direction = "from"  # Possible values are From or To

# TODO Enter your credentials
space = "example.signalwire.com"
project = "Project_ID"
api_token = "API_token"

# Base64 key
combined = f"{project}:{api_token}"
base64_result = base64.b64encode(combined.encode('utf-8')).decode('utf-8')

url = f"https://{space}/api/voice/logs"
params = {
    "created_on": f"{date}",
    "page_size": 1000,
    "page": 1  # Start with the first page
}
headers = {
    'Accept': 'application/json',
    'Authorization': f'Basic {base64_result}'
}
# List to store all filtered logs
all_filtered_logs = []

# Flag to indicate if there are more pages to retrieve
has_more_pages = True

# Loop to retrieve all pages
while has_more_pages:
    # Make the API request
    response = requests.get(url, headers=headers, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json().get('data', [])

        # Filter logs involving the target number in the "to/from" field
        filtered_logs = [log for log in data if target_number in log.get(f'{direction}', '')]

        # Append filtered logs to the list
        all_filtered_logs.extend(filtered_logs)

        # Check if there are more pages
        links = response.json().get('links', {})
        if 'next' in links:
            url = links['next']
        else:
            has_more_pages = False
    else:
        print("Failed to retrieve call logs")
        break

# Check if any logs were found
if all_filtered_logs:
    # Create DataFrame from filtered logs
    df = pd.DataFrame(all_filtered_logs)

    # Define CSV file name
    csv_file = f"call_logs_{date}.csv"

    # Write DataFrame to CSV
    df.to_csv(csv_file, index=False)

    print(f"Call logs involving {target_number} in the '{direction}' field have been saved to {csv_file}")
else:
    print(f"No call logs involving {target_number} found in the '{direction}' field")
