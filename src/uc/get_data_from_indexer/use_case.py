import typing as tp
from src.repository import (StatsRepository, SubgraphsIndexingResult,
                            SubgraphsRepository)
from src.uc.base import BaseUseCase


class GetDataFromIndexerUseCase(BaseUseCase):

    def __init__(
        self,
        subgraphs_repository: SubgraphsRepository,
        stats_repository: StatsRepository,
    ) -> None:
        self.subgraphs_repository = subgraphs_repository
        self.stats_repository = stats_repository

    def execute(self, uc_request: tp.Optional[tp.Any]) -> None:
        result: SubgraphsIndexingResult = self.subgraphs_repository.get_subgraphs()
        self.stats_repository.save(result.dict())
