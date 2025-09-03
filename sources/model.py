from pydantic import BaseModel
from google.genai import types
from typing import List, Callable, Any

class Game(BaseModel):
    appid: int
    name: str


class Function(BaseModel):
    gemini: types.FunctionDeclaration
    recognized_names: List[str]
    to_execute: Callable[..., Any]
