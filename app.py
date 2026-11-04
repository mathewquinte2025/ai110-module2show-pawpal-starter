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
            )
            # Find the chosen pet, then let Pet.add_task() attach the task to it.
            chosen_pet = next(pet for pet in owner.pets if pet.name == selected_pet_name)
            chosen_pet.add_task(task)
            st.success(f"Added '{task.description}' at {task.time} for {chosen_pet.name}.")

# --- Pets and their tasks ---------------------------------------------------
st.header("Your Pets")
if not owner.pets:
    st.write("No pets yet.")
for pet in owner.pets:
    st.subheader(f"{pet.name} ({pet.species}, age {pet.age})")
    pet_tasks = pet.get_tasks()
    if not pet_tasks:
        st.caption("No tasks yet.")
    else:
        st.table(
            [
                {
                    "Time": task.time,
                    "Task": task.description,
                    "Duration (min)": task.duration,
                    "Priority": task.priority,
                    "Frequency": task.frequency,
                }
                for task in pet_tasks
            ]
        )

# --- Daily plan -------------------------------------------------------------
st.header("Today's Schedule")
scheduler = Scheduler(owner)
sorted_tasks = scheduler.sort_by_time()
if not sorted_tasks:
    st.info("No tasks scheduled yet.")
else:
    st.table(
        [
            {
                "Time": task.time,
                "Task": task.description,
                "Pet": task.pet_name,
                "Duration (min)": task.duration,
                "Priority": task.priority,
            }
            for task in sorted_tasks
        ]
    )