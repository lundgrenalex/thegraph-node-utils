from pydantic import AnyUrl, BaseSettings


class LoggingSettings(BaseSettings):
    level: str = 'INFO'
    format: str = '%(asctime)s %(levelname)s: %(message)s'


class AppSettings(BaseSettings):

    file_store_dst: str = './checks/store.json'
    indexer_graphql_url: AnyUrl = 'http://localhost:8030/graphql'
    indexer_jsonrpc_url: AnyUrl = 'http://localhost:8020/'
    logging_settings: LoggingSettings = LoggingSettings()

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
