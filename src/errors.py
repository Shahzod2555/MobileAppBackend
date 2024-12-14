from fastapi import HTTPException

class UserAlreadyExistsError(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Пользователь с таким email или номером телефона уже существует.")

class InvalidCredentialsError(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Неверный номер телефона, email или пароль.")
