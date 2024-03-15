class BasicInfo:
    def __init__(self, name: str, id: str):
        self.__name = name
        self.__id = id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def id(self) -> str:
        return self.__id

    @name.setter
    def name(self, name: str) -> None:
        self.__name = name

    @id.setter
    def id(self, id: str) -> None:
        self.__id = id
