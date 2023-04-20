import logging
import time
import typing as tp

from pydantic import BaseModel

from src.drivers import TheGraphIndexerStore


class SubgraphError(BaseModel):
    handler: str = ''
    message: str = ''
    block_number: int = 0
    block_hash: str = ''


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

    def __get_subgraph(self, subgraph_hash: str) -> tp.Dict[str, tp.Any]:
        BASE_QUERY = """
        query {
            indexingStatuses(subgraphs: ["SUBGRAPH_HASH"]) {
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
                nonFatalErrors {
                    handler
                    message
                    block {
                        number
                        hash
                    }
                }
            }
        }
        """.replace('SUBGRAPH_HASH', subgraph_hash)
        return self.driver.send_request(query=BASE_QUERY, variables=None)

    def get_subgraph_features(self, subgraph_id: str) -> tp.Dict[str, tp.Any]:
        BASE_QUERY = """
        {
            subgraphFeatures (subgraphId: "SUBGRAPH_ID") {
                features
            }
        }
        """.replace('SUBGRAPH_ID', subgraph_id)
        result = self.driver.send_request(query=BASE_QUERY, variables=None)
        return result['subgraphFeatures']['features'] if result else []

    def get_hash_by_block_number(self, network: str, block_number: int) -> tp.Union[str, None]:
        BASE_QUERY = 'query {blockHashFromNumber(network: "NETWORK", blockNumber: BLOCK_NUMBER)}'.replace(
            'NETWORK', network).replace('BLOCK_NUMBER', str(block_number))
        try:
            result = self.driver.send_request(query=BASE_QUERY, variables=None)
            return result['blockHashFromNumber']
        except KeyError:
            logging.error(f'{BASE_QUERY}\nAPI_RESPONSE: {result}')
            return None

    def get_subgraph_by_hash(self, subgraph_hash: str) -> tp.Union[SubgraphIndexingStatus, None]:
        try:
            subgraph = self.__get_subgraph(subgraph_hash)['indexingStatuses'][0]
            if subgraph['fatalError']:
                subgraph_error = SubgraphError(
                    block_number=int(subgraph['fatalError']['block']['number']),
                    block_hash=str(subgraph['fatalError']['block']['hash']),
                    handler=str(subgraph['fatalError']['handler']),
                    message=str(subgraph['fatalError']['message']))
            else:
                subgraph_error = SubgraphError()
            subgraph_features = self.get_subgraph_features(
                subgraph_id=subgraph['subgraph'])['subgraphFeatures']['features']
            return SubgraphIndexingStatus(
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
        except (KeyError, IndexError, TypeError):
            return None

    def get_subgraphs_hashes(self,) -> tp.List[str]:
        BASE_QUERY = """
        query {
                indexingStatuses {
                    subgraph
                }
        }
        """
        result = self.driver.send_request(query=BASE_QUERY, variables=None)
        return [s['subgraph'] for s in result['indexingStatuses']]

    def get_subgraphs(self,) -> SubgraphsIndexingResult:
        subgraphs = []
        subgraps_from_indexer = self.__get_subgraphs()['indexingStatuses']
        logging.debug('ALL SUBGRAPHS STATUSES ARE: ')
        logging.debug(subgraps_from_indexer)
        for subgraph in subgraps_from_indexer:
            if subgraph['fatalError']:
                subgraph_error = SubgraphError(
                    block_number=int(subgraph['fatalError']['block']['number']),
                    block_hash=str(subgraph['fatalError']['block']['hash']),
                    handler=str(subgraph['fatalError']['handler']),
                    message=str(subgraph['fatalError']['message']))
            else:
                subgraph_error = SubgraphError()

            # Grafting and etc
            subgraph_features = self.get_subgraph_features(
                subgraph_id=subgraph['subgraph'])

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
