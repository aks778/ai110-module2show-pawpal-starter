from pawpal_system import Owner, Pet, Task, Schedule

# --- Create Owner ---
owner = Owner(name="Alex", time_available=90)

# --- Create Pets ---
buddy = Pet(name="Buddy", species="Dog", breed="Labrador", age=3)
luna = Pet(name="Luna",  species="Cat", breed="Siamese",  age=5)

# --- Add Pets to Owner ---
owner.add_pet(buddy)
owner.add_pet(luna)

# --- Create Tasks ---
morning_walk = Task(title="Morning Walk",   duration=30, priority=5,
                    time="07:00", description="30 min walk around the block")
feeding = Task(title="Feeding",         duration=10, priority=4,
               time="08:00", description="Breakfast and fresh water")
grooming = Task(title="Grooming",        duration=20, priority=3,
                time="10:00", description="Brush coat and check ears")
playtime = Task(title="Playtime",        duration=15, priority=2,
                time="15:00", description="Interactive toy session")
vet_meds = Task(title="Give Medication", duration=5,  priority=5,
                time="09:00", description="Daily prescribed tablet")

# --- Assign Tasks to Pets ---
buddy.add_task(morning_walk)
buddy.add_task(feeding)
buddy.add_task(grooming)
luna.add_task(playtime)
luna.add_task(vet_meds)

# --- Build and Display Schedule ---
schedule = Schedule(date="2026-03-29", owner=owner)
schedule.generate_plan()
print("Today's Schedule")
schedule.display()

# --- Show reasoning ---
print()
print(schedule.explain_reasoning())
