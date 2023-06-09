import sys
import logging
from src.drivers import TheGraphIndexerStore
from src.repository import SubgraphsRepository
from src.settings.base import AppSettings
from src.uc import RewindBrokenSubgraphs


def run_app() -> None:
    # rewind subgraphs with specific error
    # Error: handler=None message='Failed to transact block operations:
    # store error: no connection to the server\t' block_number=16919676

    try:
        rollback_blocks_count = sys.argv[1]
    except IndexError:
        rollback_blocks_count = 0

    # init settings
    settings = AppSettings()

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
    use_case = RewindBrokenSubgraphs(subgraphs_repository=subgraphs_repo)

    # execute usecases
    use_case.execute({
        'rollback_blocks_count': rollback_blocks_count,
    })


if __name__ == '__main__':
    run_app()
