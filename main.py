#!/usr/bin/env python3
import logging
import os
import sys

import requests
import time
import RPi.GPIO as GPIO

pfs_log = logging.getLogger('pfs')
logging.basicConfig(filename='log.txt',
                    filemode='a',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

VALVE_NAME = os.environ.get('VALVE_NAME')
STATUS_URL = os.environ.get('STATUS_URL')
API_KEY = os.environ.get('API_KEY')
DELAY = int(os.environ.get('DELAY', 5))
MAX_ATTEMPTS = int(os.environ.get('MAX_ATTEMPTS', sys.maxsize))
RELAY_SWITCH_GPIO = int(os.environ.get('RELAY_SWITCH_GPIO'))


if __name__ == '__main__':
    attempts = 0
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAY_SWITCH_GPIO, GPIO.OUT)
    GPIO.output(RELAY_SWITCH_GPIO, False)
    headers = {
        'Content-type': 'application/json',
        'x-api-key': API_KEY
    }
    while True:
        url = f'{STATUS_URL}/valve/{VALVE_NAME}'
        try:
            status_json = requests.get(url, headers=headers).json()
        except requests.exceptions.MissingSchema:
            if attempts == MAX_ATTEMPTS:
                break
            elif attempts < MAX_ATTEMPTS:
                attempts += 1
                pfs_log.log(logging.WARNING, 'Can\'t connect to (%s). Tried %s/%s times.', url, attempts,
                            MAX_ATTEMPTS)
        else:
            if status_json.get('watering', False):
                GPIO.output(RELAY_SWITCH_GPIO, True)
                pfs_log.log(logging.INFO, 'Valve: Watering')
            else:
                GPIO.output(RELAY_SWITCH_GPIO, False)
                pfs_log.log(logging.INFO, 'Valve: Off')
            time.sleep(DELAY)
