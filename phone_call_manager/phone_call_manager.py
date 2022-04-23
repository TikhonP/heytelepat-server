#!/usr/bin/env python

"""
Manager calls all patients with specific scenario with voximplant
"""

import requests
import json
import logging

__version__ = '0.0.1'

VOXIMPLANT_ACCESS_TOKEN = 'e32f56c144f157a4225122d3bb7efd48efad6496ff80adf38e98b8df323265db'
VOXIMPLANT_ACCOUNT_NAME = 'tikhon'
VOXIMPLANT_SCENARIO_ID = 33816
VOXIMPLANT_CALLER_ID = '+79581008748'

PATIENTS = [
    {'phone': '+79517287194', 'token': '6Hnojq9_fwS-yXaiawJ1og'},
    {'phone': '+79218418889', 'token': 'HxrQxl-1uxnBSjEhzP8jnw'},
    {'phone': '+79517288206', 'token': 'X9izNzavL2GFFzBAKa8qWw'},
    {'phone': '+79517228979', 'token': 'Wg7Vy7EHeF1N7-gXw6VPWQ'},
    {'phone': '+79517218799', 'token': 'Ee4g4azltSfZOS1m2cYvgg'},
    {'phone': '+79539052801', 'token': 'cO5gOtS50iqV6OjUkvibtw'},
    {'phone': '+79021489271', 'token': 'L9LaabVH6OMrbzAA3xUwcw'},
    {'phone': '+79602018075', 'token': 'CCnw_rT7BdBwThrDyVRAbQ'},
    {'phone': '+79524876078', 'token': 'CFpsegCJ2pvwuCQlzBGGtQ'},
    {'phone': '+79809963188', 'token': 'TG9ztGkNPET91vYRuQjnMw'},
    {'phone': '+79524806163', 'token': 'ocjot8-hVyxq-0PUosb-Kw'},
    {'phone': '+79524807855', 'token': 'osoXgIvw-oYQiqm5LHgASQ'},
    {'phone': '+79517228978', 'token': 'be79GyGGxhVs8g-1JksP-Q'},
    {'phone': '+79539058892', 'token': 'K0biieWo8ffAshmMIP447w'},

    # {'phone': '+79150187307', 'token': 'W3voQDYWS9LmHLP7Xz_eOg'},
    # {'phone': '+79163465407', 'token': 'W3voQDYWS9LmHLP7Xz_eOg'},
    # {'phone': '+79251286565', 'token': 'pMUFw-UXN6E-P1yHG7NcwA'},
    # {'phone': '+79636936003', 'token': 'pMUFw-UXN6E-P1yHG7NcwA'},
]

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
