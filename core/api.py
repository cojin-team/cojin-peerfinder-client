import requests
from urllib.parse import urlparse

class wrapper(object):
    def __init__(self, url: str) -> None:
        parsed = urlparse(url)
        self.url = 'https://' + parsed.netloc
        requests.get(self.url + '/ping')

    def getPeers(self) -> list:
        return requests.get(self.url + '/getpeers').json()
    
    def postPeer(self, peerURL: str) -> None:
        requests.post(
            self.url + '/postpeer',
            json={'url': urlparse(peerURL).netloc}
        )
