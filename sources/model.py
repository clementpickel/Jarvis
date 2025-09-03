from pydantic import BaseModel

class Game(BaseModel):
    appid: int
    name: str
