import boto3

sqs = boto3.client('sqs')

queue_url = 'https://sqs.us-east-2.amazonaws.com/102809568981/RaspiCommands.fifo'

# Receive message from SQS queue
response = sqs.receive_message(
    QueueUrl=queue_url,
    AttributeNames=[
        'SentTimestamp'
    ],
    MaxNumberOfMessages=1,
    MessageAttributeNames=[
        'All'
    ],
    VisibilityTimeout=0,
    WaitTimeSeconds=0
)

message = response['Messages'][0]
receipt_handle = message['ReceiptHandle']


print('Received and deleted message: %s' % message)