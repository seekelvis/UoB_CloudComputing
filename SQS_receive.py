import hashlib
import time
import boto3

# diff = 4
# found = 0
# block = "COMSM0010cloud"
# nonce = 65536
# i = -1

# checkstr = ""
# for j in range (0,diff):
#     checkstr = checkstr + "0"

# tic = time.time();
# for j in range (0,nonce,1):
#     if found == 1:
#         break
#     for k in range(0,nonce,1):
#         i = i+1

#         x = hashlib.sha256()
#         y = hashlib.sha256()
#         code = block + str(i)
#         # code = block+"0000000000"
#         # print ("code= ",code)
#         x.update(code.encode("utf-8"))
#         temstr = x.hexdigest()
#         # print("temstr= ",temstr)

#         y.update(temstr.encode("utf-8"))
#         result = y.hexdigest()
#         # bin_result = hexstr2binstr(result)

#         # print("result= ", result)
#         # print("bin_reslut = ", bin_result)
#         # print("result[d] = ", result[0:2])
#         if result[0:diff] == checkstr:
#             found = 1
#             break
# toc = time.time();
# nonce = i
# # print >> "./out.txt", "nonce = ", nonce

# # print("nonce = ", nonce,file=f)
# spend = toc -tic
# f = open("./out.txt","w")
# f.write("gold nonce = "+str(nonce)+"\n")
# f.write("cost time = "+str(spend)+"\n")
# f.close()
sqs = boto3.client("sqs")
response = sqs.get_queue_url(QueueName="Task_Q.fifo")

queue_url = response["QueueUrl"]

for receive in range(1, 4, 1):
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

    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )

    print("Received and deleted message: %s" % message)
    f = open("./out2.txt","w")
    f.write("Received and deleted message: "+str(message)+"\n")
    f.close()
