#!/usr/bin/env python

"""
Manager calls all patients with specific scenario with voximplant
"""

import requests
import json
import logging
import os.path
from pathlib import Path
import dotenv

from patients import PATIENTS

__version__ = '0.0.1'

BASE_DIR = Path(__file__).resolve().parent

dotenv_file = BASE_DIR / ".env"
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

VOXIMPLANT_ACCESS_TOKEN = os.getenv('VOXIMPLANT_ACCESS_TOKEN')
VOXIMPLANT_ACCOUNT_NAME = os.getenv('VOXIMPLANT_ACCOUNT_NAME')
VOXIMPLANT_SCENARIO_ID = os.getenv('VOXIMPLANT_SCENARIO_ID')
VOXIMPLANT_CALLER_ID = os.getenv('VOXIMPLANT_CALLER_ID')


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def run_scenario(phone: str, token: str):
    url = 'https://kitapi-ru.voximplant.com/api/v3/scenario/runScenario'
    params = {
        'access_token': VOXIMPLANT_ACCESS_TOKEN,
        'domain': VOXIMPLANT_ACCOUNT_NAME
    }
    a = requests.post(url, params=params, data={
        'scenario_id': VOXIMPLANT_SCENARIO_ID,
        'phone': phone,
        'variables': json.dumps({'token': token}),
        'caller_id': VOXIMPLANT_CALLER_ID
    }).json()
    if  a.get('success'):
        logger.info("Successfully sent call to number {}.".format(phone))
    else:
        logger.error("Error with call to {}. {}".format(phone, a))

def main():
    logger.info("Starting calling to patients...")
    for patient in PATIENTS:
        run_scenario(patient['phone'], patient['token'])
    logger.info("Done.")

if __name__ == "__main__":
    main()
