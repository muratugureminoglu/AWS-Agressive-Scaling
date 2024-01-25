import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    tag_key = 'Name'
    tag_value = 'Ant Media Server'

    instances = ec2.describe_instances(
        Filters=[
            {'Name': 'instance-state-name', 'Values': ['running']},
            {'Name': f'tag:{tag_key}', 'Values': [tag_value]}
        ]
    )

    if instances['Reservations']:
        response = {
            'statusCode': 200,
            'body': 'True'
        }
    else:
        response = {
            'statusCode': 500,
            'body': 'False'
        }

    return response

