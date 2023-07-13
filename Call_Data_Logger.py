from datetime import datetime
from signalwire.rest import Client as signalwire_client
import pandas as pd

# TODO: UPDATE WITH YOUR CREDENTIALS
ProjectID = "Project ID Goes Here"
AuthToken = "API Token Goes Here"
SpaceURL = "Your-Space-Name-Goes-Here.signalwire.com"

# TODO: UPDATE WITH DESIRED TIME & DATE
start_date = datetime(2023, 3, 1)
end_date = datetime(2023, 7, 30)

client = signalwire_client(ProjectID, AuthToken, signalwire_space_url=SpaceURL)

call_records = []
call_counts = {}
numbers = [(record.phone_number,) for record in client.incoming_phone_numbers.list()]

# Tracks the amount of numbers pulled for adding progress notifications in the console.
total_numbers = len(numbers)

for progress, number in enumerate(numbers, 1):
    # Retrieve completed calls for the current number (incoming and outgoing)
    calls_to = client.calls.list(start_time_after=f"{start_date}", start_time_before=f"{end_date}", to=f"{number}",
                                 status='completed')
    calls_from = client.calls.list(start_time_after=f"{start_date}", start_time_before=f"{end_date}", from_=f"{number}",
                                   status='completed')

    # Update the calls count for each unique phone number.
    call_counts[number] = call_counts.get(number, 0) + len(calls_to) + len(calls_from)

    # Append the call records.
    call_records.extend(
        [(record.from_formatted, record.to_formatted, record.start_time, record.status, record.sid, record.price)
         for record in calls_to] +
        [(record.from_formatted, record.to_formatted, record.start_time, record.status, record.sid, record.price)
         for record in calls_from]
    )

    # Print progress notifications
    print(f"Processing {progress}/{total_numbers} phone numbers...")

df = pd.DataFrame(call_records, columns=("From", "To", "Date", "Status", "CallSID", "Price"))

call_counts_df = pd.DataFrame({'Phone Number': list(call_counts.keys()), 'Total Calls': list(call_counts.values())})

# Calculate the total cost of calls
total_cost = df['Price'].sum()
formatted_cost = f"${total_cost:,.2f}"

combined_df = pd.concat([df, call_counts_df], axis=1)

# Save the combined DataFrame to a CSV file
combined_df.to_csv('Call_Logs.csv', index=False, encoding='utf-8')

print(f"\nThe total cost of calls in your selected date range is approximately {formatted_cost} USD."
      f" Check the Call_Logs.csv file for additional details!")