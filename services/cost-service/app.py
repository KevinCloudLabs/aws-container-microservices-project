from flask import Flask, jsonify
from flask_cors import CORS
import boto3
from datetime import date, timedelta

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'cost-service'})

@app.route('/cost/summary', methods=['GET'])
def get_cost_summary():
    client = boto3.client('ce', region_name='us-east-1')

    today = date.today()
    yesterday = today - timedelta(days=1)

    # From January 1st to yesterday (Cost Explorer excludes today)
    start = '2026-01-01'
    end = yesterday.strftime('%Y-%m-%d')

    response = client.get_cost_and_usage(
        TimePeriod={'Start': start, 'End': end},
        Granularity='MONTHLY',
        Metrics=['UnblendedCost'],
        GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
    )

    results = []
    for time_period in response['ResultsByTime']:
        for group in time_period['Groups']:
            service = group['Keys'][0]
            amount = float(group['Metrics']['UnblendedCost']['Amount'])
            if amount > 0:
                existing = next((r for r in results if r['service'] == service), None)
                if existing:
                    existing['cost'] += amount
                else:
                    results.append({'service': service, 'cost': amount})

    for r in results:
        r['cost'] = round(r['cost'], 2)

    results = [r for r in results if r['cost'] > 0]
    results.sort(key=lambda x: x['cost'], reverse=True)
    total = round(sum(r['cost'] for r in results), 2)

    return jsonify({
        'period': f"{start} to {end}",
        'total': total,
        'breakdown': results
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
