from __future__ import annotations
from dataclasses import dataclass, field, replace
from datetime import date, timedelta
from typing import List, Tuple


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

    def next_occurrence(self) -> Task:
        """Return a new pending copy of this task for its next occurrence."""
        return replace(self, is_complete=False, pet=self.pet)

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

    def complete_task(self, task: Task) -> Task | None:
        """Mark a task complete and auto-schedule the next occurrence for recurring tasks.

        For 'daily' tasks, creates a copy due 1 day after this schedule's date.
        For 'weekly' tasks, creates a copy due 7 days after this schedule's date.
        'as-needed' tasks are marked complete with no follow-up scheduled.
        The new task is added directly to the same pet's task list.

        Args:
            task: A Task already present in this schedule.

        Returns:
            The newly created Task for the next occurrence, or None if the task
            is not recurring (frequency == 'as-needed').
        """
        task.mark_complete()

        if task.frequency not in ("daily", "weekly"):
            return None

        days = 1 if task.frequency == "daily" else 7
        next_date = date.fromisoformat(self.date) + timedelta(days=days)

        next_task = task.next_occurrence()
        if task.pet:
            task.pet.add_task(next_task)
            print(
                f"  -> '{next_task.title}' rescheduled for {next_date} ({task.frequency})"
            )
        return next_task

    def generate_plan(self) -> None:
        """Generate a daily task plan using a greedy priority-first algorithm.

        Collects all incomplete tasks from every pet owned by this schedule's
        owner, sorts them by priority (highest first), then adds them one by one
        until the owner's available time is exhausted.  Tasks that don't fit are
        skipped and noted in the reasoning log.

        Algorithm: greedy — O(n log n) sort + O(n) pass.
        Side effects: replaces self.tasks and self.reasoning in place.
        """
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

    def find_conflicts(self) -> List[Tuple[Task, Task]]:
        """Return pairs of tasks whose time windows overlap.

        Two tasks conflict when one starts before the other finishes:
            start_a < end_b  AND  start_b < end_a
        Uses an O(n²) pairwise scan over all scheduled tasks; works across
        pets and within the same pet.

        Returns:
            A list of (Task, Task) tuples where each pair overlaps in time.
            Returns an empty list when the schedule has no conflicts.
        """
        def to_minutes(t: str) -> int:
            h, m = t.split(":")
            return int(h) * 60 + int(m)

        conflicts = []
        for i, a in enumerate(self.tasks):
            for b in self.tasks[i + 1:]:
                start_a, end_a = to_minutes(
                    a.time), to_minutes(a.time) + a.duration
                start_b, end_b = to_minutes(
                    b.time), to_minutes(b.time) + b.duration
                if start_a < end_b and start_b < end_a:
                    conflicts.append((a, b))
        return conflicts

    def warn_conflicts(self) -> str | None:
        """Return a warning string listing any overlapping tasks, or None if clear."""
        conflicts = self.find_conflicts()
        if not conflicts:
            return None
        lines = [
            f"WARNING: {len(conflicts)} scheduling conflict(s) on {self.date}:"]
        for a, b in conflicts:
            pet_a = a.pet.name if a.pet else "unassigned"
            pet_b = b.pet.name if b.pet else "unassigned"
            lines.append(
                f"  - [{pet_a}] {a.title} ({a.time}, {a.duration}min)"
                f"  overlaps  [{pet_b}] {b.title} ({b.time}, {b.duration}min)"
            )
        return "\n".join(lines)

    def filter_by_status(self, is_complete: bool) -> List[Task]:
        """Return tasks matching the given completion status."""
        return [t for t in self.tasks if t.is_complete == is_complete]

    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """Return tasks belonging to the pet with the given name."""
        return [t for t in self.tasks if t.pet and t.pet.name == pet_name]

    def sort_by_time(self) -> None:
        """Sort the scheduled tasks in-place by their start time (HH:MM)."""
        self.tasks.sort(key=lambda t: t.time)

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
