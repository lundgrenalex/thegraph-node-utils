import logging
import time
import typing as tp

from pydantic import BaseModel

from src.drivers import TheGraphIndexerStore


class SubgraphError(BaseModel):
    handler: tp.Union[str, None] = None
    message: tp.Union[str, None] = None
    block_number: int = 0
    block_hash: tp.Union[str, None] = None


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
    error: SubgraphError = SubgraphError()
    features: tp.List[str] = []


class SubgraphsIndexingResult(BaseModel):
    check_date: int = int(time.time())
    subgraphs: tp.List[SubgraphIndexingStatus]
    length: int


class SubgraphsStat(BaseModel):
    data: tp.List[tp.Optional[SubgraphsIndexingResult]] = []


class SubgraphsRepository:

    def __init__(self, driver: TheGraphIndexerStore) -> None:
        self.driver = driver

    def __get_subgraphs(self) -> tp.Dict[str, tp.Any]:
        BASE_QUERY = """
        query {
                indexingStatuses {
                    subgraph
                    node
                    entityCount
                    health
                    synced
                    chains {
                        network
                        chainHeadBlock {
                            number
                        }
                        latestBlock {
                            number
                        }
                    }
                    fatalError {
                        handler
                        message
                        block {
                            number
                            hash
                        }
                    }
                }
        }
        """
        return self.driver.send_request(query=BASE_QUERY, variables=None)

    def get_subgraph_features(self, subgraph_id: str) -> tp.Dict[str, tp.Any]:
        BASE_QUERY = """
        {
            subgraphFeatures (subgraphId: "SUBGRAPH_ID") {
                features
            }
        }
        """.replace('SUBGRAPH_ID', subgraph_id)
        return self.driver.send_request(query=BASE_QUERY, variables=None)

    def get_hash_by_block_number(self, network: str, block_number: int) -> tp.Union[str, None]:
        BASE_QUERY = 'query {blockHashFromNumber(network: "NETWORK", blockNumber: BLOCK_NUMBER)}'.replace(
            'NETWORK', network).replace('BLOCK_NUMBER', str(block_number))
        try:
            return self.driver.send_request(query=BASE_QUERY, variables=None)['data']['blockHashFromNumber']
        except KeyError:
            return None

    def get_subgraphs(self,) -> SubgraphsIndexingResult:
        subgraphs = []
        subgraps_from_indexer = self.__get_subgraphs()['indexingStatuses']
        logging.debug('ALL SUBGRAPHS STATUSES ARE: ')
        logging.debug(subgraps_from_indexer)
        for subgraph in subgraps_from_indexer:
            if subgraph['fatalError']:
                subgraph_error = SubgraphError(
                    block_number=subgraph['fatalError']['block']['number'],
                    block_hash=subgraph['fatalError']['block']['hash'],
                    handler=subgraph['fatalError']['handler'],
                    message=subgraph['fatalError']['message'])
            else:
                subgraph_error = None
            subgraph_features = self.get_subgraph_features(
                subgraph_id=subgraph['subgraph'])['subgraphFeatures']['features']
            try:
                subgraph_status = SubgraphIndexingStatus(
                    name='XXX',  # TODO: Get the Name
                    hash=subgraph['subgraph'],
                    health=subgraph['health'],
                    synced=subgraph['synced'],
                    entities=subgraph['entityCount'],
                    head_block=subgraph['chains'][0]['chainHeadBlock']['number'],
                    latest_block=subgraph['chains'][0]['latestBlock']['number'],
                    network=subgraph['chains'][0]['network'],
                    node=subgraph['node'],
                    error=subgraph_error,
                    features=subgraph_features)
            except (TypeError, KeyError, IndexError) as e:
                logging.error(e)
                logging.info('WRONG SUBGRAPH INFO:')
                logging.info(subgraph)
                continue
            subgraphs.append(subgraph_status)
        return SubgraphsIndexingResult(
            subgraphs=subgraphs, length=len(subgraphs))
