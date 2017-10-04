import boto
import time
import os
import credential
from boto.ec2.connection import EC2Connection
regions = boto.ec2.regions()

#step 1

#region = 'us-east-1'

#establish the connection to region
conn=boto.ec2.connect_to_region('us-east-1',aws_access_key_id=credential.Access_Key_Id,aws_secret_access_key=credential.Secret_Access_Key)



#step 2
 
# create a new key pair
key_name='keyfile'
KeyPair = conn.create_key_pair(key_name) 
KeyPair.save(' use your path here')
#check if the key pair exists
# try:
#     	KeyPair = conn.get_all_key_pairs(keynames=[key_name])[0]
# except conn.ResponseError, e:
#     if e.code == 'InvalidKeyPair.NotFound':
#         KeyPair = conn.create_key_pair(key_name) 
#         KeyPair.save('xxx')
#     else:
#             raise

#step 3
group_name = "pick your name"
#check if the security group exists
try:
    SecurityGroup = conn.get_all_security_groups(groupnames=[group_name])[0]
except conn.ResponseError, e:
    if e.code == 'InvalidGroup.NotFound':
    	#steo 4
        SecurityGroup = conn.create_security_group(name= group_name,description="My Web Application")
        SecurityGroup.authorize('icmp', -1, -1, '0.0.0.0/0')
        SecurityGroup.authorize('tcp', 22, 22, '0.0.0.0/0')
        SecurityGroup.authorize('tcp', 80, 80, '0.0.0.0/0')
        SecurityGroup.authorize('tcp', 8080, 8080, '0.0.0.0/0')

    else:
            raise




#step 5/6
#start a new instance
reservation= conn.run_instances(image_id = "ami-8caa1ce4",key_name = key_name,  instance_type='t1.micro', security_groups= ['pick your name'])

instance = reservation.instances[0]


#update the instance state
while instance.state == 'pending':
  time.sleep(0.1)
  instance.update()


publicip= instance.ip_address


print "-------------------------"
print "public DNS name is: %s" %instance.public_dns_name  
print "public IP is: %s" %publicip
print "instance ID is: %s" %instance.id

time.sleep(80)

os.system("scp -o StrictHostKeyChecking=no -i keyfile.pem /homes/l/lixuan6/lab1_group_6/lab4/table.db ubuntu@%s:~/" %publicip) 
os.system("scp -o StrictHostKeyChecking=no -i keyfile.pem /homes/l/lixuan6/lab1_group_6/lab4/frontend_NoGoogle.py ubuntu@%s:~/" %publicip) 
time.sleep(1)
# os.system("ssh -i key.pem ubuntu@%s  'sudo apt-get -y install sysstat dstat'" %publicip ) 
os.system("ssh -i keyfile.pem ubuntu@%s  'sudo apt-get -y install python-bottle'" %publicip ) 


print "-------------------------"
print "public DNS name is: %s" %instance.public_dns_name  
print "public IP is: %s" %publicip
print "instance ID is: %s" %instance.id
os.system("ssh -i keyfile.pem ubuntu@%s  'python frontend_NoGoogle.py'" %publicip) 







