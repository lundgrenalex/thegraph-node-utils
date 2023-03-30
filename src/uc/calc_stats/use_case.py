import typing as tp

from src.repository import StatsRepository
from src.uc.base import BaseUseCase
from src.uc.calc_stats.models import SubgraphIndexingStatus


class CalcStatsUseCase(BaseUseCase):

    result: tp.List[SubgraphIndexingStatus] = []

    def __init__(self, stats_repository: StatsRepository) -> None:
        self.stats_repo = stats_repository

    def __get_subgraph_status_by_hash(
            self,
            subgraphs: tp.List[tp.Dict[str, tp.Any]],
            hash: str) -> tp.Union[tp.Dict[str, tp.Any], None]:
        for subgraph in subgraphs:
            if subgraph['hash'] == hash:
                return subgraph
        return None

    def __print_subgraps_info(
            self,
            name_stat: str,
            subgraps: tp.Dict[str, SubgraphIndexingStatus]) -> None:
        print(f'##### {name_stat.upper()} SUBGRAPHS ####\n')
        if not subgraps:
            print('None\n')
        for subgraph_hash in subgraps:
            print(f'Subgraph hash is {subgraph_hash}\nDetails:')
            print(subgraps[subgraph_hash])

    def __get_ids_healthy_subgrpaps(
            self,
            subgraphs: tp.List[tp.Any]
    ) -> tp.List[str]:
        result = []
        for subgraph in subgraphs:
            if subgraph['health'] == 'healthy':
                result.append(subgraph['hash'])
        return result

    def __get_healthy_subgraphs(
        self,
        subgraphs: tp.List[tp.Dict[str, tp.Any]],
        ids_for_healthy_subgraphs: tp.List[str],
    ) -> tp.List[tp.Dict[str, tp.Any]]:
        result = []
        for subgraph in subgraphs:
            if subgraph['hash'] in ids_for_healthy_subgraphs:
                result.append(subgraph)
        return result

    def __show_results(self) -> None:

        # filter subgraps
        stopped_subgraps = {}
        unhealthy_subgraphs = {}
        synced_subgraps = {}
        syncing_subgraphs = {}

        for subgraph in self.result:

            # stopped
            if subgraph.health == 'failed':
                stopped_subgraps[subgraph.hash] = subgraph
                continue

            # synced
            if subgraph.synced:
                synced_subgraps[subgraph.hash] = subgraph
                continue

            # unhealthy
            if subgraph.health == 'unhealthy':
                unhealthy_subgraphs[subgraph.hash] = subgraph

            # syncing subgraphs
            syncing_subgraphs[subgraph.hash] = subgraph

        print(f'Total subgraps count: {len(self.result)}\n')
        self.__print_subgraps_info('stopped', stopped_subgraps)
        self.__print_subgraps_info('unhealthy', unhealthy_subgraphs)
        self.__print_subgraps_info('synced', synced_subgraps)
        self.__print_subgraps_info('syncing', syncing_subgraphs)

    def execute(self, uc_request: tp.Optional[tp.Any]) -> None:

        checks = self.stats_repo.get()
        sorted_checks = sorted(checks['data'], key=lambda d: d['check_date'])

        # get healthy subgraphs only
        healthy_subgraphs_ids = self.__get_ids_healthy_subgrpaps(
            sorted_checks[-1]['subgraphs'])

        results_for_median = {}
        for check_id in range(0, len(sorted_checks)):

            try:
                current_subgraphs_check = sorted_checks[check_id]
                next_subgraphs_check = sorted_checks[check_id + 1]
            except IndexError:
                continue

            # filter only healthy
            current_subgraphs_check['subgraphs'] = self.__get_healthy_subgraphs(
                current_subgraphs_check['subgraphs'],
                healthy_subgraphs_ids)
            next_subgraphs_check['subgraphs'] = self.__get_healthy_subgraphs(
                next_subgraphs_check['subgraphs'], healthy_subgraphs_ids)

            # get median sync speed and estimation in days
            spent_time = next_subgraphs_check['check_date'] - \
                current_subgraphs_check['check_date']

            # get sync speed and estimation date in days
            for current_subgraph in current_subgraphs_check['subgraphs']:
                for next_subgraph in next_subgraphs_check['subgraphs']:
                    if current_subgraph['hash'] != next_subgraph['hash']:
                        continue

                    # get sync speed in min
                    sync_speed_per_min = ((
                        next_subgraph['latest_block'] - current_subgraph['latest_block']) / spent_time) * 60

                    try:
                        estimation_time_to_sync_chain = int(
                            next_subgraph['head_block'] / sync_speed_per_min / 60 / 24)
                    except ZeroDivisionError:
                        estimation_time_to_sync_chain = None

                    # reduse indexing error
                    if next_subgraph['hash'] not in results_for_median:
                        results_for_median[next_subgraph['hash']] = {
                            'sync_speed': 0,
                            'estimation_time_to_sync_chain': 0,
                        }

                    if not estimation_time_to_sync_chain:
                        continue

                    # store information
                    sync_speed = int((results_for_median[next_subgraph['hash']]['sync_speed'] + sync_speed_per_min) / 2)
                    estimation_time_to_sync_chain = int(
                        (results_for_median[next_subgraph['hash']]['estimation_time_to_sync_chain'] + estimation_time_to_sync_chain) / 2)
                    results_for_median[next_subgraph['hash']] = {
                        'sync_speed': sync_speed,
                        'estimation_time_to_sync_chain': estimation_time_to_sync_chain,
                    }

            # Get final results
            for subgraph in sorted_checks[-1]['subgraphs']:
                if subgraph['hash'] in results_for_median:
                    subgraph['sync_speed_per_min'] = results_for_median[
                        subgraph['hash']]['sync_speed']
                    subgraph['estimation_time_to_sync_chain'] = results_for_median[
                        subgraph['hash']]['estimation_time_to_sync_chain']
                self.result.append(SubgraphIndexingStatus(**subgraph))

            self.__show_results()
