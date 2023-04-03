import logging
import sys

from src.settings.base import AppSettings
from src.drivers import IndexerRPCDriver
from src.repository import SubgraphsOperatorRepository
from src.uc import DeploySubgraphWithIpfsHashUseCase


def run_app() -> None:

    subgraph_name = sys.argv[1]
    subgraph_ipfs_hash = sys.argv[2]

    # init settings
    settings = AppSettings()

    # logging setup
    logging.basicConfig(
        **settings.logging_settings.dict()
    )

    if any([not subgraph_ipfs_hash, not subgraph_name]):
        logging.error('Please, define subgraph name and ipfs hash correctly.')
        return

    # RPC indexer
    rpc_driver = IndexerRPCDriver(
        indexer_rpc_url=settings.indexer_jsonrpc_url)

    # repos
    subgraph_operator_repository = SubgraphsOperatorRepository(driver=rpc_driver)

    # use cases
    use_case = DeploySubgraphWithIpfsHashUseCase(subgraph_operator_repository)
    use_case.execute({
        'subgraph_name': subgraph_name,
        'subgraph_ipfs_hash': subgraph_ipfs_hash,
    })


if __name__ == '__main__':
    run_app()
