import typing as tp


class BaseUseCase:

    def execute(self, uc_request: tp.Optional[tp.Any]) -> tp.Any:
        ...
