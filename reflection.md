# PawPal+ Project Reflection

## 1. System Design

1. Users should be able to add pets and enter basic information about them.
2. Users should be able to create pet care tasks, such as feeding, walking, and medication.
3. Users should be able to view a daily schedule that organizes tasks based on priority and available time.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design included four main classes: Owner, Pet, Task, and Scheduler.

The **Owner** class represents the pet owner and stores their name, available time, preferences, and pets. The **Pet** class represents each pet and stores its name, species, age, and assigned tasks. The **Task** class represents individual pet care activities and stores details such as description, time, duration, priority, frequency, and completion status. Finally, the **Scheduler** class manages the owner's tasks and organizes them by time.

The classes are connected so that an Owner can have multiple Pets, each Pet can have multiple Tasks, and the Scheduler can retrieve and organize tasks belonging to the Owner.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

--- After reviewing my initial design with an AI coding assistant, I made one change to improve the relationship between Task and Pet. I added a pet_name attribute to the Task class so each task can be associated with the pet it belongs to. This will make it easier for the Scheduler to display tasks with the correct pet name and allow tasks to be filtered by pet. The rest of the original design was kept because it already matched the UML diagram.

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
