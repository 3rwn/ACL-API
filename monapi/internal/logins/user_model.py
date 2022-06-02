from pydantic import BaseModel

users = {
    "admin": {
        "username": "admin",
        "password": "admin",
        "disabled": False,
    }
}


class User(BaseModel):
    username: str
    password: str
    disabled: bool | None = None
