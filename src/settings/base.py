from pydantic import AnyUrl, BaseSettings


class AppSettings(BaseSettings):

    file_store_dst: str = './checks/store.json'
    indexer_graphql_url: AnyUrl = 'http://localhost:8030/graphql'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
