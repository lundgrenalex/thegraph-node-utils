from os.path import exists


class FileStore:

    def __init__(self, file_dst: str) -> None:
        self.file_dst = file_dst
        self.__check_store()

    def __check_store(self) -> None:
        file_exists = exists(self.file_dst)
        if not file_exists:
            self.save('[]')

    def get(self) -> str:
        with open(self.file_dst, 'r') as f:
            return f.read()

    def save(self, data: str) -> None:
        with open(self.file_dst, 'w') as f:
            f.write(data)
