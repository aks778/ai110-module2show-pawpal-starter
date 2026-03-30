import streamlit as st
from pawpal_system import Owner, Pet, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")

# Initialize Owner in session state if it doesn't exist
if 'owner' not in st.session_state:
    st.session_state.owner = Owner(
        name=owner_name, time_available=120)  # Default 2 hours available
    st.info("New Owner created and stored in session state!")
else:
    # Update existing owner name if changed
    if st.session_state.owner.name != owner_name:
        st.session_state.owner.name = owner_name
        st.info("Owner name updated!")

# Display current owner info
st.write(
    f"Current Owner: {st.session_state.owner.name} (Available time: {st.session_state.owner.time_available} min)")

st.markdown("### Add a Pet")
st.caption("Add pets to your owner profile.")

# Pet addition form
col1, col2, col3, col4 = st.columns(4)
with col1:
    new_pet_name = st.text_input("Pet name", key="new_pet_name")
with col2:
    new_species = st.selectbox(
        "Species", ["dog", "cat", "other"], key="new_species")
with col3:
    new_breed = st.text_input("Breed", value="Mixed", key="new_breed")
with col4:
    new_age = st.number_input(
        "Age", min_value=0, max_value=30, value=1, key="new_age")

if st.button("Add Pet"):
    # Create new Pet instance using the Pet constructor
    new_pet = Pet(
        name=new_pet_name,
        species=new_species,
        breed=new_breed,
        age=new_age
    )
    # Use Owner.add_pet() method to add the pet to the owner
    st.session_state.owner.add_pet(new_pet)
    st.success(f"Pet '{new_pet_name}' added to {st.session_state.owner.name}!")
    # Clear the form by rerunning (Streamlit will reset the inputs)
    st.rerun()

# Display all pets for the owner
if st.session_state.owner.get_pets():
    st.write("**Your Pets:**")
    for pet in st.session_state.owner.get_pets():
        st.write(f"- {pet.get_info()}")
else:
    st.info("No pets added yet.")

st.markdown("### Tasks")
st.caption(
    "Add tasks for your pets. Select which pet the task is for.")

# Only show task form if there are pets
if st.session_state.owner.get_pets():
    # Pet selector for tasks
    pet_names = [pet.name for pet in st.session_state.owner.get_pets()]
    selected_pet_name = st.selectbox("Select pet for this task", pet_names)
    selected_pet = next(pet for pet in st.session_state.owner.get_pets(
    ) if pet.name == selected_pet_name)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    if st.button("Add task"):
        # Convert priority string to number (1=low, 3=medium, 5=high)
        priority_map = {"low": 1, "medium": 3, "high": 5}
        new_task = Task(
            title=task_title,
            duration=duration,
            priority=priority_map[priority]
        )
        # Use Pet.add_task() method to add task to the selected pet
        selected_pet.add_task(new_task)
        st.success(f"Task '{task_title}' added to {selected_pet.name}!")

    # Display tasks for all pets
    st.write("**All Tasks:**")
    all_tasks = st.session_state.owner.get_all_tasks()
    if all_tasks:
        task_data = []
        for task in all_tasks:
            task_data.append({
                "pet": task.pet.name if task.pet else "unassigned",
                "title": task.title,
                "duration_minutes": task.duration,
                "priority": task.priority,
                "status": "done" if task.is_complete else "pending"
            })
        st.table(task_data)
    else:
        st.info("No tasks yet. Add one above.")
else:
    st.warning("Add a pet first before creating tasks.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    from pawpal_system import Schedule
    from datetime import date

    # Create a schedule for today
    today = date.today().strftime("%Y-%m-%d")
    schedule = Schedule(date=today, owner=st.session_state.owner)

    # Generate the plan
    schedule.generate_plan()

    st.success("Schedule generated!")
    st.write("**Reasoning:**")
    st.code(schedule.explain_reasoning(), language="text")

    st.write("**Scheduled Tasks:**")
    if schedule.tasks:
        schedule.display()
    else:
        st.info("No tasks were scheduled (possibly all complete or time constraints).")
