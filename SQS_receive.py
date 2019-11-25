import hashlib
import time
import boto3

f1 = open("./ttt1.txt", "w")
f1.write("run"+"\n")
f = open("./out2.txt","w")

sqs = boto3.client("sqs")
response = sqs.get_queue_url(QueueName="Task_Q.fifo")

queue_url = response["QueueUrl"]

for receive in range(1, 4, 1):
    f1.write("run1" + "\n")
    content = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            "SentTimestamp"
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            "All"
        ],
        VisibilityTimeout=43100,
        WaitTimeSeconds=0
    )
    message = content["Messages"][0]
    receipt_handle = message["ReceiptHandle"]
    f1.write("run2" + "\n")
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )


    print("Received and deleted message: %s" % message)

    f.write("Received and deleted message: "+str(message)+"\n")
f.close()
f1.close()
