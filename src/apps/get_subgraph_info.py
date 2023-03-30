import logging
import sys

from src.drivers import TheGraphIndexerStore
from src.repository import SubgraphsRepository
from src.settings.base import AppSettings
from src.uc import GetSubgraphInfoUseCase


def run_app() -> None:

    # init settings
    settings = AppSettings()

    # get subgraph hash
    subgraph_hash = sys.argv[1]

    # logging setup
    logging.basicConfig(
        **settings.logging_settings.dict()
    )

    # init drivers
    graph_indexer_store = TheGraphIndexerStore(
        url=settings.indexer_graphql_url)

    # init repositories
    subgraphs_repo = SubgraphsRepository(
        driver=graph_indexer_store)

    # init usecases
    use_case = GetSubgraphInfoUseCase(subgraphs_repository=subgraphs_repo)

    # execute usecases
    use_case.execute(uc_request=subgraph_hash)


if __name__ == '__main__':
    run_app()
