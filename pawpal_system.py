from __future__ import annotations
from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    title: str
    duration: int            # in minutes
    priority: int            # 1 (low) to 5 (high)
    time: str = "08:00"      # scheduled start time (HH:MM)
    pet: Pet = None
    description: str = ""
    frequency: str = "daily"  # daily, weekly, as-needed
    is_complete: bool = False

    def mark_complete(self) -> None:
        """Mark the task as complete."""
        self.is_complete = True

    def edit(self, field: str, value) -> None:
        """Edit a field on the task if it exists."""
        if hasattr(self, field):
            setattr(self, field, value)

    def __str__(self) -> str:
        """Return a user-friendly string representation of the task."""
        status = "done" if self.is_complete else "pending"
        pet_name = self.pet.name if self.pet else "unassigned"
        return (
            f"[{status}] {self.time} | {self.title} ({pet_name}) "
            f"| {self.duration} min | Priority: {self.priority} | {self.frequency}"
        )


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def get_info(self) -> str:
        """Get a summary string for the pet."""
        return f"{self.name} | {self.species} ({self.breed}) | Age: {self.age}"

    def update_info(self, field: str, value) -> None:
        """Update a field on the pet if it exists."""
        if hasattr(self, field):
            setattr(self, field, value)

    def add_task(self, task: Task) -> None:
        """Associate a task with this pet and add it to the task list."""
        task.pet = self
        self.tasks.append(task)


class Owner:
    def __init__(self, name: str, time_available: int, preferences: dict = None):
        """Initialize an owner with a name, available minutes, and optional preferences."""
        self.name = name
        self.time_available = time_available   # daily minutes available
        self.preferences = preferences or {}
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from the owner."""
        self.pets.remove(pet)

    def get_pets(self) -> List[Pet]:
        """Return all pets owned by the owner."""
        return self.pets

    def get_all_tasks(self) -> List[Task]:
        """Aggregate tasks from all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


class Schedule:
    def __init__(self, date: str, owner: Owner):
        """Initialize a schedule for a given date and owner."""
        self.date = date
        self.owner = owner
        self.tasks: List[Task] = []
        self.reasoning: str = ""

    def add_task(self, task: Task) -> None:
        """Add a task to the schedule."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from the schedule."""
        self.tasks.remove(task)

    def generate_plan(self) -> None:
        """Generate a daily task plan based on priority and owner availability."""
        # Pull all tasks from every pet the owner has
        all_tasks = self.owner.get_all_tasks()

        # Sort by priority descending so highest-priority tasks are scheduled first
        sorted_tasks = sorted(
            all_tasks, key=lambda t: t.priority, reverse=True)

        self.tasks = []
        self.reasoning = "Scheduled:\n"
        skipped = []
        time_used = 0

        for task in sorted_tasks:
            if task.is_complete:
                skipped.append(
                    f"  - '{task.title}' skipped (already complete)")
                continue
            if time_used + task.duration <= self.owner.time_available:
                self.tasks.append(task)
                time_used += task.duration
                self.reasoning += (
                    f"  - '{task.title}' added "
                    f"(priority {task.priority}, {task.duration} min)\n"
                )
            else:
                remaining = self.owner.time_available - time_used
                skipped.append(
                    f"  - '{task.title}' skipped "
                    f"(needs {task.duration} min, only {remaining} min left)"
                )

        if skipped:
            self.reasoning += "Skipped:\n" + "\n".join(skipped)

    def explain_reasoning(self) -> str:
        """Return human-readable reasoning for the generated schedule."""
        if not self.reasoning:
            return "No plan generated yet. Call generate_plan() first."
        return f"Plan reasoning for {self.date}:\n{self.reasoning}"

    def display(self) -> None:
        """Print out the schedule summary and total time used."""
        if not self.tasks:
            print("No tasks scheduled. Call generate_plan() first.")
            return
        print(
            f"\n--- Daily Schedule: {self.date} | Owner: {self.owner.name} ---")
        total_time = 0
        for i, task in enumerate(sorted(self.tasks, key=lambda t: t.time), 1):
            print(f"  {i}. {task}")
            total_time += task.duration
        print(
            f"\n  Total: {total_time} min / {self.owner.time_available} min available")
