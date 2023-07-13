from datetime import datetime
from signalwire.rest import Client as signalwire_client
import pandas as pd
import csv

# TODO: UPDATE WITH YOUR CREDENTIALS
ProjectID = "Project ID Goes Here"
AuthToken = "API Token Goes Here"
SpaceURL = "Your-Space-Name-Goes-Here.signalwire.com"

# TODO: UPDATE WITH DESIRED TIME & DATE
Start_Date = datetime(2023, 4, 1)
End_Date = datetime(2023, 5, 30)

client = signalwire_client(f"{ProjectID}", f"{AuthToken}", signalwire_space_url=f"{SpaceURL}")

# TODO: VERIFY YOUR NUMBERS.CSV IS SETUP WITH THE DESIRED NUMBERS
numbers = []

with open("Numbers.csv", 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        number = row[0]
        number = number.replace("(", "").replace(")", "").replace(" ", "").replace("-", "")
        if not number.startswith("+"):
            number = "+1" + number
        numbers.append(number)
d = []
for i in numbers:
    calls_to = client.calls.list(start_time_after=f"{Start_Date}", start_time_before=f"{End_Date}", to=f"{i}", status='completed')
    calls_from = client.calls.list(start_time_after=f"{Start_Date}", start_time_before=f"{End_Date}", from_=f"{i}", status='completed')
    for record in calls_to:
        d.append((record.from_formatted, record.to_formatted, record.start_time, record.status, record.sid, record.price))
    for record in calls_from:
        d.append((record.from_formatted, record.to_formatted, record.start_time, record.status, record.sid, record.price))

df = pd.DataFrame(d, columns=("From", "To", "Date", "Status", "CallSID", "Price"))

total_cost = df['Price'].sum()
formatted_cost = f"${total_cost:,.2f}"
df.to_csv('Call_Logs.csv', index=False, encoding='utf-8')
print(f"\nThe total cost of calls in your selected date range is approximately {formatted_cost} USD."
      f" Check the Call_Logs.csv file for additional details!")

