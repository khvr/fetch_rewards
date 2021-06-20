import boto3
import sys
import botocore

from dateutil import parser

class Image:

    # def __init__(self, name, age):
    #     self.name = name
    #     self.age = age

    # def filter(self,ami_type,region):

    #     name_filter, description_filter = None, None
    #     if ami_type == "amzn2":
    #         name_filter= "amzn2-ami-hvm-*" 
    #         description_filter = "Amazon Linux 2 AMI*"
    #     elif ami_type== "amzn":
    #         name_filter= "amzn-ami-hvm-*"
    #         description_filter = "Amazon Linux AMI*"
    #     else:
    #         sys.exit(f'Invalid ami_type {ami_type}')
        

    """
    newest_image 

    This function keeps track of latest image from a list of images and return it
    @param list_of_images: The list of images obtained as a part of configuration
    @return: latest: The latest image
    """
    def newest_image(self, list_of_images):
        latest = None

        for image in list_of_images:
            if not latest:
                latest = image
                continue

            if parser.parse(image['CreationDate']) > parser.parse(latest['CreationDate']):
                latest = image

        return latest


    """
    amazon_ami 

    This function returns an ami id by applying filters
    @param ami_type,region: The region of ami id
    @param ami_type architecture: The architecture of ami
    @param ami_type root_device_type The root_device_type of ami
    @param ami_type virtualization_type The virtualization_type of ami
    @param ami_type client The instance of boto3 client
    @return: ami_id: The ami_id of the latest image
    """
    def amazon_ami(self, ami_type,region,architecture,root_device_type,virtualization_type,client):
        name_filter, description_filter = None, None
        # client = boto3.client('ec2', region_name=region)
        
        if ami_type == "amzn2":
            name_filter= "amzn2-ami-hvm-*" 
            description_filter = "Amazon Linux 2 AMI*"
        elif ami_type== "amzn":
            name_filter= "amzn-ami-hvm-*"
            description_filter = "Amazon Linux AMI*"
        else:
            sys.exit(f'Invalid ami_type {ami_type}')

        filters = [ 
            {
                'Name': 'name',
                # 'Values': ['amzn2-ami-hvm-*']
                'Values': [name_filter]
            },
            {
                'Name': 'description',
                # 'Values': ['Amazon Linux 2 AMI*']
                'Values': [description_filter]
            },
            {
                'Name': 'architecture',
                'Values': [architecture]
            },
            {
                'Name': 'owner-alias',
                'Values': ['amazon']
            },
            {
                'Name': 'owner-id',
                'Values': ['137112412989']
            },
            {
                'Name': 'state',
                'Values': ['available']
            },
            {
                'Name': 'root-device-type',
                'Values': [root_device_type]
            },
            {
                'Name': 'virtualization-type',
                'Values': [virtualization_type]
            },
            {
                'Name': 'hypervisor',
                'Values': ['xen']
            },
            {
                'Name': 'image-type',
                'Values': ['machine']
            } 
        ]
        try:
            response = client.describe_images(Owners=['amazon'], Filters=filters)
            source_image = self.newest_image(response['Images'])
            return source_image['ImageId']
        except botocore.exceptions.NoCredentialsError as error:
            print("Please set you aws profile to set a profile or use $aws configure")
            sys.exit(1)