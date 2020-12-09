import emoji
import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_luaswap_user(address: str):
    endpoint = os.getenv('LUASWAP_QUERY_ENDPOINT')
    query = """
    {
        users(where:{address: """ + '"' + address + '"' + """}) {
            address
            amount
            id
        }
    }
    """
    r = requests.post(endpoint, json={'query': query})
    r_json = r.json()
    return r_json
