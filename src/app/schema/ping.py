from typing import Literal

from src.common.schema import SchemaBase


class GetPing(SchemaBase):
    ping: Literal['pong'] = 'pong'
