import emoji
import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_validator_status(project_name: str):
    if project_name == 'Desmos':
        endpoint = os.getenv('DESMOS_LCD_ENDPOINT')
        validator_address = os.getenv('DESMOS_VALIDATOR_ADDRESS')
        return _get_validator_status_rest(endpoint, validator_address)
    if project_name == 'Bluzelle':
        endpoint = os.getenv('BLUZELLE_GRAPHQL_ENDPOINT')
        validator_address = os.getenv('BLUZELLE_VALIDATOR_ADDRESS')
        return _get_validator_status_graphql(endpoint, validator_address)
    else:
        return 'Not valid project name.'


def _get_validator_status_rest(endpoint: str, validator_address: str):
    url = endpoint + '/staking/validators/' + validator_address
    r = requests.get(url)
    r_json = r.json()
    jailed = r_json['result']['jailed']
    status_code = r_json['result']['status']
    status = map_status(status_code)

    if is_validator_active(jailed, status_code):
        return emoji.emojize('Validator is active. :white_check_mark:')
    else:
        return emoji.emojize('Validator is inactive, please check. :x: ') \
                   + 'Jailed: {}, Status: {}'.format(jailed, status)


def _get_validator_status_graphql(endpoint: str, validator_address: str):
    query = """
    {
        validators {   
            valoper
            moniker
            jailed
        }
    }
    """
    r = requests.post(endpoint, json={'query': query})
    r_json = r.json()
    validators = r_json['data']['validators']
    for validator in validators:
        if validator['valoper'] == validator_address:
            if not validator['jailed']:
                return emoji.emojize('Validator is active. :white_check_mark:')
            else:
                return emoji.emojize('Validator is inactive, please check. :x: ') \
                       + 'Jailed: {}'.format(validator['jailed'])
    return emoji.emojize('Validator not found. :cry:')


def request_faucet(project_name: str):
    if project_name == 'Desmos':
        endpoint = os.getenv('DESMOS_FAUCET_ENDPOINT')
        validator_address = os.getenv('DESMOS_ACCOUNT_ADDRESS')
    else:
        return 'Not valid project name.'

    url = endpoint + '/airdrop'
    r = requests.post(url, json={'address': validator_address})
    if is_faucet_request_success(r.json()):
        return emoji.emojize('Request faucet succeed. :moneybag:') \
               + 'Tx Hash: {}'.format(r.json()['txhash'])
    else:
        return emoji.emojize('Request faucet failed, try it later. :cry:')


def map_status(status: int):
    return {
        0: 'Unbonded',
        1: 'Unbonding',
        2: 'Active'
    }.get(status, 'Unbonded')


def is_validator_active(jailed: bool, status: int):
    if jailed is False and status == 2:
        return True
    else:
        return False


def is_faucet_request_success(response_json):
    return response_json.get('txhash') is not None


