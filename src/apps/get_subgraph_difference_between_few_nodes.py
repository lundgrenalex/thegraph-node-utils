import logging
from src.drivers import TheGraphIndexerStore
from src.repository import SubgraphsRepository
from src.settings.base import AppSettings
from src.uc import GetSubgraphDifferenceBetweenFewNodesUseCase


def run_app():

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
    subgraphs_repo = SubgraphsRepository(driver=graph_indexer_store)

    use_case = GetSubgraphDifferenceBetweenFewNodesUseCase(
        subgraphs_repository=subgraphs_repo)

    use_case.execute(None)


if __name__ == '__main__':
    run_app()
