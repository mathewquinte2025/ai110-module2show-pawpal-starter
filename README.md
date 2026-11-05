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

## ✨ Features

- **Pet management:** add pets with a name, species, and age in the Streamlit app. Duplicate pet names are rejected.
- **Task management:** schedule care tasks for a pet with a description, date, time, duration, priority, and frequency.
- **Sorting by date and time:** `Scheduler.sort_by_time()` lists every task from every pet in order of due date, then "HH:MM" time, earliest first.
- **Filtering:** `Scheduler.filter_tasks()` shows tasks for one pet, only finished or unfinished tasks, or both, and keeps them in time order.
- **Daily and weekly recurring tasks:** completing a `daily` task adds a new copy for the next day, and completing a `weekly` task adds one 7 days later, for the same pet.
- **One-time tasks:** tasks with frequency `once` are simply marked done and do not repeat.
- **Duplicate-completion protection:** completing a task that is already done does nothing, so a recurring task never creates two copies of its next occurrence.
- **Conflict detection:** `Scheduler.find_conflicts()` warns when two or more unfinished tasks are scheduled at the exact same date and time. Each warning names the tasks, their pets, and the time. It does not check whether task durations overlap.
- **Command-line demo:** `main.py` runs through all of these features with sample pets and prints the results.

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

The first part of the output from `python main.py` (the full output is in the Demo Walkthrough below):

```
Today's Schedule
07:30 - Litter Cleaning (Max)
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

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sorting | Scheduler.sort_by_time() | Returns all tasks from all pets, ordered by due date and then by their "HH:MM" time (earliest first). It uses sorted() with a lambda key. |
| Filtering | Scheduler.filter_tasks(pet_name=None, completed=None) | Returns the time-sorted tasks, optionally only for one pet (pet_name="Buddy"), only done or not-done tasks (completed=True / False), or both together. |
| Conflict detection | Scheduler.find_conflicts() | Looks for unfinished tasks scheduled at the exact same date and time (for the same pet or different pets). It returns readable warning messages that name each task and pet, and an empty list if there are no conflicts. It never raises an error. |
| Recurring tasks | Task.next_occurrence() and Scheduler.mark_task_complete(task) | When a "daily" or "weekly" task is completed, a new copy is added to the same pet with a due date 1 day or 7 days later (using timedelta). "once" tasks do not repeat. Completing the same task a second time does nothing, so it never creates duplicates. |

## 🚀 Demo Walkthrough

### Running the app

```bash
streamlit run app.py
```

### What you can do in the UI

| Section | What it does |
|---------|--------------|
| **Owner** | Set the owner's name and the minutes available today. |
| **Add a Pet** | Add a pet with a name, species, and age. Empty or duplicate names show an error. |
| **Add a Care Task** | Pick a pet and enter a description, date, time, duration, priority, and frequency (`once`, `daily`, or `weekly`). |
| **Mark a Task Complete** | Choose an unfinished task and mark it done. Recurring tasks automatically schedule their next occurrence. |
| **Your Pets** | One table per pet showing its tasks in date and time order. |
| **Schedule** | Conflict warnings, filters for pet and status, and a table of every matching task in chronological order. |

### Example workflow

1. In **Add a Pet**, enter `Buddy`, choose `Dog`, and click **Add pet**. A green success message confirms it. Add a second pet, `Max` the cat.
2. In **Add a Care Task**, choose `Buddy`, enter `Morning Walk` at `08:00`, set frequency to `daily`, and click **Add task**.
3. Add `Breakfast` for `Max` at `09:30`, then `Vet Visit` for `Buddy` also at `09:30` on the same date.
4. Scroll to **Schedule**. The tasks appear earliest first, no matter what order they were added in.
5. A yellow warning appears: *Vet Visit (Buddy) and Breakfast (Max) are scheduled at the same time (09:30 on ...)*. Completing one of the two tasks clears the warning, because finished tasks are not counted.
6. In **Mark a Task Complete**, choose `Morning Walk` and click **Mark complete**. The success message shows that the next walk is scheduled for tomorrow at 08:00.
7. Use the **Show pet** and **Show status** filters to see, for example, only Buddy's unfinished tasks or only completed tasks.

### How the scheduling features work

- **Sorting:** every schedule table uses `Scheduler.sort_by_time()` or `Scheduler.filter_tasks()`, which order tasks by due date and then by time.
- **Filtering:** the **Show pet** and **Show status** dropdowns are passed straight to `Scheduler.filter_tasks(pet_name, completed)`. "All" means no filter.
- **Recurring tasks:** `Scheduler.mark_task_complete()` marks the task done and calls `Task.next_occurrence()`. A `daily` task gets a copy one day later and a `weekly` task gets one seven days later. A `once` task is not repeated. Completing an already-finished task does nothing, so no duplicates are created.
- **Conflict warnings:** `Scheduler.find_conflicts()` groups unfinished tasks by their exact date and time. Any slot with two or more tasks becomes an `st.warning()` message. If there are no conflicts, an `st.success()` message says so. Completed tasks are not counted, and tasks that only overlap in duration (for example, 09:30 for 45 minutes and 10:00) are not flagged.

### CLI demo output

Running `python main.py` sets up Buddy and Max with five tasks and demonstrates sorting, filtering, recurrence, and conflict detection. Actual output (dates are based on the day it is run):

```
Today's Schedule
07:30 - Litter Cleaning (Max)
08:00 - Morning Walk (Buddy)
09:30 - Breakfast (Max)
11:00 - Grooming (Buddy)
18:00 - Evening Playtime (Max)

Tasks in the order they were added (unsorted):
  2026-11-04 11:00 - Grooming (Buddy) [to do]
  2026-11-04 08:00 - Morning Walk (Buddy) [to do]
  2026-11-04 09:30 - Breakfast (Max) [to do]
  2026-11-04 18:00 - Evening Playtime (Max) [to do]
  2026-11-04 07:30 - Litter Cleaning (Max) [to do]

Sorted by time:
  2026-11-04 07:30 - Litter Cleaning (Max) [to do]
  2026-11-04 08:00 - Morning Walk (Buddy) [to do]
  2026-11-04 09:30 - Breakfast (Max) [to do]
  2026-11-04 11:00 - Grooming (Buddy) [to do]
  2026-11-04 18:00 - Evening Playtime (Max) [to do]

Filtered: Buddy's tasks only
  2026-11-04 08:00 - Morning Walk (Buddy) [to do]
  2026-11-04 11:00 - Grooming (Buddy) [to do]

Recurring tasks:
  Completed 'Morning Walk' -> next one on 2026-11-05
  Completed 'Litter Cleaning' -> next one on 2026-11-11
  Completed 'Grooming' -> no repeat
  Completing 'Morning Walk' a second time -> new task created? False

Filtered: completed tasks
  2026-11-04 07:30 - Litter Cleaning (Max) [done]
  2026-11-04 08:00 - Morning Walk (Buddy) [done]
  2026-11-04 11:00 - Grooming (Buddy) [done]

Filtered: Buddy's unfinished tasks
  2026-11-05 08:00 - Morning Walk (Buddy) [to do]

Conflict check:
  Warning: Vet Visit (Buddy) and Breakfast (Max) are scheduled at the same time (09:30 on 2026-11-04).
```
