# PawPal+ Project Reflection

## 1. System Design

1. Users should be able to add pets and enter basic information about them.
2. Users should be able to create pet care tasks, such as feeding, walking, and medication.
3. Users should be able to view a daily schedule that organizes tasks based on priority and available time.

### a. Initial design

My initial UML design included four main classes: Owner, Pet, Task, and Scheduler.

The **Owner** class represents the pet owner and stores their name, available time, preferences, and pets. The **Pet** class represents each pet and stores its name, species, age, and assigned tasks. The **Task** class represents individual pet care activities and stores details such as description, time, duration, priority, frequency, and completion status. Finally, the **Scheduler** class manages the owner's tasks and organizes them by time.

The classes are connected so that an Owner can have multiple Pets, each Pet can have multiple Tasks, and the Scheduler can retrieve and organize tasks belonging to the Owner.

### b. Design changes

My design changed slightly during implementation. After reviewing my initial design with an AI coding assistant, I added a `pet_name` attribute to the Task class. This allows each task to be associated with the pet it belongs to. It also makes it easier for the Scheduler to display tasks with the correct pet name and filter tasks by pet. The rest of the original design was kept because it already matched the needs of the project.

## 2. Scheduling Logic and Tradeoffs

### a. Constraints and priorities

My scheduler considers task dates, times, pet names, completion status, and recurrence. It can organize tasks chronologically, filter tasks by pet or completion status, and identify conflicts when unfinished tasks share the same date and start time. Priority and duration are stored with each task, but the scheduler does not currently use them to automatically allocate the owner's available time. I focused on organizing tasks and identifying scheduling conflicts because those were the main features needed for this project.

### b. Tradeoffs

My scheduler's conflict detection (`Scheduler.find_conflicts()`) only flags tasks that start at the exact same date and time. It does not check whether tasks overlap based on their durations. For example, a 45-minute Vet Visit at 09:30 and a 10-minute Breakfast at 09:40 would overlap in real life, but the scheduler would not warn about them because their start times are different.

I chose this tradeoff because exact matching is easy to read, easy to test, and matches the assignment's goal of lightweight conflict detection. Checking overlaps would require converting time strings into minutes, adding task durations, and comparing tasks. For a simple pet care app, warning the owner about exact duplicates is reasonable, and overlap checking could be a future improvement.

A related simplification is that conflicts ignore tasks that are already completed, since a finished task no longer competes for the owner's time.

## 3. AI Collaboration

### a. How you used AI

I used AI tools throughout the project to help plan the system design, create the UML diagram, develop the Python classes, build the Streamlit interface, and improve the documentation. I also used AI to review my code, identify possible improvements, and suggest additional tests. The most helpful prompts were specific instructions asking the AI to work on one project phase at a time and review the existing code before making changes.

### b. Judgment and verification

One suggestion I did not accept was adding a direct reference from each Task back to its Pet. I decided to keep the design simpler by using the `pet_name` attribute instead. I reviewed the code and tested the scheduler's filtering functionality to verify that tasks could still be associated with the correct pets.

I also verified AI-generated changes by running the automated tests and checking the application myself. This helped me make sure the suggested changes worked instead of accepting them without reviewing the results.

## 4. Testing and Verification

### a. What you tested

I tested adding pets, creating tasks, sorting tasks by date and time, filtering tasks by pet and completion status, marking tasks as complete, recurring tasks, and conflict detection. I also tested edge cases such as empty filter results, completed tasks being ignored during conflict detection, and recurring tasks continuing into a new month.

These tests were important because they helped verify that the scheduler worked correctly under different conditions and that changes did not break existing functionality.

### b. Confidence

I am fairly confident that the scheduler works correctly for the features implemented. All 14 automated tests passed, and I also tested the Streamlit interface. If I had more time, I would test overlapping tasks with different start times, invalid time inputs, and situations where the owner's available time is exceeded.

## 5. Reflection

### a. What went well

I am most satisfied with how the project developed from a basic UML design into a working Streamlit application. The scheduler can organize tasks, filter them, detect conflicts, and handle recurring tasks. I am also satisfied that I was able to test the system and improve its documentation throughout the project.

### b. What you would improve

If I had another iteration, I would improve the scheduling algorithm so it could consider task durations, priorities, and the owner's available time when organizing tasks. I would also improve conflict detection to identify overlapping tasks instead of only tasks with identical start times. Another improvement would be making the interface more visually organized and easier to navigate.

### c. Key takeaway

One important thing I learned is that designing a system before writing code makes implementation easier because it gives the project a clear structure. I also learned that AI can be helpful during software development, but its suggestions should be reviewed and tested instead of automatically accepted. Breaking a larger project into smaller phases made it easier to manage and complete.
