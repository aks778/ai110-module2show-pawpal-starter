from pawpal_system import Task, Pet


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
