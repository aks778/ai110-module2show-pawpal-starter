# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling
New features include allowing the user to see conflicts between task times and duration, warn the user of such conflicts, filter the tasks by completion status, and sort the tasks based on time.

## Testing PawPal+
To run tests: python -m pytest
The tests check if tasks are assigned to pets correctly, if completion status of those tasks change as they are completed, if the tasks are sorted correctly by time, if tasks that have the label of "daily" have recurring occurrences, and lastly, if conflicts are accurately detected.
Confidence level: 5

## PawPal+ Scheduler Features

### 1. Core task scheduling
- **Priority-driven plan generation**
  - `Schedule.generate_plan()`: greedy sort by `Task.priority` (highest first)
  - Adds tasks until `Owner.time_available` is exhausted
- **Incomplete task filtering**
  - Skips tasks where `Task.is_complete == True`

### 2. Time-based ordering
- **Chronological sort**
  - `Schedule.sort_by_time()`: orders scheduled tasks by `Task.time` (HH:MM)
- **Display table output**
  - `app.py` uses `st.table()` to show sorted schedule and total time usage

### 3. Recurrence handling
- **Daily/weekly recurrence creation**
  - `Task.frequency`: `daily`, `weekly`, `as-needed`
  - `Schedule.complete_task(task)` generates next occurrence with `Task.next_occurrence()`
- **As-needed behavior**
  - does not create a new task after completion
- **Complete status toggle**
  - `Task.mark_complete()` updates completion state

### 4. Conflict detection & warnings
- **Time overlap detection**
  - `Schedule.find_conflicts()`: compares task intervals ([start,end)) and detects overlaps
- **Conflict warning text**
  - `Schedule.warn_conflicts()` returns user-friendly warning string
- **UI warning badge**
  - `app.py` shows warnings with `st.warning(conflict_warning)`

### 5. Owner/Pet/Task relationships
- **Owner → Pet**
  - `Owner.add_pet()`, `Owner.remove_pet()`, `Owner.get_all_tasks()`
- **Pet → Task**
  - `Pet.add_task()` sets `task.pet` and adds to `pet.tasks`

### 6. Reasoning and explainability
- **Plan reasoning log**
  - `Schedule.reasoning` stores selected/skipped entries
  - `Schedule.explain_reasoning()` returns an explanation string

### 7. Tests included
- Sorting correctness by time
- Daily recurrence after completion
- Conflict detection for overlapping task times
- Task completion status updates
- Task association with Pet

![PawPal demo screenshot](demo.png)

