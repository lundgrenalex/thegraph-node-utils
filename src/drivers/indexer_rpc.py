import typing as tp
import requests


class IndexerRPCDriver:

    BASE_QUERY = {
        "jsonrpc": "2.0",
        "id": "1",
        "method": "--",
        "params": {}
    }

    def __init__(self, indexer_rpc_url: str) -> None:
        self.indexer_rpc_url = indexer_rpc_url

    def reassign(self, query: tp.Dict[str, tp.Any]) -> tp.Dict[str, tp.Any]:
        response = requests.post(url=self.indexer_rpc_url, json=req_data, headers=headers)
        return response.json()
