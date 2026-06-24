from flask import Flask, jsonify
from flask_cors import CORS
import boto3

app = Flask(__name__)
CORS(app)

REGION = 'us-west-1'

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'resource-service'})

@app.route('/api/resources/summary', methods=['GET'])
def get_resources():
    ec2 = boto3.client('ec2', region_name=REGION)
    rds = boto3.client('rds', region_name=REGION)
    s3 = boto3.client('s3', region_name=REGION)

    ec2_response = ec2.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running', 'stopped']}]
    )
    instances = []
    for reservation in ec2_response['Reservations']:
        for instance in reservation['Instances']:
            name = next((tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'), 'Unnamed')
            instances.append({
                'id': instance['InstanceId'],
                'name': name,
                'type': instance['InstanceType'],
                'state': instance['State']['Name'],
                'az': instance['Placement']['AvailabilityZone']
            })

    rds_response = rds.describe_db_instances()
    databases = []
    for db in rds_response['DBInstances']:
        databases.append({
            'id': db['DBInstanceIdentifier'],
            'engine': db['Engine'],
            'status': db['DBInstanceStatus'],
            'class': db['DBInstanceClass']
        })

    s3_response = s3.list_buckets()
    buckets = []
    for bucket in s3_response['Buckets']:
        buckets.append({
            'name': bucket['Name'],
            'created': bucket['CreationDate'].strftime('%Y-%m-%d')
        })

    return jsonify({
        'region': REGION,
        'ec2_instances': instances,
        'rds_databases': databases,
        's3_buckets': buckets,
        'summary': {
            'ec2_count': len(instances),
            'rds_count': len(databases),
            's3_count': len(buckets)
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
