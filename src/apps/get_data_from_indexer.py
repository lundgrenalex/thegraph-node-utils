import logging
from src.drivers import FileStore, TheGraphIndexerStore
from src.repository import StatsRepository, SubgraphsRepository
from src.settings.base import AppSettings
from src.uc import GetDataFromIndexerUseCase


def run_app() -> None:

    # init settings
    settings = AppSettings()

    # logging setup
    logging.basicConfig(
        **settings.logging_settings.dict()
    )

    # init drivers
    graph_indexer_store = TheGraphIndexerStore(
        url=settings.indexer_graphql_url)

    stats_file_store = FileStore(
        file_dst=settings.file_store_dst)

    # init repositories
    subgraphs_repo = SubgraphsRepository(
        driver=graph_indexer_store)
    stats_repo = StatsRepository(
        driver=stats_file_store)

    # init usecases
    use_case = GetDataFromIndexerUseCase(
        subgraphs_repository=subgraphs_repo,
        stats_repository=stats_repo)

    # execute usecases
    use_case.execute(None)


if __name__ == '__main__':
    run_app()
