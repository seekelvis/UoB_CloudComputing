import datetime
import logging
import time
import math
import boto3
from botocore.exceptions import ClientError




C90 = [12714.1,
6675.537,
5265.242,
3569.399,
2483.243,
2255.107,
2064.594,
1846.565,
1685.99,
1550.257,
1421.047,
1359.144,
1217.938,
1083.227,
928.8454,
878.3075,
843.16,
827.4928,
796.6275,
771.7888,
746.1408,
697.2714,
641.1264,
619.4288,
619.6531,
595.7821,
547.0214,
532.4566,
520.2646,
504.5949]
C95 = [12716.17 ,
6678.418    ,
5267.568    ,
3572.02 ,
2485.572    ,
2259.055    ,
2067.58 ,
1849.499    ,
1689.72 ,
1554.485    ,
1424.882    ,
1363.161    ,
1221.569    ,
1087.4  ,
934.1769    ,
884.5048    ,
850.9546    ,
835.9109    ,
803.4244    ,
778.8879    ,
753.8994    ,
705.2746    ,
650.7317    ,
627.727 ,
626.498 ,
604.7422    ,
556.4301    ,
542.6807    ,
530.129 ,
515.078 ]
C99 = [12717.5  ,
6680.257    ,
5269.054    ,
3573.695    ,
2487.059    ,
2261.576    ,
2069.486    ,
1851.372    ,
1692.102    ,
1557.185    ,
1427.331    ,
1365.727    ,
1223.888    ,
1090.065    ,
937.5819    ,
888.4627    ,
855.9326    ,
841.2872    ,
807.7652    ,
783.4217    ,
758.8545    ,
710.3859    ,
656.8662    ,
633.0267    ,
630.8694    ,
610.4647    ,
562.439 ,
549.2104    ,
536.4289    ,
521.7731    ]
C = [C90,C95, C99]
def setWayOfStart():
    print("""Choose the way you want to start:
        1) specify the num of VM 
        2) Let CND system specify the num of VM """)
    input_str = input()
    if not (input_str>='1' and input_str<='2'):
        print("please enter 1 or 2")
        return setWayOfStart()
    return  input_str
def setExpectedTime():
    print("""please enter the expected time ( a positive number larger than 925) :""")
    input_str = input()
    if float(input_str) % 1 != 0:
        print("please enter an integer")
        return setExpectedTime()
    if float(input_str) < 0:
        print("please enter a positive number")
        return setExpectedTime()
    D = int(float(input_str))
    return int(D)
def setConfidence():
    print("""please enter confidence(A\B\C) :
    A: 90
    B: 95
    C: 99""")
    input_str = input()
    if not (input_str>='A' and input_str<='C'):
        print("please enter A or B or C")
        return setConfidence()
    if input_str == 'A':
        return 0
    if input_str=='B':
        return 1
    if input_str=='C':
        return 2
def setDifficulty():
    print("please enter the Difficulty for hexadecimal zeros (D=1 for hexadecimal zeros equals D=4 for binary zeros)")
    input_str = input()
    if float(input_str) % 1 != 0:
        print("please enter an integer")
        return setDifficulty()
    if float(input_str) < 0:
        print("please enter a positive number")
        return setDifficulty()
    D = int(float(input_str))
    return int(D)
def setNumVM():
    print("please enter the number of VM  ")
    input_str = input()
    if float(input_str) % 1 != 0:
        print("please enter an integer")
        return setDifficulty()
    if float(input_str) < 0:
        print("please enter a positive number")
        return setDifficulty()
    D = int(float(input_str))
    return int(D)


Way = setWayOfStart()
if  Way == 2:
    #Let CND system specify the num of VM
    confidence = setConfidence()
    expectedTime = setExpectedTime()
    for i in range(14,0,-1):
        # print(i)
        if expectedTime < C[confidence][i]:
            break
    numVM = i+2;
    print("numVM = ", numVM)
else:
    # specify the num of VM by user
    numVM = setNumVM()
# numVM = 8
# DIFF = 8

DIFF = setDifficulty()

numTrunk = 1024
MAX_nonce = math.pow(2,32)  # 2^32 4294967296
trunk = int(math.pow(2,32)/numTrunk  )
numTask =numTrunk

ACCESS_KEY = """"""

image_id = 'ami-04b9e92b5572fa0d1'
instance_type = 't2.micro'
keypair_name = 'CC_key'
security_groups = ['CC_group']

sqs = boto3.client('sqs')
ec2_client = boto3.client('ec2')

user_data6 = ("""#!/bin/bash
touch /home/ubuntu/begin.txt
cd /home/ubuntu/
git clone https://github.com/seekelvis/UoB_CloudComputing.git
mkdir .aws

cat>/home/ubuntu/.aws/credentials<<EOF
%(ACCESS_KEY)s
EOF

cat>/home/ubuntu/.aws/config<<EOF
[default]
region = us-east-1
EOF

cat>/home/ubuntu/diff.txt<<EOF
%(DIFF)s
EOF

cd /root
mkdir .aws
cp /home/ubuntu/.aws/credentials /root/.aws/credentials
cp /home/ubuntu/.aws/config /root/.aws/config

cd /home/ubuntu/
sudo apt-get -y  update
sudo apt-get -y upgrade
sudo apt-get -y install python3-pip
pip3 install boto3 
pip3 install awscli


sudo python3 /home/ubuntu/UoB_CloudComputing/CNDinInstance.py
touch end.txt
""") % {'DIFF': DIFF, 'ACCESS_KEY':ACCESS_KEY}



def SQS_creak_ReadyTime():
    # create Task queue
    response = sqs.create_queue(
        QueueName='ReadyTime.fifo',
        Attributes={
            'DelaySeconds': '0',
            'MessageRetentionPeriod': '86400',
            'FifoQueue': 'true'
        }
    )
def SQS_creak_Task():
    # create Task queue
    response = sqs.create_queue(
        QueueName='Task.fifo',
        Attributes={
            'DelaySeconds': '0',
            'MessageRetentionPeriod': '86400',
            'FifoQueue': 'true'
        }
    )
def SQS_creak_Result():
    # create Result queue
    response = sqs.create_queue(
        QueueName='Result.fifo',
        Attributes={
            'DelaySeconds': '0',
            'MessageRetentionPeriod': '86400',
            'FifoQueue': 'true'
        }
    )
def SQS_send_Task():
    response = sqs.get_queue_url(QueueName='Task.fifo')
    queue_url = response['QueueUrl']

    # for n in range(0, 50):
    for n in range(0, numTask):
        sqs.send_message(
            QueueUrl=queue_url,
            DelaySeconds=0,
            MessageGroupId=str(n+time.time()),
            MessageDeduplicationId=str(n+time.time()),

            MessageAttributes={
                'Begin': {
                    'StringValue': str(n*trunk),
                    'DataType': 'String'
                },
                'End': {
                    'StringValue': str((n+1)*trunk),
                    'DataType': 'String'
                }
            },
            MessageBody=(
                str(n)
            )
        )
        # print(n)
def SQS_clear_Task():
    try:
        # initial
        response = sqs.get_queue_url(QueueName="Task.fifo")
        queue_url = response["QueueUrl"]
        # recieve
        for receive in range(1, 65536):

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
    except:
        print("clear all Tasks")
    return 0
def SQS_clear_Result():
    try:
        # initial
        response = sqs.get_queue_url(QueueName="Result.fifo")
        queue_url = response["QueueUrl"]
        # recieve
        while True:
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
    except:
        print("clear all Result")

    return 0
def SQS_recive_Result():
    try:
        response = sqs.get_queue_url(QueueName="Result.fifo")
        queue_url = response["QueueUrl"]
        # recieve
        for receive in range(1, 2):
            # print("debug:a")
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
            gold_nonce = int(message['Body'])
            numTask = int(message["MessageAttributes"]["num_Task"]["StringValue"])
            toc = float(message["MessageAttributes"]["toc"]["StringValue"])
            spend = float(message["MessageAttributes"]["spend"]["StringValue"])

            # sqs.delete_message(
            #     QueueUrl=queue_url,
            #     ReceiptHandle=receipt_handle
            # )

    except:
        # print("There is no result")
        return [-2,-2,-2,-2]
    else:
        return [gold_nonce, numTask, toc, spend]
        print("receive gold nonce")
def SQS_recive_Readytime():
    try:
        response = sqs.get_queue_url(QueueName="ReadyTime.fifo")
        queue_url = response["QueueUrl"]
        # recieve
        for receive in range(1, 2):
            # print("debug:a")
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
            tic_ins = float(message['Body'])

            # sqs.delete_message(
            #     QueueUrl=queue_url,
            #     ReceiptHandle=receipt_handle
            # )

    except:
        # print("There is no result")
        return -1
    else:
        return tic_ins
        print("receive gold nonce")
def SQS_purge_Task():
    try:
        sqs.purge_queue(
            QueueUrl=sqs.get_queue_url(QueueName="Task.fifo")['QueueUrl']
        )
    except:
        print("clear all Result")

    return 0
def SQS_purge_Result():
    try:
        sqs.purge_queue(
            QueueUrl=sqs.get_queue_url(QueueName="Result.fifo")['QueueUrl']
        )
    except:
        print("clear all Result")

    return 0
def SQS_purge_ReadyTime():
    try:
        sqs.purge_queue(
            QueueUrl=sqs.get_queue_url(QueueName="ReadyTime.fifo")['QueueUrl']
        )
    except:
        print("clear all ReadyTime")

    return 0


def create_ec2_instance(image_id, instance_type, keypair_name, security_groups, user_data):
    """Provision and launch an EC2 instance
    The method returns without waiting for the instance to reach
    a running state.
    :param image_id: ID of AMI to launch, such as 'ami-XXXX'
    :param instance_type: string, such as 't2.micro'
    :param keypair_name: string, name of the key pair
    :return Dictionary containing information about the instance. If error,
    returns None.
    """

    # Provision and launch the EC2 instance

    try:
        response = ec2_client.run_instances(ImageId=image_id,
                                            InstanceType=instance_type,
                                            KeyName=keypair_name,
                                            MinCount=numVM,
                                            MaxCount=numVM,
                                            SecurityGroups=security_groups,
                                            UserData=user_data
                                            )

    except ClientError as e:
        logging.error(e)
        return None
    return response['Instances'][0]

def EC2_terminate():
    ec2 = boto3.resource('ec2')
    ec2.instances.terminate()

def Log(nonce,spend,num_task):
    fl = open("./log.txt", "a+")
    fl.write("-------------------------------------------------\n")
    fl.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"\n")
    fl.write("diff          = " + str(DIFF) + "\n")
    fl.write("VM_num        = " + str(numVM) + "\n")
    fl.write("Trunk_num     = " + str(numTrunk) + "\n")
    fl.write("Task_num      = " + str(numTask) + "\n")
    fl.write("NO.x task     = " + str(num_task) + "\n")
    fl.write("gold nonce    = " + str(nonce) + "\n")
    fl.write("cost time     = " + str(spend) + "\n")
    fl.write("-------------------------------------------------\n")
    fl.close()

def main():

    SQS_creak_Task()
    SQS_creak_Result()
    SQS_creak_ReadyTime()

    create_ec2_instance(image_id, instance_type, keypair_name,
                        security_groups, user_data6)
    SQS_send_Task()
    print ("CND system has sent ", numTask, "Tasks.")
    ReadyNum = 0;
    tic_ins = 0;
    while (ReadyNum<numVM):
        tic_temp = SQS_recive_Readytime()
        if tic_temp != -1:
            if tic_ins == 0:
                tic_ins = tic_temp
            elif tic_ins > tic_temp:
                tic_ins = tic_temp
            ReadyNum = ReadyNum + 1
            print("ReadyNum = ", ReadyNum, "; tic_ins = ", tic_ins, "; tic_temp = ", tic_temp)


    gold_nonce = -1
    ins_done_num = 0; #the number of instances who had finished the mission but had not find the result
    toc_ins = 0;
    while (gold_nonce == -1 or gold_nonce == -2): #-1 means didn't find nonce ; -2 means didn't receive the result
        receive = SQS_recive_Result()
        gold_nonce = receive[0]
        num_task = receive[1]
        toc_temp =  receive[2]
        if toc_temp > toc_ins :
            toc_ins = toc_temp
        if num_task == -1:
            ins_done_num = ins_done_num + 1
            print(ins_done_num, " instances have finished mission; cost = ", receive[3])
            if ins_done_num == numVM:
                print("mission field")
                break

        # print("waiting for result...")

    print("gold nonce = ", gold_nonce)
    print ("cost time = ", toc_ins-tic_ins)
    print ("tic ", tic_ins)
    print("toc ",toc_ins)
    Log(gold_nonce,toc_ins-tic_ins,num_task)

    EC2_terminate()
    SQS_purge_Task()
    SQS_purge_Result()
    SQS_purge_ReadyTime()




if __name__ == '__main__':
    main()


