from dataclasses import dataclass, field
from typing import List


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int

    def get_info(self) -> str:
        pass

    def update_info(self, field: str, value) -> None:
        pass


@dataclass
class Task:
    title: str
    duration: int        # in minutes
    priority: int        # 1 (low) to 5 (high)
    pet: Pet = None
    description: str = ""
    is_complete: bool = False

    def mark_complete(self) -> None:
        pass

    def edit(self, field: str, value) -> None:
        pass

    def __str__(self) -> str:
        pass


class Owner:
    def __init__(self, name: str, time_available: int, preferences: dict = None):
        self.name = name
        self.time_available = time_available   # daily minutes available
        self.preferences = preferences or {}
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet: Pet) -> None:
        pass

    def get_pets(self) -> List[Pet]:
        pass


class Schedule:
    def __init__(self, date: str, owner: Owner):
        self.date = date
        self.owner = owner
        self.tasks: List[Task] = []
        self.reasoning: str = ""

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def generate_plan(self) -> None:
        pass

    def explain_reasoning(self) -> str:
        pass

    def display(self) -> None:
        pass
