import time
import json
import typing as tp

from pydantic import BaseModel, error_wrappers
from src.drivers import FileStore


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
    features: tp.List[str] = []


class SubgraphsIndexingResult(BaseModel):
    check_date: int = int(time.time())
    subgraphs: tp.List[SubgraphIndexingStatus]
    length: int


class SubgraphsStat(BaseModel):
    data: tp.List[tp.Optional[SubgraphsIndexingResult]] = []


class StatsRepository:

    def __init__(self, driver: FileStore) -> None:
        self.store = driver

    def save(self, stat_data: tp.Dict[str, tp.Any]):
        try:
            current_state = SubgraphsStat(**json.loads(self.store.get()))
        except json.decoder.JSONDecodeError:
            current_state = SubgraphsStat(data=[])
        current_state.data.append(SubgraphsIndexingResult(**stat_data))
        self.store.save(data=current_state.json())

    def get(self) -> tp.Dict[str, tp.Any]:
        try:
            data = SubgraphsStat(**json.loads(self.store.get()))
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            data = SubgraphsStat(data=[])
        return data.dict()
