from pawpal_system import Owner, Pet, Task, Scheduler


def print_tasks(tasks):
    """Print one line per task: time, description, pet name, and done status."""
    if not tasks:
        print("  (none)")
    for task in tasks:
        status = "done" if task.completed else "to do"
        print(f"  {task.due_date} {task.time} - {task.description} ({task.pet_name}) [{status}]")


def main():
    # Create the owner and two pets
    owner = Owner(name="Mathew", available_time=120)
    buddy = Pet(name="Buddy", species="Dog", age=4)
    max_the_cat = Pet(name="Max", species="Cat", age=2)
    owner.add_pet(buddy)
    owner.add_pet(max_the_cat)

    # Add tasks (not in time order on purpose, so sorting is visible)
    buddy.add_task(Task(description="Grooming", time="11:00", duration=30))
    max_the_cat.add_task(Task(description="Breakfast", time="09:30", duration=10))
    buddy.add_task(Task(description="Morning Walk", time="08:00", duration=30,
                        priority="high", frequency="daily"))
    max_the_cat.add_task(Task(description="Evening Playtime", time="18:00", duration=20))
    max_the_cat.add_task(Task(description="Litter Cleaning", time="07:30", duration=10,
                              frequency="weekly"))

    scheduler = Scheduler(owner)

    print("Today's Schedule")
    for task in scheduler.sort_by_time():
        print(f"{task.time} - {task.description} ({task.pet_name})")

    print("\nTasks in the order they were added (unsorted):")
    print_tasks(scheduler.get_all_tasks())

    print("\nSorted by time:")
    print_tasks(scheduler.sort_by_time())

    print("\nFiltered: Buddy's tasks only")
    print_tasks(scheduler.filter_tasks(pet_name="Buddy"))

    # Recurring tasks: completing a daily/weekly task creates the next one
    print("\nRecurring tasks:")
    walk = buddy.get_tasks()[1]  # Morning Walk (daily)
    litter = max_the_cat.get_tasks()[2]  # Litter Cleaning (weekly)
    grooming = buddy.get_tasks()[0]  # Grooming (does not repeat)
    for task in (walk, litter, grooming):
        new_task = scheduler.mark_task_complete(task)
        if new_task:
            print(f"  Completed '{task.description}' -> next one on {new_task.due_date}")
        else:
            print(f"  Completed '{task.description}' -> no repeat")
    again = scheduler.mark_task_complete(walk)
    print(f"  Completing 'Morning Walk' a second time -> new task created? {again is not None}")

    print("\nFiltered: completed tasks")
    print_tasks(scheduler.filter_tasks(completed=True))

    print("\nFiltered: Buddy's unfinished tasks")
    print_tasks(scheduler.filter_tasks(pet_name="Buddy", completed=False))

    # Conflict detection: two tasks at the same time
    buddy.add_task(Task(description="Vet Visit", time="09:30", duration=45))

    print("\nConflict check:")
    conflicts = scheduler.find_conflicts()
    if conflicts:
        for warning in conflicts:
            print(f"  {warning}")
    else:
        print("  No conflicts found.")


if __name__ == "__main__":
    main()