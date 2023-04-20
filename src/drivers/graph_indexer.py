import typing as tp

import requests
import logging


class TheGraphIndexerStore:

    def __init__(self, url: str) -> None:
        self.url = url

    def send_request(self, query: str, variables: None) -> tp.Dict[str, tp.Any]:
        try:
            result = requests.post(
                self.url,
                json={'query': query, 'variables': None})
            response = result.json()
            return response['data']
        except KeyError:
            logging.warning(response)
            return None
