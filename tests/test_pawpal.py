from pawpal_system import Pet, Task


def test_mark_complete_changes_status():
    task = Task(description="Morning Walk", time="08:00", duration=30)
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    pet = Pet(name="Buddy", species="Dog", age=4)
    task = Task(description="Grooming", time="11:00", duration=30)
    assert len(pet.get_tasks()) == 0

    pet.add_task(task)

    assert len(pet.get_tasks()) == 1