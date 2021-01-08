import os
import requests
from dotenv import load_dotenv

load_dotenv()


def is_mina_node_synced():
    try:
        endpoint = os.getenv('MINA_NODE_GRAPHQL_ENDPOINT')
        url = endpoint + '?query=query%20MyQuery%20%7B%0A%20%20daemonStatus%20%7B%0A%20%20%20%20syncStatus%0A%20%20%7D%0A%7D%0A'
        r = requests.get(url)
        r_json = r.json()
        sync_status = r_json['data']['daemonStatus']['syncStatus']
        return sync_status == 'SYNCED'
    except:
        return False


def is_slot_available():
    endpoint = os.getenv('SLOT_QUERY_ENDPOINT')
    r = requests.get(endpoint)
    r_json = r.json()
    return r_json['status'] == 0

