import logging
import re
import typing as tp

from src.repository import SubgraphsIndexingResult, SubgraphsRepository
from src.uc.base import BaseUseCase


class RewindBrokenSubgraphs(BaseUseCase):

    def __init__(self, subgraphs_repository: SubgraphsRepository) -> None:
        self.subgraphs_repository = subgraphs_repository
        self.commands: tp.List[str] = []

    def __log_wrong_subgraph(self, subgraph: tp.Any) -> None:
        logging.debug(f'Subgraph {subgraph.hash} filed!')
        logging.debug(f'Error for fubgraph {subgraph.hash} is:\n{subgraph.error}')

    def __get_subgraph_command_for_rewind(
            self, subgraph: tp.Any, error_messages: tp.List[str]) -> tp.Union[str, None]:
        search_pattern = '|'.join(error_messages)
        if not re.search(rf'{search_pattern}', subgraph.error.message):
            return None
        command = f'graphman rewind {subgraph.error.block_hash} {subgraph.error.block_number} {subgraph.hash}'
        self.commands.append(command)

    def execute(self, uc_request: tp.Optional[tp.Any]) -> None:
        subgraphs_info: SubgraphsIndexingResult = self.subgraphs_repository.get_subgraphs()
        for subgraph in subgraphs_info.subgraphs:

            if subgraph.health != 'failed':
                continue

            self.__get_subgraph_command_for_rewind(subgraph, [
                'no connection to the server',
                'subgraph writer poisoned by previous error',
            ])

            self.__log_wrong_subgraph(subgraph)

        print('\n')
        print('COMMANDS FOR REWIND ARE:')
        for command in self.commands:
            print(command)
