import boto
import time
import os
import credential
import sys
from boto.ec2.connection import EC2Connection
regions = boto.ec2.regions()
#connect to region
conn=boto.ec2.connect_to_region('us-east-1',aws_access_key_id=credential.Access_Key_Id,aws_secret_access_key=credential.Secret_Access_Key)

#get all reservations in this region
reservations = conn.get_all_instances()
instances = []
for r in reservations:
    instances.extend(r.instances)

#get all instance in a list
instanceIDs= []
for i in instances:
    instanceIDs.append(i.id)

#print instance information
for i in range(len(instanceIDs)):
    print "index: %s instance id: %s state: %s" %(i, instanceIDs[i], instances[i].state)

#receive user input as string or integer
index = 0
userInput= input("What's the instance id that you want to terminate? Input can be the instance id as string or instance index as integer   ")
if type(userInput) == int:
    if userInput <= len(instanceIDs):
        terminate_instance = instanceIDs[userInput]
        index= userInput
    else:
        print "Index exceeds cureent instance list. Please try again with correct instance id"

if type(userInput) == str:
    
    for i in range(len(instanceIDs)):
        if instanceIDs[i]== userInput:
            terminate_instance = userInput
            index=i
            break

#process

print "Instance exists. Start to termination."
if  instances[index].state != "terminated":
    conn.terminate_instances(terminate_instance)

while instances[index].state != "terminated":
    time.sleep(0.5)
    instances[index].update()

print "%s state: %s" %(terminate_instance, instances[index].state)
print "Instance %s has been terminated successfully" %terminate_instance

   
