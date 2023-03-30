import logging
import re
import typing as tp

from src.repository import SubgraphsIndexingResult, SubgraphsRepository
from src.repository.subgraphs import SubgraphIndexingStatus
from src.uc.base import BaseUseCase


class RewindBrokenSubgraphs(BaseUseCase):

    def __init__(self, subgraphs_repository: SubgraphsRepository) -> None:
        self.subgraphs_repository = subgraphs_repository
        self.commands: tp.List[str] = []

    def __log_wrong_subgraph(self, subgraph: tp.Any) -> None:
        logging.debug(f'Subgraph {subgraph.hash} filed!')
        logging.debug(f'Error for fubgraph {subgraph.hash} is:\n{subgraph.error}')

    def __get_subgraph_command_for_rewind(
        self,
        subgraph: SubgraphIndexingStatus,
        error_messages: tp.List[str],
        rollback_blocks_count: int = 0,
    ) -> None:
        search_pattern = '|'.join(error_messages)
        if not re.search(rf'{search_pattern}', subgraph.error.message):
            return None

        block_number = subgraph.error.block_number - rollback_blocks_count
        block_hash = self.subgraphs_repository.get_hash_by_block_number(subgraph.network, block_number)
        if not block_hash:
            logging.error(
                f'Cannot get block hash {block_hash} for block number {block_number} for {subgraph.network} network')
            return

        command = f'graphman rewind {subgraph.error.block_hash} {block_number} {block_hash}'
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

        # Display subgraphs for rewind
        print('\n')
        print('COMMANDS FOR REWIND ARE:')
        for command in self.commands:
            print(command)
