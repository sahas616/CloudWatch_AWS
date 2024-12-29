import boto3
cloudwatch = boto3.client('cloudwatch',region="us-east-1")

cloudwatch.put_metric_alarm(
    AlarmName='HighCPUUtilization',
    MetricName='CPUUtilization',
    Namespace='AWS/EC2',
    Statistic='Average',
    Period=300,
    Threshold=80,
    ComparisonOperator='GreaterThanOrEqualToThreshold',
    EvaluationPeriods=2,
    Dimensions=[
        {
            'Name': 'InstanceId',
            'Value': 'i-07cc7650c14c477d0'
        },
    ],
    AlarmActions=['arn:aws:sns:us-east-1:891377046509:cloudwatch-trigger-email']
)