import json
import requests

class RPC(object):
    def __init__(self, url: str, user: str, passwd: str) -> None:
        self.url = url
        self.user = user
        self.passwd = passwd
        self.request('ping')

    # Stolen from https://stackoverflow.com/questions/53073163/how-to-connect-with-bitcoin-rpc-through-python
    def request(self, method: str, params: list = []):
        payload = json.dumps({
            "jsonrpc": "1.0",
            "method": method,
            "params": params
        })
        return requests.post(self.url, auth=(self.user, self.passwd), data=payload).json()
