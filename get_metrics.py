import json
import typing as tp
from pydantic import BaseModel

subgraphs_stat: tp.Dict[str, tp.Any] = {}


class SubgraphError(BaseModel):
    handler: tp.Union[str, None]
    message: str
    block_number: int


class SubgraphIndexingStatus(BaseModel):
    name: str
    health: str
    synced: bool
    hash: str
    node: tp.Union[str, None]
    network: str
    head_block: int
    latest_block: int
    entities: int
    error: tp.Union[SubgraphError, None]
    sync_speed_per_min: tp.Union[float, None] = None
    estimation_time_to_sync_chain: tp.Union[int, None] = None

    def __repr_str__(self, join_str: str) -> str:
        result = f'Synced: {self.synced}\n'
        result += f'Head block: {self.head_block}\n'
        result += f'Latest Block: {self.latest_block}\n'
        result += f'Stored entities: {self.entities}\n'
        result += f'Error: {self.error}\n'
        result += f'Sync speed blocks/per min: {self.sync_speed_per_min}\n'
        result += f'Estimation time to sync all blocks: {self.estimation_time_to_sync_chain} days\n'
        return f'{result}'


with open('./checks.json', 'r') as f:
    result = json.loads(f.read())
    sorted_checks = sorted(result['data'], key=lambda d: d['check_date'])
    a_point = sorted_checks[0]
    b_point = sorted_checks[-1]

    spent_time = b_point['check_date'] - a_point['check_date']

    # filter subgraps
    stopped_subgraps = {}
    unhealthy_subgraphs = {}
    synced_subgraps = {}
    syncing_subgraphs = {}
    new_deployed_subgraphs = {}

    def get_subgraph_status_by_hash(
            subgraphs: tp.List[tp.Dict[str, tp.Any]],
            hash: str) -> tp.Union[tp.Dict[str, tp.Any], None]:
        for subgraph in subgraphs:
            if subgraph['hash'] == hash:
                return subgraph
        return None

    def print_subgraps_info(
            name_stat: str,
            subgraps: tp.Dict[str, SubgraphIndexingStatus]) -> None:
        print(f'##### {name_stat.upper()} SUBGRAPHS ####\n')
        if not subgraps:
            print('None\n')
        for subgraph_hash in subgraps:
            print(f'Subgraph hash is {subgraph_hash}\nDetails:')
            print(subgraps[subgraph_hash])

    def get_ids_healthy_subgrpaps(subgraphs: tp.List[tp.Any]) -> tp.List[str]:
        result = []
        for subgraph in subgraphs:
            if subgraph['health'] == 'healthy':
                result.append(subgraph['hash'])
        return result

    def get_healthy_subgraphs(
        subgraphs: tp.List[tp.Dict[str, tp.Any]],
        ids_for_healthy_subgraphs: tp.List[str],
    ) -> tp.List[tp.Dict[str, tp.Any]]:
        result = []
        for subgraph in subgraphs:
            if subgraph['hash'] in ids_for_healthy_subgraphs:
                result.append(subgraph)
        return result

    # get healthy subgraphs only
    healthy_subgraphs_ids = get_ids_healthy_subgrpaps(
        sorted_checks[-1]['subgraphs'])

    results_for_median = {}
    for check_id in range(0, len(sorted_checks)):

        try:
            current_subgraphs_check = sorted_checks[check_id]
            next_subgraphs_check = sorted_checks[check_id + 1]
        except IndexError:
            continue

        # filter only healthy
        current_subgraphs_check['subgraphs'] = get_healthy_subgraphs(
            current_subgraphs_check['subgraphs'], healthy_subgraphs_ids)
        next_subgraphs_check['subgraphs'] = get_healthy_subgraphs(
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
                results_for_median[next_subgraph['hash']] = {
                    'sync_speed': int((results_for_median[next_subgraph['hash']]['sync_speed'] + sync_speed_per_min) / 2),
                    'estimation_time_to_sync_chain': int((results_for_median[next_subgraph['hash']]['estimation_time_to_sync_chain'] + estimation_time_to_sync_chain) / 2),
                }

        print(results_for_median)

        # Get final results
        final_result = []
        for subgraph in sorted_checks[-1]['subgraphs']:
            if subgraph['hash'] in results_for_median:
                subgraph['sync_speed_per_min'] = results_for_median[
                    subgraph['hash']]['sync_speed']
                subgraph['estimation_time_to_sync_chain'] = results_for_median[
                    subgraph['hash']]['estimation_time_to_sync_chain']
            final_result.append(SubgraphIndexingStatus(**subgraph))

        for subgraph in final_result:

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

        print(f'Total subgraps count: {len(final_result)}\n')
        print_subgraps_info('stopped', stopped_subgraps)
        print_subgraps_info('unhealthy', unhealthy_subgraphs)
        print_subgraps_info('synced', synced_subgraps)
        print_subgraps_info('syncing', syncing_subgraphs)
