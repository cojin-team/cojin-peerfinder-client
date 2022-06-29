import json
import requests

class RPC(object):
    """Simple yet useful bitcoinRPC wrapper"""
    def __init__(self, url: str, user: str, passwd: str) -> None:
        """
        Args:
            url (str): RPC server url
            user (str): RPC username
            passwd (str): RPC password
        """
        self.url = url
        self.user = user
        self.passwd = passwd
        self.request('ping') # won't create the RPC instance if the server refuses the connection

    # Stolen from https://stackoverflow.com/questions/53073163/how-to-connect-with-bitcoin-rpc-through-python
    def request(self, method: str, params: list[str] = []):
        """
        Args:
            method (str): The actual RPC command
            params (list[str]): Command params/arguments
        """
        payload = json.dumps({
            "jsonrpc": "1.0",
            "method": method,
            "params": params
        })
        return requests.post(self.url, auth=(self.user, self.passwd), data=payload).json()
