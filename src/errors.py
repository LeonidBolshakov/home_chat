class UserAlreadyExistsError(Exception):
    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(f"Пользователь {name} уже существует")


class UserNotFoundError(Exception):
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        super().__init__(f"Пользователь с Id {self.user_id} не существует")


class RoomNotFoundError(Exception):
    def __init__(self, room_id: int) -> None:
        self.room_id = room_id
        super().__init__(f"Комната {room_id} не существует")
