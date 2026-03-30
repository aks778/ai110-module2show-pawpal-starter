from pawpal_system import Owner, Pet, Task, Schedule

# --- Create Owner ---
owner = Owner(name="Alex", time_available=90)

# --- Create Pets ---
buddy = Pet(name="Buddy", species="Dog", breed="Labrador", age=3)
luna = Pet(name="Luna",  species="Cat", breed="Siamese",  age=5)

# --- Add Pets to Owner ---
owner.add_pet(buddy)
owner.add_pet(luna)

# --- Create Tasks (intentionally out of time order) ---
playtime = Task(title="Playtime",        duration=15, priority=2,
                time="15:00", description="Interactive toy session")
vet_meds = Task(title="Give Medication", duration=5,  priority=5,
                time="08:00", description="Daily prescribed tablet")  # conflicts with Feeding
grooming = Task(title="Grooming",        duration=20, priority=3,
                time="10:00", description="Brush coat and check ears")
feeding = Task(title="Feeding",         duration=10, priority=4,
               time="08:00", description="Breakfast and fresh water")
morning_walk = Task(title="Morning Walk",  duration=30, priority=5,
                    time="07:00", description="30 min walk around the block")

# --- Assign Tasks to Pets ---
buddy.add_task(playtime)
buddy.add_task(grooming)
buddy.add_task(morning_walk)
luna.add_task(vet_meds)
luna.add_task(feeding)

# --- Build Schedule ---
schedule = Schedule(date="2026-03-29", owner=owner)
schedule.generate_plan()

# --- Test sort_by_time() ---
print("=== Tasks sorted by time (before sort) ===")
for task in schedule.tasks:
    print(f"  {task.time} | {task.title}")

schedule.sort_by_time()

print("\n=== Tasks sorted by time (after sort_by_time) ===")
for task in schedule.tasks:
    print(f"  {task.time} | {task.title}")

# --- Test filter_by_status() ---
print("\n=== filter_by_status(is_complete=False) — pending tasks ===")
pending = schedule.filter_by_status(is_complete=False)
for task in pending:
    print(f"  {task.title} | complete={task.is_complete}")

print("\n=== filter_by_status(is_complete=True) — completed tasks ===")
done = schedule.filter_by_status(is_complete=True)
print(f"  {len(done)} completed task(s)" if done else "  None completed yet.")

# --- Test filter_by_pet() ---
print("\n=== filter_by_pet('Buddy') ===")
buddy_tasks = schedule.filter_by_pet("Buddy")
for task in buddy_tasks:
    print(f"  {task.title} ({task.pet.name})")

print("\n=== filter_by_pet('Luna') ===")
luna_tasks = schedule.filter_by_pet("Luna")
for task in luna_tasks:
    print(f"  {task.title} ({task.pet.name})")

# --- Conflict detection ---
print("\n=== warn_conflicts() ===")
warning = schedule.warn_conflicts()
if warning:
    print(warning)
else:
    print("  Schedule is clear.")

# --- Full schedule display and reasoning ---
print()
schedule.display()
print()
print(schedule.explain_reasoning())
