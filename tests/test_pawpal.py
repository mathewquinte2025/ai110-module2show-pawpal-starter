from datetime import date

from pawpal_system import Owner, Pet, Task, Scheduler

TODAY = date(2026, 11, 4)


def make_scheduler():
    """Build an owner with Buddy and Max (no tasks yet) and return their pieces."""
    owner = Owner(name="Mathew", available_time=120)
    buddy = Pet(name="Buddy", species="Dog", age=4)
    max_the_cat = Pet(name="Max", species="Cat", age=2)
    owner.add_pet(buddy)
    owner.add_pet(max_the_cat)
    return Scheduler(owner), buddy, max_the_cat


# --- Phase 2 tests -----------------------------------------------------------

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


# --- Phase 4 tests -----------------------------------------------------------

def test_sort_by_time_returns_chronological_order():
    scheduler, buddy, max_the_cat = make_scheduler()
    buddy.add_task(Task("Grooming", "11:00", 30, due_date=TODAY))
    max_the_cat.add_task(Task("Breakfast", "09:30", 10, due_date=TODAY))
    buddy.add_task(Task("Morning Walk", "08:00", 30, due_date=TODAY))

    times = [task.time for task in scheduler.sort_by_time()]

    assert times == ["08:00", "09:30", "11:00"]


def test_filter_by_pet_and_by_completion_status():
    scheduler, buddy, max_the_cat = make_scheduler()
    walk = Task("Morning Walk", "08:00", 30, due_date=TODAY)
    buddy.add_task(walk)
    buddy.add_task(Task("Grooming", "11:00", 30, due_date=TODAY))
    max_the_cat.add_task(Task("Breakfast", "09:30", 10, due_date=TODAY))
    walk.mark_complete()

    assert [t.description for t in scheduler.filter_tasks(pet_name="Max")] == ["Breakfast"]
    assert [t.description for t in scheduler.filter_tasks(completed=True)] == ["Morning Walk"]
    assert [t.description for t in scheduler.filter_tasks(pet_name="Buddy", completed=False)] == ["Grooming"]


def test_daily_task_recurs_one_day_later():
    scheduler, buddy, _ = make_scheduler()
    walk = Task("Morning Walk", "08:00", 30, frequency="daily", due_date=TODAY)
    buddy.add_task(walk)

    new_task = scheduler.mark_task_complete(walk)

    assert walk.completed is True
    assert new_task.due_date == date(2026, 11, 5)
    assert new_task.completed is False
    assert new_task.pet_name == "Buddy"
    assert new_task in buddy.get_tasks()


def test_weekly_task_recurs_seven_days_later():
    scheduler, _, max_the_cat = make_scheduler()
    litter = Task("Litter Cleaning", "07:30", 10, frequency="weekly", due_date=TODAY)
    max_the_cat.add_task(litter)

    new_task = scheduler.mark_task_complete(litter)

    assert new_task.due_date == date(2026, 11, 11)


def test_one_time_task_does_not_recur():
    scheduler, buddy, _ = make_scheduler()
    grooming = Task("Grooming", "11:00", 30, due_date=TODAY)
    buddy.add_task(grooming)

    assert scheduler.mark_task_complete(grooming) is None
    assert len(buddy.get_tasks()) == 1


def test_completing_same_task_twice_does_not_duplicate():
    scheduler, buddy, _ = make_scheduler()
    walk = Task("Morning Walk", "08:00", 30, frequency="daily", due_date=TODAY)
    buddy.add_task(walk)

    scheduler.mark_task_complete(walk)
    second = scheduler.mark_task_complete(walk)

    assert second is None
    assert len(buddy.get_tasks()) == 2  # the original plus exactly one new task


def test_conflict_detection_flags_same_time_with_names():
    scheduler, buddy, max_the_cat = make_scheduler()
    buddy.add_task(Task("Vet Visit", "09:30", 45, due_date=TODAY))
    max_the_cat.add_task(Task("Breakfast", "09:30", 10, due_date=TODAY))
    max_the_cat.add_task(Task("Playtime", "18:00", 20, due_date=TODAY))

    warnings = scheduler.find_conflicts()

    assert len(warnings) == 1
    assert "Vet Visit (Buddy)" in warnings[0]
    assert "Breakfast (Max)" in warnings[0]
    assert "09:30" in warnings[0]


def test_no_conflicts_and_empty_pets_do_not_crash():
    scheduler, buddy, _ = make_scheduler()  # both pets have no tasks
    assert scheduler.find_conflicts() == []
    assert scheduler.sort_by_time() == []

    buddy.add_task(Task("Walk", "08:00", 30, due_date=TODAY))
    buddy.add_task(Task("Grooming", "11:00", 30, due_date=TODAY))
    assert scheduler.find_conflicts() == []