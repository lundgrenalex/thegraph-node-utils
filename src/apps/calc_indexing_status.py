import logging

from src.drivers import FileStore
from src.repository import StatsRepository
from src.settings.base import AppSettings
from src.uc import CalcStatsUseCase


def run_app() -> None:

    # init settings
    settings = AppSettings()

    # logging setup
    logging.basicConfig(
        **settings.logging_settings.dict()
    )

    # init drivers
    stats_file_store = FileStore(
        file_dst=settings.file_store_dst)

    # init repos
    stats_repo = StatsRepository(
        driver=stats_file_store)

    # use case
    uc = CalcStatsUseCase(stats_repository=stats_repo)
    uc.execute(None)


if __name__ == '__main__':
    run_app()
