import requests
from urllib.parse import urlparse

class wrapper(object):
    """A wrapper for the cojin peerfinder rest api"""
    def __init__(self, url: str) -> None:
        """
        Args:
            url (str): The server root url (like https://localhost:8080/)"""
        parsed = urlparse(url)
        self.url = parsed.scheme + '://' + parsed.netloc
        requests.get(self.url + '/ping')

    def getPeers(self) -> list:
        """Get a list of top 10 peers"""
        return requests.get(self.url + '/getpeers').json()
    
    def postPeer(self, peerURL: str) -> None:
        """Post your peer in the server
        
        Args:
            peerURL (str): Your peer url (like a ngrok tunnel)"""
        requests.post(
            self.url + '/postpeer',
            json={'url': urlparse(peerURL).netloc}
        )
