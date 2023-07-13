from datetime import datetime
from signalwire.rest import Client as signalwire_client
import pandas as pd

# TODO: UPDATE WITH YOUR CREDENTIALS
ProjectID = "Project ID Goes Here"
AuthToken = "API Token Goes Here"
SpaceURL = "Your-Space-Name-Goes-Here.signalwire.com"

# TODO: UPDATE WITH DESIRED TIME & DATE
Start_Date = datetime(2023, 4, 1)
End_Date = datetime(2023, 5, 30)

client = signalwire_client(f"{ProjectID}", f"{AuthToken}", signalwire_space_url=f"{SpaceURL}")

faxes = client.fax.faxes.list(date_created_after=f"{Start_Date}", date_created_on_or_before=f"{End_Date}")

for record in faxes:
    print((record.date_created, record.status, record.sid))

d = []

# Appends all data from calls into an array
for record in faxes:
    d.append((record.from_, record.to, record.date_created, record.status, record.sid))

print(d)

df = pd.DataFrame(d, columns=('From', 'To', 'Date', 'Status', 'FaxSID'))

print('dataframe')
print('\n')
print(df)

df.to_csv('faxes.csv', index=False, encoding='utf-8')