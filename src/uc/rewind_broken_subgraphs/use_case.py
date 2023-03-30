import typing as tp
from src.uc.base import BaseUseCase
from src.repository import SubgraphsRepository, SubgraphsIndexingResult


class RewindBrokenSubgraphs(BaseUseCase):

    def __init__(self, subgraphs_repository: SubgraphsRepository) -> None:
        self.subgraphs_repository = subgraphs_repository

    def execute(self, uc_request: tp.Optional[tp.Any]) -> None:
        subgraphs_info: SubgraphsIndexingResult = self.subgraphs_repository.get_subgraphs()
        for subgraph in subgraphs_info.subgraphs:

            if subgraph.health != 'failed':
                continue

            if 'no connection to the server' not in subgraph.error.message:
                continue

            command = f'graphman rewind {subgraph.error.block_hash} {subgraph.error.block_number} {subgraph.hash}'

            # operation with failed subgraphs
            print(command)
