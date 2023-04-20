import json
import typing as tp
import logging
from src.uc.base import BaseUseCase
from src.repository import SubgraphsRepository


class GetSubgraphDifferenceBetweenFewNodesUseCase(BaseUseCase):

    def __init__(
        self,
        subgraphs_repository: SubgraphsRepository,
    ) -> None:
        self.subgraphs_repository = subgraphs_repository

    def __get_diff(self, subgraphs_store_data: tp.List[tp.List[str]]) -> None:
        A_HASHES = set([s for s in subgraphs_store_data[0]])
        B_HASHES = set([s for s in subgraphs_store_data[1]])
        unique_subgraps_for_a = list(A_HASHES - B_HASHES)
        unique_subgraps_for_b = list(B_HASHES - A_HASHES)
        print(
            f'Unique subgraps for 1st indexer only: {unique_subgraps_for_a}', '\n',
            f'Unique subgraps for 2nd indexer only: {unique_subgraps_for_b}'
        )

    def execute(self, uc_request: tp.Optional[tp.Any]) -> None:

        FILE_DIFF_DST = './checks/diff.json'

        try:
            with open(FILE_DIFF_DST, 'r') as diff_store:
                data_from_store: tp.List[tp.List[str]] = json.loads(diff_store.read())
        except FileNotFoundError:
            data_from_store = []

        # if already few
        if len(data_from_store) >= 2:
            logging.warn(
                f'Stats is ready, to start a new one please remove {FILE_DIFF_DST} and run app again.')
            self.__get_diff(data_from_store)
            return

        # update store
        new_hashes = self.subgraphs_repository.get_subgraphs_hashes()
        data_from_store.append(new_hashes)
        with open(FILE_DIFF_DST, 'w') as diff_store:
            diff_store.write(json.dumps(data_from_store))
        logging.info('RUN SCRIPT AGAIN!')
