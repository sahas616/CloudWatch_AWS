#This script is to create a CloudWatch Alarm for instances with CPU utilization breaching threshold

import boto3
from datetime import datetime, timedelta
instance_ids = []
instance_metrics={}

cloudwatch = boto3.client('cloudwatch')
ec2 = boto3.client('ec2')
response = ec2.describe_instances(
    Filters=[
        {
            'Name': 'instance-state-name',
            'Values': [
                'running',
            ]
        },
    ],
)

for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instance_ids.append(instance['InstanceId'])

for instance_id in instance_ids:
    metrics = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
        StartTime=datetime.utcnow() - timedelta(hours=1),
        EndTime=datetime.utcnow(),
        Period=300,
        Statistics=['Average']
    )

    metrics_data =[]
    for datapoint in metrics['Datapoints']:
        metrics_data.append(datapoint['Average'])
    avg_metrics = sum(metrics_data)/len(metrics_data)

    if avg_metrics > 6:
        cloudwatch.put_metric_alarm(
            AlarmName='HighCPUUtilization',
            MetricName='CPUUtilization',
            Namespace='AWS/EC2',
            Statistic='Average',
            Period=300,
            Threshold=6,
            ComparisonOperator='GreaterThanOrEqualToThreshold',
            EvaluationPeriods=2,
            Dimensions=[
                {
                    'Name': 'InstanceId',
                    'Value': instance_id
                },
            ],
            AlarmActions=['arn:aws:sns:us-east-1:891377046509:cloudwatch-trigger-email']
        )

    #instance_metrics[instance_id] = avg_metrics

    