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

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
Today's Schedule
08:00 - Morning Walk (Buddy)
09:30 - Breakfast (Max)
11:00 - Grooming (Buddy)
18:00 - Evening Playtime (Max)

```

## 🧪 Testing PawPal+

Run the full test suite from the project folder:

```bash
python -m pytest
```

The 14 tests in `tests/test_pawpal.py` check:

- **Basic tasks and pets:** marking a task complete changes its status, and adding a task increases the pet's task count.
- **Sorting:** tasks come back in chronological order, and earlier dates come first even when a later date has an earlier time.
- **Filtering:** tasks can be filtered by pet, by completion status, or both. A filter with no matches returns an empty list.
- **Recurring tasks:** completing a daily task creates a new one for the next day (including across a month boundary, keeping the same time, priority and description). Weekly tasks repeat 7 days later, one-time tasks do not repeat, and completing the same task twice does not create a duplicate.
- **Conflict detection:** two unfinished tasks at the same date and time give a warning that names both tasks and pets. Completed tasks are ignored, and pets with no tasks do not cause errors.

Test output:

```
============================= test session starts =============================
platform win32 -- Python 3.13.7, pytest-9.0.2, pluggy-1.6.0
collected 14 items

tests\test_pawpal.py ..............                                      [100%]

============================= 14 passed in 0.08s ==============================
```

**Confidence level: ★★★★☆ (4/5)**

The main scheduling behaviors (sorting, filtering, recurrence and conflict detection) are tested for both normal use and edge cases, and all 14 tests pass. It is not 5 stars because the tests only cover `pawpal_system.py`. The Streamlit UI in `app.py` is checked by hand, not by automated tests. Conflict detection also only catches tasks with the exact same start time, so tasks that overlap (for example, a 45-minute task at 09:30 and another task at 10:00) are not flagged.

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|

| Sorting | Scheduler.sort_by_time() | Returns all tasks from all pets, ordered by due date and then by their "HH:MM" time (earliest first). It uses sorted() with a lambda key. |

| Filtering | Scheduler.filter_tasks(pet_name=None, completed=None) | Returns the time-sorted tasks, optionally only for one pet (pet_name="Buddy"), only done or not-done tasks (completed=True / False), or both together. |

| Conflict detection | Scheduler.find_conflicts() | Looks for unfinished tasks scheduled at the exact same date and time (for the same pet or different pets). It returns readable warning messages that name each task and pet, and an empty list if there are no conflicts. It never raises an error. |

| Recurring tasks | Task.next_occurrence() and Scheduler.mark_task_complete(task) | When a "daily" or "weekly" task is completed, a new copy is added to the same pet with a due date 1 day or 7 days later (using timedelta). "once" tasks do not repeat. Completing the same task a second time does nothing, so it never creates duplicates. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
