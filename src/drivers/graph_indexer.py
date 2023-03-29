import typing as tp

import requests


class TheGraphIndexerStore:

    def __init__(self, url: str) -> None:
        self.url = url

    def send_request(self, query: str, variables: None) -> tp.Dict[str, tp.Any]:
        result = requests.post(
            self.url,
            json={'query': query, 'variables': None})
        return result.json()['data']
