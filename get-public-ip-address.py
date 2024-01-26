import boto3

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')

    instances = ec2_client.describe_instances(
        Filters=[
            {'Name': 'tag:Name', 'Values': ['Ant-Media-Server']},
            {'Name': 'instance-state-name', 'Values': ['running']}
        ]
    )

    if 'Reservations' in instances and instances['Reservations']:
        instance = instances['Reservations'][0]['Instances'][0]
    
        # Check if the instance has a public IP address
        if 'PublicIpAddress' in instance:
            public_ip = instance['PublicIpAddress']
            return {
                'statusCode': 200,
                'body': f"{public_ip}"
            }
        else:
            return {
                'statusCode': 404,
                'body': "Instance doesn't have a public IP address."
            }
    else:
        return {
            'statusCode': 404,
            'body': "No instances found with the specified tag."
        }
