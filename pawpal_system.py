
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Task:
    description: str
    time: str
    duration: int
    priority: str = "medium"
    frequency: str = "once"
    completed: bool = False

    def mark_complete(self) -> None:
        pass

    def reschedule(self, new_time: str) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def get_tasks(self) -> List[Task]:
        pass


class Owner:
    def __init__(
        self,
        name: str,
        available_time: int,
        preferences: Optional[dict] = None
    ):
        self.name = name
        self.available_time = available_time
        self.preferences = preferences or {}
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_all_tasks(self) -> List[Task]:
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def get_all_tasks(self) -> List[Task]:
        pass

    def sort_by_time(self) -> List[Task]:
        pass
