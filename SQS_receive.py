import hashlib
import time
import boto3

# f1 = open("./debug1.txt", "w")

f = open("./out_receive.txt","w")
f.write("debug:1"+"\n")
sqs = boto3.client("sqs")
f.write("debug:2"+"\n")
response = sqs.get_queue_url(QueueName="Task_Q.fifo")
f.write("debug:3"+"\n")
queue_url = response["QueueUrl"]
f.write("debug:4"+"\n")
for receive in range(1, 4, 1):
    f.write("debug:1" + "\n")
    print("debug:a")
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
    f.write("debug:2" + "\n")
    taskUnit = int(message['Body'])
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )



    print (str(taskUnit))
    # print("Received and deleted message: %s" % message)

    f.write("Received and deleted message: "+str(taskUnit)+"\n")
f.close()
# f1.close()
