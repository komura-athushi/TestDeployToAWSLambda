import datetime
import http.client
import json

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

import boto3

ce_client = boto3.client('ce')

today = datetime.datetime.today().date()
first_day_of_this_month = today.replace(day=1)

import os
slack_webhook = os.environ['SLACK_WEBHOOK']


def lambda_handler(event, context):


    cost_and_usage_response = ce_client.get_cost_and_usage(
        TimePeriod={
            'Start': str(first_day_of_this_month),
            'End': str(today)
        },
        Granularity='MONTHLY',
        Metrics=['BlendedCost']
    )

    total_cost = float(cost_and_usage_response['ResultsByTime'][0]['Total']['BlendedCost']['Amount'])

    conn = http.client.HTTPSConnection('hooks.slack.com')
    headers = {
        'Content-Type': 'application/json'
    }
    body = json.dumps({
        'channel': '#講義_khrisさん',
        'text': f'本日のAWSの料金は{total_cost}$ですです。'
    })
    conn.request('POST', f'{slack_webhook}', body, headers)
    slack_response = conn.getresponse()
    conn.close()

    return


if __name__ == '__main__':
    import sys
    args = sys.argv
    lambda_handler('','')
