from flask import Flask, jsonify, request
from flask_cors import CORS
import boto3

app = Flask(__name__)
CORS(app)

REGION = 'us-west-1'

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'alert-service'})

@app.route('/api/alerts/alarms', methods=['GET'])
def get_alarms():
    cloudwatch = boto3.client('cloudwatch', region_name=REGION)

    response = cloudwatch.describe_alarms()

    alarms = []
    for alarm in response['MetricAlarms']:
        alarms.append({
            'name': alarm['AlarmName'],
            'state': alarm['StateValue'],
            'metric': alarm['MetricName'],
            'description': alarm.get('AlarmDescription', 'No description'),
            'updated': alarm['StateUpdatedTimestamp'].strftime('%Y-%m-%d %H:%M:%S')
        })

    in_alarm = [a for a in alarms if a['state'] == 'ALARM']
    ok = [a for a in alarms if a['state'] == 'OK']
    insufficient = [a for a in alarms if a['state'] == 'INSUFFICIENT_DATA']

    return jsonify({
        'total': len(alarms),
        'in_alarm': len(in_alarm),
        'ok': len(ok),
        'insufficient_data': len(insufficient),
        'alarms': alarms
    })

@app.route('/api/alerts/notify', methods=['POST'])
def send_notification():
    sns = boto3.client('sns', region_name=REGION)
    data = request.json

    topic_arn = data.get('topic_arn')
    message = data.get('message')
    subject = data.get('subject', 'AWS Operations Alert')

    sns.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject=subject
    )

    return jsonify({'status': 'notification sent'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)
