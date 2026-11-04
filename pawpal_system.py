from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Task:
    description: str
    time: str  # "HH:MM" format, e.g. "08:30"
    duration: int  # minutes
    priority: str = "medium"
    frequency: str = "once"
    completed: bool = False
    pet_name: str = ""  # filled in automatically by Pet.add_task()

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def reschedule(self, new_time: str) -> None:
        """Change this task's scheduled time to new_time ("HH:MM")."""
        self.time = new_time


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet and record this pet's name on the task."""
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet if it is in the list."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> List[Task]:
        """Return this pet's list of tasks."""
        return self.tasks


class Owner:
    def __init__(
        self,
        name: str,
        available_time: int,
        preferences: Optional[dict] = None
    ):
        self.name = name
        self.available_time = available_time  # minutes per day
        self.preferences = preferences or {}
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return every task from every pet this owner has."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks by asking the owner (which asks each pet)."""
        return self.owner.get_all_tasks()

    def sort_by_time(self) -> List[Task]:
        """Return all tasks sorted by their "HH:MM" time, earliest first."""
        return sorted(self.get_all_tasks(), key=lambda task: task.time)