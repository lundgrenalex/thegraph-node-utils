import typing as tp

from src.uc.base import BaseUseCase
from src.repository import SubgraphsOperatorRepository


class DeploySubgraphWithIpfsHashUseCase(BaseUseCase):

    def __init__(self, subgraphs_operator_repo: SubgraphsOperatorRepository) -> None:
        self.__subgraphs_operator_repo = subgraphs_operator_repo

    def execute(self, uc_request: tp.Optional[tp.Any]) -> None:
        self.__subgraphs_operator_repo.create_subgraph(uc_request['subgraph_name'])
        deploy_res = self.__subgraphs_operator_repo.deploy_subgraph(
            uc_request['subgraph_name'],
            uc_request['ipfs_hash'])
        if 'error' in deploy_res:
            if 'code' in deploy_res['error']:
                if deploy_res['error']['code'] == 0:
                    new_ipfs_hash = deploy_res['error']['message'].replace(
                        'subgraph validation error: [the graft base is invalid: deployment not found: ', '').replace(']', '')
                    deploy_res = self.__subgraphs_operator_repo.deploy_subgraph(
                        uc_request['subgraph_name'], new_ipfs_hash)
