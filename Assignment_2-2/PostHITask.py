# Copyright 2017 Amazon.com, Inc. or its affiliates

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import boto3
import csv

# Before connecting to MTurk, set up your AWS account and IAM settings as
# described here:
# https://blog.mturk.com/how-to-use-iam-to-control-api-access-to-your-mturk-account-76fe2c2e66e2
#
# Follow AWS best practices for setting up credentials here:
# http://boto3.readthedocs.io/en/latest/guide/configuration.html

# Use the Amazon Mechanical Turk Sandbox to publish test Human Intelligence
# Tasks (HITs) without paying any money.  Sign up for a Sandbox account at
# https://requestersandbox.mturk.com/ with the same credentials as your main
# MTurk account.


#load key file
data=[]

with open('../rootkey.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        root = ''.join(row)
        data.append(root)

#print (data)

aws_access_key_id = data[0].split('=')[1]        #'YOUR_ACCESS_ID'
aws_secret_access_key = data[1].split('=')[1]    #'YOUR_SECRET_KEY'

#print(aws_access_key_id)
#print(aws_secret_access_key)

# By default, HITs are created in the free-to-use Sandbox
create_hits_in_live = False

environments = {
        "live": {
            "endpoint": "https://mturk-requester.us-east-1.amazonaws.com",
            "preview": "https://www.mturk.com/mturk/preview",
            "manage": "https://requester.mturk.com/mturk/manageHITs",
            "reward": "0.5"
        },
        "sandbox": {
            "endpoint": "https://mturk-requester-sandbox.us-east-1.amazonaws.com",
            "preview": "https://workersandbox.mturk.com/mturk/preview",
            "manage": "https://requestersandbox.mturk.com/mturk/manageHITs",
            "reward": "0.5"
        },
}
mturk_environment = environments["live"] if create_hits_in_live else environments["sandbox"]

# use profile if one was passed as an arg, otherwise
profile_name = sys.argv[1] if len(sys.argv) >= 2 else None
session = boto3.Session(profile_name=profile_name)
client = session.client(
    service_name='mturk',
    region_name='us-east-1',
    endpoint_url=mturk_environment['endpoint'],
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)

# Test that you can connect to the API by checking your account balance
user_balance = client.get_account_balance()

# In Sandbox this always returns $10,000. In live, it will be your acutal balance.
print ("Your account balance is {}".format(user_balance['AvailableBalance']))

# The question we ask the workers is contained in this file.
question_sample = open("setting.xml", "r").read()

# Example of using qualification to restrict responses to Workers who have had
# at least 80% of their assignments approved. See:
# http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_QualificationRequirementDataStructureArticle.html#ApiReference_QualificationType-IDs
worker_requirements = [{
    'QualificationTypeId': '00000000000000000040',
    'Comparator': 'GreaterThanOrEqualTo',
    'IntegerValues': [0],
    'RequiredToPreview': True,
}]

# Create the HIT
response = client.create_hit(
    MaxAssignments=3,
    LifetimeInSeconds=500000,
    AssignmentDurationInSeconds=600,
    Reward=mturk_environment['reward'],
    Title='Visual Storytelling',
    Keywords='question, answer, research, story',
    Description='Descript a short story from the photos.',
    Question=question_sample,
    QualificationRequirements=worker_requirements,
)

# Show HIT_ID, HIT worker interface, HIT result
hit_type_id = response['HIT']['HITTypeId']
hit_id = response['HIT']['HITId']
print ("\nCreated HIT: {}".format(hit_id))

print ("\nYou can work the HIT here:")
print (mturk_environment['preview'] + "?groupId={}".format(hit_type_id))

print ("\nAnd see results here:")
print (mturk_environment['manage'])
