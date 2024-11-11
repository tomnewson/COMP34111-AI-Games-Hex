from dataclasses import dataclass
from unittest.mock import Mock

from src.AgentBase import AgentBase as Agent


@dataclass
class Player:
    name: str
    agent: Agent
    move_time: int = 0
    turn: int = 0

    def __eq__(self, value: object) -> bool:
        if isinstance(self.agent, Mock) and isinstance(value.agent, Mock):
            return (
                self.name == value.name
                and self.move_time == value.move_time
            )
        return (
            hash(self.agent) == hash(value.agent)
            and self.name == value.name
            and self.move_time == value.move_time
        )
