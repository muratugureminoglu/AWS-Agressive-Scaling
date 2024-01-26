import boto3, time

def wait_for_instances_running(auto_scaling_group_name):
    ec2_client = boto3.client('ec2')
    
    while True:
        instances = ec2_client.describe_instances(
            Filters=[
                {'Name': 'tag:Name', 'Values': ['Ant-Media-Server']},
                {'Name': 'instance-state-name', 'Values': ['running']}
            ]
        )
    
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                print(f"Instance ID: {instance['InstanceId']}, State: {instance['State']['Name']}")

                if instance['State']['Name'] == 'running':
                    print("Instance is running. Exiting the loop.")
                    return instances  # Return instances once they are running

        time.sleep(10)

def lambda_handler(event, context):
    autoscaling_client = boto3.client('autoscaling')
    asg_names = autoscaling_client.describe_auto_scaling_groups()
    asg_name = [group for group in asg_names['AutoScalingGroups'] if
                       'OriginGroup' in group['AutoScalingGroupName']]
    auto_scaling_group_name = [group['AutoScalingGroupName'] for group in asg_name][0]

    print(auto_scaling_group_name)

    origin_autoscaling_group = autoscaling_client.describe_auto_scaling_groups(
        AutoScalingGroupNames=[auto_scaling_group_name])

    new_desired_capacity = 1
    min_size = 1

    autoscaling_client = boto3.client('autoscaling')
    response = autoscaling_client.update_auto_scaling_group(
        AutoScalingGroupName=auto_scaling_group_name,
        DesiredCapacity=new_desired_capacity,
        MinSize=min_size
    )

    print(f"DesiredCapacity of Auto Scaling Group '{auto_scaling_group_name}' is set to {new_desired_capacity}")

    # Wait for instances to be in the "running" state
   # wait_for_instances_running(auto_scaling_group_name)

    instances = wait_for_instances_running(auto_scaling_group_name)

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
