import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾")

st.title("🐾 PawPal+")
st.caption("A simple pet care planner.")

# --- Application memory -----------------------------------------------------
# Streamlit re-runs this whole file after every click. We only create the Owner
# if one is not already stored in st.session_state, so data survives reruns.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_time=120)

owner = st.session_state.owner

# --- Owner info -------------------------------------------------------------
st.header("Owner")
owner.name = st.text_input("Owner name", value=owner.name)
owner.available_time = st.number_input(
    "Time available today (minutes)",
    min_value=0,
    max_value=1440,
    value=owner.available_time,
    step=15,
)

# --- Add a pet --------------------------------------------------------------
st.header("Add a Pet")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["Dog", "Cat", "Other"])
    age = st.number_input("Age (years)", min_value=0, max_value=40, value=1)
    add_pet_clicked = st.form_submit_button("Add pet")

if add_pet_clicked:
    pet_name = pet_name.strip()
    if not pet_name:
        st.error("Please enter a pet name.")
    elif pet_name in [pet.name for pet in owner.pets]:
        st.error(f"You already have a pet named {pet_name}.")
    else:
        owner.add_pet(Pet(name=pet_name, species=species, age=age))
        st.success(f"Added {pet_name} the {species.lower()}!")

# --- Add a task -------------------------------------------------------------
st.header("Add a Care Task")
if not owner.pets:
    st.info("Add a pet first, then you can schedule tasks for it.")
else:
    with st.form("add_task_form", clear_on_submit=True):
        selected_pet_name = st.selectbox("Pet", [pet.name for pet in owner.pets])
        description = st.text_input("Task description", placeholder="Morning walk")
        task_date = st.date_input("Date")
        task_time = st.time_input("Time")
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=480, value=20)
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        add_task_clicked = st.form_submit_button("Add task")

    if add_task_clicked:
        if not description.strip():
            st.error("Please enter a task description.")
        else:
            task = Task(
                description=description.strip(),
                time=task_time.strftime("%H:%M"),
                duration=duration,
                priority=priority,
                frequency=frequency,
                due_date=task_date,
            )
            # Find the chosen pet, then let Pet.add_task() attach the task to it.
            chosen_pet = next(pet for pet in owner.pets if pet.name == selected_pet_name)
            chosen_pet.add_task(task)
            st.success(
                f"Added '{task.description}' on {task.due_date} at {task.time} for {chosen_pet.name}."
            )

# --- Mark a task complete --------------------------------------------------
scheduler = Scheduler(owner)

st.header("Mark a Task Complete")
pending_tasks = scheduler.filter_tasks(completed=False)
if not pending_tasks:
    st.info("There are no unfinished tasks to complete.")
else:
    with st.form("complete_task_form"):
        task_index = st.selectbox(
            "Unfinished task",
            range(len(pending_tasks)),
            format_func=lambda i: (
                f"{pending_tasks[i].due_date} {pending_tasks[i].time} - "
                f"{pending_tasks[i].description} ({pending_tasks[i].pet_name})"
            ),
        )
        complete_clicked = st.form_submit_button("Mark complete")

    if complete_clicked:
        done_task = pending_tasks[task_index]
        # The Scheduler marks the task done and, for daily/weekly tasks,
        # adds the next occurrence to the same pet.
        next_task = scheduler.mark_task_complete(done_task)
        if next_task:
            st.success(
                f"Completed '{done_task.description}'. The next one is scheduled "
                f"for {next_task.due_date} at {next_task.time}."
            )
        else:
            st.success(f"Completed '{done_task.description}'.")


def task_rows(tasks):
    """Turn a list of tasks into table rows for st.table()."""
    return [
        {
            "Date": str(task.due_date),
            "Time": task.time,
            "Task": task.description,
            "Pet": task.pet_name,
            "Duration (min)": task.duration,
            "Priority": task.priority,
            "Frequency": task.frequency,
            "Status": "Done" if task.completed else "To do",
        }
        for task in tasks
    ]


# --- Pets and their tasks ---------------------------------------------------
st.header("Your Pets")
if not owner.pets:
    st.write("No pets yet.")
for pet in owner.pets:
    st.subheader(f"{pet.name} ({pet.species}, age {pet.age})")
    # filter_tasks() returns this pet's tasks already sorted by date and time.
    pet_tasks = scheduler.filter_tasks(pet_name=pet.name)
    if not pet_tasks:
        st.caption("No tasks yet.")
    else:
        st.table(task_rows(pet_tasks))

# --- Schedule ---------------------------------------------------------------
st.header("Schedule")

# Conflict warnings: two or more unfinished tasks at the exact same date and time.
conflicts = scheduler.find_conflicts()
if conflicts:
    for warning in conflicts:
        st.warning(warning)
elif scheduler.get_all_tasks():
    st.success("No scheduling conflicts. No two unfinished tasks share the same date and time.")

# Filters use Scheduler.filter_tasks(), which also sorts by date and time.
col1, col2 = st.columns(2)
with col1:
    pet_choice = st.selectbox("Show pet", ["All pets"] + [pet.name for pet in owner.pets])
with col2:
    status_choice = st.selectbox("Show status", ["All", "To do", "Done"])

pet_filter = None if pet_choice == "All pets" else pet_choice
status_filter = {"All": None, "To do": False, "Done": True}[status_choice]
shown_tasks = scheduler.filter_tasks(pet_name=pet_filter, completed=status_filter)

if not scheduler.get_all_tasks():
    st.info("No tasks scheduled yet.")
elif not shown_tasks:
    st.info("No tasks match these filters.")
else:
    st.caption(f"Showing {len(shown_tasks)} task(s), earliest first.")
    st.table(task_rows(shown_tasks))
