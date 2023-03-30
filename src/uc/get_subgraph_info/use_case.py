import typing as tp

from src.repository import SubgraphsRepository
from src.uc.base import BaseUseCase


class GetSubgraphInfoUseCase(BaseUseCase):

    def __init__(self, subgraphs_repository: SubgraphsRepository) -> None:
        self.subgraphs_repository = subgraphs_repository

    def execute(self, uc_request: tp.Optional[tp.Any]) -> None:
        subgraph_hash = str(uc_request)
        result = self.subgraphs_repository.get_subgraph_by_hash(subgraph_hash).json()
        print(result)
