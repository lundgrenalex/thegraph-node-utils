import typing as tp
from src.uc.base import BaseUseCase
from src.repository import SubgraphsRepository


class CheckSubgraphsFromCsvFile(BaseUseCase):

    def __init__(self, subgraphs_repository: SubgraphsRepository) -> None:
        self.subgraphs_repository = subgraphs_repository

    def execute(self, uc_request: tp.Optional[tp.Any]) -> None:
        with open(uc_request['subgraphs_csv_file'], 'r') as subgraphs_file:
            while True:

                subgraph_data_from_file = subgraphs_file.readline()
                if not subgraph_data_from_file:
                    break

                subgraph_data = subgraph_data_from_file.split('|')
                subgraph_name = str(subgraph_data[0]).strip()
                subgraph_hash = str(subgraph_data[1]).strip()

                subgraph = self.subgraphs_repository.get_subgraph_by_hash(subgraph_hash)
                subgraph.name = subgraph_name

                if subgraph.error.message:
                    print(subgraph.json())
