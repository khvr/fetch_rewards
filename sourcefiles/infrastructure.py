import boto3
import yaml
import sys
from image import Image
import botocore
import socket
import time


with open(r'../configuration.yaml') as file:
    configuration = yaml.full_load(file)

server_configuration = configuration['server']
users_configuration = server_configuration['users']

try:
    resource_ec2 = boto3.client("ec2")
    ec2 = boto3.resource('ec2')
except botocore.exceptions.NoRegionError as error:
    # Put your error handling logic here
    print("Please set you aws profile to set a region or use $aws configure")
    sys.exit(1)

"""
function create_user_data_script

This function creates the user data script to be executed on instance creation

@return: user_data script
"""

def create_user_data_script():
    try:
        with open("../user_data.sh", "r") as f:
            lines=f.readlines()
    except OSError:
        print ("Could not open/read file:")
        sys.exit()
    with open("../user_data.sh", "w") as f:
        for i in range (0,19):
            f.write(lines[i])
    with open("../user_data.sh", "a+") as f:
        for user in users_configuration:
            username = user['login']
            user_public_key = user['ssh_key']
            f.write(f"\nadduser {username}\nusermod -a -G shared {username}\nbash -c 'echo \"{user_public_key}\">>/home/{username}/.ssh/authorized_keys'\n")
    with open("../user_data.sh", "r")as reader:
        user_data=reader.read()
    return user_data

"""
function create_ec2_instance

This function gets userdata, gets the ami, creates and waits for an instances by passing various
parameters as a part of configuration.yaml

@param user_data: The user_data script thats passed on instance creation
@return: public_ip_address, the public ip address of the instance
@raise Exception: raises an exception
"""
def create_ec2_instance(user_data):
    region = server_configuration['region'] 
    ami_type = server_configuration['ami_type']
    architecture = server_configuration['architecture']
    root_device_type = server_configuration['root_device_type']
    virtualization_type = server_configuration['virtualization_type']
    image=Image()
    image_id=image.amazon_ami(ami_type,region,architecture,root_device_type,virtualization_type,resource_ec2)

    try:  

        response=resource_ec2.run_instances(
            BlockDeviceMappings=[
            {
                'DeviceName': server_configuration['volumes'][0]['device'],
                'Ebs': {
                    'DeleteOnTermination': True,
                    'VolumeSize': server_configuration['volumes'][0]['size_gb'],
                    'VolumeType': 'gp2',
                }
            },
            {
                'DeviceName': server_configuration['volumes'][1]['device'],
                'Ebs': {
                    'DeleteOnTermination': True,
                    'VolumeSize': server_configuration['volumes'][1]['size_gb'],
                    'VolumeType': 'gp2',
                }
            }
            ],
            InstanceType=server_configuration['instance_type'],
            ImageId=image_id,
            MinCount= server_configuration['min_count'],
            MaxCount= server_configuration['max_count'],
            UserData=user_data,
            # KeyName= <The key pair name for defualt ec2-user>  server_configuration['default_user_key_pair'],
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'fetch_rewards_instance'
                        },
                    ]
                },
            ],

        )

        # print(response)
            # check if EC2 instance was created successfully
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            InstanceId = response['Instances'][0]['InstanceId']
            print ("***Successfully created instance! Instance Id: " + InstanceId+" and waiting for instance to be up...")
            retries = 10
            retry_delay=10
            retry_count = 0
            instance = ec2.Instance(id=InstanceId)
            instance.wait_until_running()
            while retry_count <= retries:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((instance.public_ip_address,22))
                if result == 0:
                    print("Instance is UP & accessible on port 22, the IP address is:  ",instance.public_ip_address)
                    return instance.public_ip_address
                    break
                else:
                    print("instance is still down retrying . . . ")
                    time.sleep(retry_delay)
            

    except Exception as e:
        print('***Failed to create the instance...')
        print(type(e), ':', e)
        sys.exit(1)


"""
function ssh_string

This function gets public ip address of the created instance and prints a ssh
string for the user

@param public_ip_address, the public ip address of the instance
@return: None
"""
def ssh_string(Ip_addr):
    for user in users_configuration:
        username = user['login']
        print("\nSSH commands: \n")
        print(f"\n$ ssh -i <path to private key of {username}> {username}@{Ip_addr}")
    
"""
function main

This is the entry point for the script
@param none
@return: none
"""
def main():
    if server_configuration['ami_type'] == "amzn2" and server_configuration['volumes'][0]['type']== "ext4":
        sys.exit('Invalid root volume file system type for ami_type amzn2 valid values: xfs or change ami_type to amzn')
    elif server_configuration['ami_type'] == "amzn" and server_configuration['volumes'][0]['type']== "xfs":
        sys.exit('Invalid root volume file system type for ami_type amzn valid values: ext4 or change ami_type to amzn2')

    user_data=create_user_data_script()
    Ip_addr=create_ec2_instance(user_data)  
    ssh_string(Ip_addr)
    

if __name__ == "__main__":
    main()

