"""gql schema: https://github.com/graphprotocol/graph-node/blob/master/server/index-node/src/schema.graphql"""

import typing as tp
import time
import requests
from pydantic import BaseModel
import json

BASE_URL = 'http://localhost:8030/graphql'

BASE_QUERY = """
query {
        indexingStatuses (limit: 100) {
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
                    }
                }
        }
}
"""


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


class SubgraphsIndexingResult(BaseModel):
    check_date: int = int(time.time())
    subgraphs: tp.List[SubgraphIndexingStatus]
    length: int


class SubgraphsStat(BaseModel):
    data: tp.List[tp.Optional[SubgraphsIndexingResult]] = []


result = requests.post(
    BASE_URL, json={'query': BASE_QUERY, 'variables': None})

subgraphs = []
subgraph_indexing_data = result.json()['data']['indexingStatuses']
for subgraph in subgraph_indexing_data:
    if subgraph['fatalError']:
        subgraph_error = SubgraphError(
            block_number=subgraph['fatalError']['block']['number'],
            handler=subgraph['fatalError']['handler'],
            message=subgraph['fatalError']['message'])
    else:
        subgraph_error = None

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
    )
    subgraphs.append(subgraph_status)

result = SubgraphsIndexingResult(subgraphs=subgraphs, length=len(subgraphs))

try:
    with open('./checks.json', 'r') as f:
        stats_data = SubgraphsStat(**json.loads(f.read()))
except (json.decoder.JSONDecodeError, FileNotFoundError):
    stats_data = SubgraphsStat(data=[])

with open('./checks.json', 'w') as f:
    stats_data.data.append(result)
    f.write(stats_data.json())
