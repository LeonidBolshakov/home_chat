class UserAlreadyExistsError(Exception):
    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(f"Пользователь {name} уже существует")
