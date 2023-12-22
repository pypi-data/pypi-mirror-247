from enum import Enum


class AutoCLIAction(Enum):
    Clean = "clean"

    def __str__(self) -> str:
        return self.value
