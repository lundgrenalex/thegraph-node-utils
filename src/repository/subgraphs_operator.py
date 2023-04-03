import typing as tp
from src.drivers.indexer_rpc import IndexerRPCDriver


class SubgraphsOperatorRepository:

    def __init__(self, driver: IndexerRPCDriver) -> None:
        self.__driver = driver

    def create_subgraph(self, subgraph_name: str) -> tp.Dict[str, tp.Any]:
        return self.__driver.create_subgraph(subgraph_name)

    def deploy_subgraph(self, subgraph_name: str, ipfs_hash: str) -> tp.Dict[str, tp.Any]:
        return self.__driver.deploy_subgraph(subgraph_name, ipfs_hash)
