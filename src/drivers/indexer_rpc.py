import logging
import typing as tp
import requests


class IndexerRPCDriver:

    headers = {
        'Content-Type': 'application/json'
    }

    def __init__(self, indexer_rpc_url: str) -> None:
        self.indexer_rpc_url = indexer_rpc_url

    def __make_request(self, query: tp.Dict[str, tp.Any], method: str) -> tp.Dict[str, tp.Any]:
        RPC_QUERY = {"jsonrpc": "2.0", "id": "1", "method": method, "params": query}
        response = requests.post(
            url=self.indexer_rpc_url,
            json=RPC_QUERY,
            headers=self.headers,
            timeout=20)
        logging.info(response.text)
        return response.json()

    def create_subgraph(self, subgraph_name: str) -> tp.Dict[str, tp.Any]:
        return self.__make_request(
            query={'name': subgraph_name},
            method='subgraph_create'
        )

    def deploy_subgraph(self, subgraph_name: str, ipfs_hash: str) -> tp.Dict[str, tp.Any]:
        return self.__make_request(
            query={'name': subgraph_name, 'ipfs_hash': ipfs_hash},
            method='subgraph_deploy'
        )
