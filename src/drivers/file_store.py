from os.path import exists


class FileStore:

    def __init__(self, file_dst: str) -> None:
        self.file_dst = file_dst
        self.__init_store()

    def __init_store(self) -> None:
        if exists(self.file_dst):
            return
        fp = open(self.file_dst, 'x')
        fp.close()

    def get(self) -> str:
        with open(self.file_dst, 'r') as f:
            return f.read()

    def save(self, data: str) -> None:
        with open(self.file_dst, 'w') as f:
            f.write(data)
