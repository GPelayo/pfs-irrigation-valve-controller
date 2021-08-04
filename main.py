#!/usr/bin/env python3
import config
import logging
import requests
import time
import RPi.GPIO as GPIO

pfs_log = logging.getLogger('pfs')
logging.basicConfig(filename='log.txt',
                    filemode='a',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

if __name__ == '__main__':
    attempts = 0
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(config.RELAY_SWITCH_GPIO, GPIO.OUT)
    GPIO.output(config.RELAY_SWITCH_GPIO, False)
    while True:
        url = f'{config.STATUS_URL}/valves/{config.VALVE_NAME}'
        try:
            status_json = requests.get(url).json()
        except requests.exceptions.MissingSchema:
            if attempts == config.ATTEMPTS:
                break
            elif attempts < config.ATTEMPTS:
                attempts += 1
                pfs_log.log(logging.WARNING, 'Can\'t connect to (%s). Tried %s/%s times.', url, attempts,
                            config.ATTEMPTS)
        else:
            if status_json.get('watering', False):
                GPIO.output(config.RELAY_SWITCH_GPIO, True)
                pfs_log.log(logging.INFO, 'Valve: Watering')
            else:
                GPIO.output(config.RELAY_SWITCH_GPIO, False)
                pfs_log.log(logging.INFO, 'Valve: Off')
            time.sleep(config.DELAY)
