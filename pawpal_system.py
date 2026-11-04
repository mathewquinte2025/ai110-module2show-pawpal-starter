from dataclasses import dataclass, field, replace
from datetime import date, timedelta
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
    due_date: date = field(default_factory=date.today)  # defaults to today

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def next_occurrence(self) -> Optional["Task"]:
        """Return a fresh copy of this task for its next date, or None if it does not repeat."""
        if self.frequency == "daily":
            days = 1
        elif self.frequency == "weekly":
            days = 7
        else:
            return None
        return replace(self, due_date=self.due_date + timedelta(days=days), completed=False)

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
        """Return all tasks sorted by date, then by their "HH:MM" time, earliest first."""
        return sorted(self.get_all_tasks(), key=lambda task: (task.due_date, task.time))

    def filter_tasks(self, pet_name: Optional[str] = None, completed: Optional[bool] = None) -> List[Task]:
        """Return time-sorted tasks, optionally only for one pet and/or one completion status."""
        tasks = self.sort_by_time()
        if pet_name is not None:
            tasks = [task for task in tasks if task.pet_name == pet_name]
        if completed is not None:
            tasks = [task for task in tasks if task.completed == completed]
        return tasks

    def mark_task_complete(self, task: Task) -> Optional[Task]:
        """Complete a task and, if it repeats, add its next occurrence to the same pet."""
        if task.completed:
            return None  # already done, so do not create another recurring copy
        task.mark_complete()
        next_task = task.next_occurrence()
        if next_task is None:
            return None
        for pet in self.owner.pets:
            if pet.name == task.pet_name:
                pet.add_task(next_task)
                return next_task
        return None

    def find_conflicts(self) -> List[str]:
        """Return a warning message for each date and time that has 2+ unfinished tasks."""
        slots = {}  # (due_date, time) -> tasks scheduled then
        for task in self.get_all_tasks():
            if not task.completed:
                slots.setdefault((task.due_date, task.time), []).append(task)

        warnings = []
        for (due_date, time), tasks in sorted(slots.items()):
            if len(tasks) > 1:
                names = " and ".join(f"{t.description} ({t.pet_name})" for t in tasks)
                warnings.append(f"Warning: {names} are scheduled at the same time ({time} on {due_date}).")
        return warnings