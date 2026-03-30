from pawpal_system import Task, Pet, Owner, Schedule
from datetime import date


def test_mark_complete_changes_status():
    task = Task(title="Feed", duration=5, priority=3)
    assert task.is_complete == False
    task.mark_complete()
    assert task.is_complete == True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", species="Dog", breed="Labrador", age=3)
    task = Task(title="Walk", duration=30, priority=4)
    assert len(pet.tasks) == 0
    pet.add_task(task)
    assert len(pet.tasks) == 1


def test_sort_by_time_orders_tasks_chronologically():
    """Verify tasks are returned in chronological order."""
    owner = Owner(name="Test Owner", time_available=120)
    pet = Pet(name="Test Pet", species="Dog", breed="Mixed", age=2)
    owner.add_pet(pet)

    # Create tasks with different times
    task1 = Task(title="Morning Feed", duration=10, priority=3, time="08:00")
    task2 = Task(title="Afternoon Walk", duration=30, priority=4, time="14:00")
    task3 = Task(title="Evening Play", duration=20, priority=2, time="18:00")
    task4 = Task(title="Midday Snack", duration=15, priority=3, time="12:00")

    # Add tasks to pet
    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)
    pet.add_task(task4)

    # Create schedule and generate plan
    schedule = Schedule(date="2024-01-01", owner=owner)
    schedule.generate_plan()

    # Sort by time
    schedule.sort_by_time()

    # Verify chronological order
    assert len(schedule.tasks) == 4
    assert schedule.tasks[0].time == "08:00"
    assert schedule.tasks[1].time == "12:00"
    assert schedule.tasks[2].time == "14:00"
    assert schedule.tasks[3].time == "18:00"


def test_daily_task_completion_creates_next_day_task():
    """Confirm that marking a daily task complete creates a new task for the following day."""
    owner = Owner(name="Test Owner", time_available=120)
    pet = Pet(name="Test Pet", species="Dog", breed="Mixed", age=2)
    owner.add_pet(pet)

    # Create a daily task
    task = Task(title="Daily Walk", duration=30, priority=4, frequency="daily")
    pet.add_task(task)

    # Create schedule
    schedule = Schedule(date="2024-01-01", owner=owner)
    schedule.generate_plan()

    # Verify task is scheduled
    assert len(schedule.tasks) == 1
    assert schedule.tasks[0].title == "Daily Walk"

    # Mark task complete and check recurrence
    next_task = schedule.complete_task(task)

    # Verify original task is complete
    assert task.is_complete == True

    # Verify next occurrence was created
    assert next_task is not None
    assert next_task.title == "Daily Walk"
    assert next_task.is_complete == False
    assert next_task.frequency == "daily"

    # Verify next task was added to pet
    assert len(pet.tasks) == 2
    assert pet.tasks[1] == next_task


def test_scheduler_flags_duplicate_times():
    """Verify that the Scheduler flags duplicate times."""
    owner = Owner(name="Test Owner", time_available=120)
    pet = Pet(name="Test Pet", species="Dog", breed="Mixed", age=2)
    owner.add_pet(pet)

    # Create tasks with same time (duplicate)
    task1 = Task(title="Morning Feed", duration=10, priority=3, time="08:00")
    task2 = Task(title="Morning Walk", duration=30, priority=4, time="08:00")
    task3 = Task(title="Afternoon Play", duration=20, priority=2, time="14:00")

    # Add tasks to pet
    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)

    # Create schedule and generate plan
    schedule = Schedule(date="2024-01-01", owner=owner)
    schedule.generate_plan()

    # Check for conflicts
    conflicts = schedule.find_conflicts()

    # Should detect conflict between task1 and task2 (same time)
    assert len(conflicts) == 1
    assert (task1, task2) in conflicts or (task2, task1) in conflicts

    # Check warning message
    warning = schedule.warn_conflicts()
    assert warning is not None
    assert "scheduling conflict" in warning.lower()
    assert "08:00" in warning
