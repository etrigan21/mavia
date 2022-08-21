import boto3
from dotenv import load_dotenv
import os
load_dotenv()

print(os.getenv("aws_access_id"))

client = boto3.client(
    "sns",
    aws_access_key_id=os.getenv("aws_access_id"),
    aws_secret_access_key=os.getenv("aws_secret_key"),
    region_name="ap-southeast-2"
)

try:
    client.publish(
    PhoneNumber="+639205822248",
    Message="Hello World!"
    )
except:
    print("something went wrong")


