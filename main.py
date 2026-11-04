from pawpal_system import Owner, Pet, Task, Scheduler


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
    buddy.add_task(Task(description="Morning Walk", time="08:00", duration=30, priority="high"))
    max_the_cat.add_task(Task(description="Evening Playtime", time="18:00", duration=20))

    # The Scheduler retrieves and sorts the tasks
    scheduler = Scheduler(owner)

    print("Today's Schedule")
    for task in scheduler.sort_by_time():
        print(f"{task.time} - {task.description} ({task.pet_name})")


if __name__ == "__main__":
    main()