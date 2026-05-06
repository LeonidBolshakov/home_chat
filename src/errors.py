class UserAlreadyExistsError(Exception):
    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(f"Пользователь с именем {name} уже существует")


class RoomUserAlreadyExistsError(Exception):
    def __init__(self, room: int, user: int) -> None:
        self.room = room
        self.user = user
        super().__init__(
            f"В таблице room_user уже есть запись с комнатой ID {room} и пользователем с ID {user}"
        )


class UserNotFoundError(Exception):
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        super().__init__(f"Пользователь с ID {self.user_id} не существует")


class RoomNotFoundError(Exception):
    def __init__(self, room_id: int) -> None:
        self.room_id = room_id
        super().__init__(f"Комната с ID {room_id} не существует")


class RoomUserNotFoundError(Exception):
    def __init__(self, room_id: int, user_id: int) -> None:
        self.room_id = room_id
        self.user_id = user_id
        super().__init__(
            f"Пользователь с ID {self.user_id} не находится в комнате с ID {self.room_id}"
        )


class InvalidCredentialsError(Exception):
    pass


class AccessDeniedError(Exception):
    pass
