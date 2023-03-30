from pydantic import BaseModel
import typing as tp


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
    features: tp.List[str] = []

    def __repr_str__(self, join_str: str) -> str:
        result = f'Synced: {self.synced}\n'
        result += f'Head block: {self.head_block}\n'
        result += f'Latest Block: {self.latest_block}\n'
        result += f'Stored entities: {self.entities}\n'
        result += f'Error: {self.error}\n'
        result += f'Features: {self.features}\n'
        result += f'Sync speed blocks/per min: {self.sync_speed_per_min}\n'
        result += f'Estimation time to sync all blocks: {self.estimation_time_to_sync_chain} days\n'
        return f'{result}'
