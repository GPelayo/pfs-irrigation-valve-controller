import config
import logging
import requests
import time

pfs_log = logging.getLogger('pfs')

if __name__ == '__main__':
    attempts = 0

    while True:
        url = f'{config.HOST}/api/status'
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
                pfs_log.log(logging.INFO, 'Valve: Watering')
                # if valve off trigger off:
                # else do nothing
            else:
                pfs_log.log(logging.INFO, 'Valve: Off')
            time.sleep(config.DELAY)
