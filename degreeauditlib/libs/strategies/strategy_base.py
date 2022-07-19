from typing import Protocol


class Strategy(Protocol):
    name: str

    def merge_program_requirements(self):
        ...

    def sql(self) -> str:
        ...
