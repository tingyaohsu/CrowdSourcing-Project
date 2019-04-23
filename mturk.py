import boto3
import csv

data=[]

with open('rootkey.csv', 'r') as csvFile:
	reader = csv.reader(csvFile)
	for row in reader:
		root = ''.join(row)
		data.append(root)
		#print(row)
print (data)


region_name = 'us-east-1'
aws_access_key_id = data[0].split('=')[1]    #'YOUR_ACCESS_ID'
aws_secret_access_key = data[1].split('=')[1]    #'YOUR_SECRET_KEY'

print(aws_access_key_id)
print(aws_secret_access_key)

endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

# Uncomment this line to use in production
# endpoint_url = 'https://mturk-requester.us-east-1.amazonaws.com'

client = boto3.client(
    'mturk',
    endpoint_url=endpoint_url,
    region_name=region_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)

# This will return $10,000.00 in the MTurk Developer Sandbox
print(client.get_account_balance()['AvailableBalance'])