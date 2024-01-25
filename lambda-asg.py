import boto3

def lambda_handler(event, context):
    autoscaling_client = boto3.client('autoscaling')
    asg_names = autoscaling_client.describe_auto_scaling_groups()
    asg_name = [group for group in asg_names['AutoScalingGroups'] if
                       'OriginGroup' in group['AutoScalingGroupName']]
    auto_scaling_group_name = [group['AutoScalingGroupName'] for group in asg_name][0]

    print(auto_scaling_group_name)

    origin_autoscaling_group = autoscaling_client.describe_auto_scaling_groups(
        AutoScalingGroupNames=[auto_scaling_group_name])

    new_desired_capacity = 0
    min_size = 0

    autoscaling_client = boto3.client('autoscaling')
    response = autoscaling_client.update_auto_scaling_group(
        AutoScalingGroupName=auto_scaling_group_name,
        DesiredCapacity=new_desired_capacity,
        MinSize=min_size
    )

    print(f"DesiredCapacity of Auto Scaling Group '{auto_scaling_group_name}' is set to {new_desired_capacity}")
    return {
        'statusCode': 200,
        'body': f"DesiredCapacity of Auto Scaling Group '{auto_scaling_group_name}' is set to {new_desired_capacity}"
    }
