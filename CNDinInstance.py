import hashlib
import time
import boto3


found = 0
block = "COMSM0010cloud"
nonce = 65536
begin_nonce = 0
end_nonce = 4194304
sqs = boto3.client("sqs")

diff = -1
if diff == -1:
    fo = open("/home/ubuntu/diff.txt", "r")
    for line in fo.readlines():
        line = line.strip()
        print("data = ", int(line))
    fo.close()
    diff = int(line)

def ReciveTask():
    try:
        response = sqs.get_queue_url(QueueName="Task.fifo")
        queue_url = response["QueueUrl"]
        #recieve
        for receive in range(1, 2):
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
            Num_task = int(message["Body"])
            Begin = int( message["MessageAttributes"]["Begin"]["StringValue"])
            End = int(message["MessageAttributes"]["End"]["StringValue"])
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )
            return [Begin, End, Num_task]
    except:
        print("There is no task")
    else:
        print("receive new task")

    return 0

def CND(begin,end):
    checkstr = ""
    for i in range (0,diff):
        checkstr = checkstr + "0"
    print ("diff = ", diff)
    tic = time.time()
    for i in range(begin,end):
        # print(i)
        x = hashlib.sha256()
        y = hashlib.sha256()
        code = block + str(i)

        x.update(code.encode("utf-8"))
        temstr = x.hexdigest()
        y.update(temstr.encode("utf-8"))
        result = y.hexdigest()

        if result[0:diff] == checkstr:
            nonce = i
            found = 1
            return nonce
            break
    toc = time.time()
    spend = toc - tic

    # print("nonce = ", nonce)
    # print("time = %s " %(time))
    return -1

def SQS_send_Result(goldNonce, numTask):
    response = sqs.get_queue_url(QueueName="Result.fifo")
    queue_url = response["QueueUrl"]
    sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=0,
        MessageGroupId=str(goldNonce)+str(time.time()),
        MessageDeduplicationId=str(goldNonce)+str(time.time()),
        MessageAttributes={
            'num_Task': {
                'StringValue': str(numTask),
                'DataType': 'String'
            },
        },
        MessageBody=(
            str(goldNonce)
        )

    )

def main():
    nonce = -1;

    # diff = ReadDiff()

    # receiveTask

    while nonce == -1 :
        trunk = ReciveTask()
        nonce = CND(trunk[0],trunk[1])
    print(nonce)
    SQS_send_Result(nonce,trunk[2])

if __name__ == "__main__":
    main()


# f = open("./out.txt","w")
# f.write("gold nonce = "+str(nonce)+"\n")
# f.write("cost time = "+str(spend)+"\n")
# f.close()







