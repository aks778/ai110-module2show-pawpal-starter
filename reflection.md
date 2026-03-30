# PawPal+ Project Reflection

## 1. System Design

It should allow the user to enter their information and their pets' information, add and change tasks, and create and display a daily schedule.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

For the UML design, I included classes Pet, Task, Owner, and Schedule. The Pet class had the responbility of giving characteristics to pets and the associated methods like getting the information about each pet. Then for Task, it had attributes like duration, description etc and then for methods like whether that task was done and whether it can be edited. Then for Owner, it had attributes like name, the pets it has etc. and the methods it would have like adding, removing pets for the owner. And then for the Schedule, it had characteristics like the date, owner, task, and reasoning and the methods like adding, removing tasks, and making new plans and explaining the reasoning for that task.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
Yes, I added the detecting conflicts feature as well as the warnings feature.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

It added constraints like task priority, the amount of time the owner is available for, and owner preferences.

- How did you decide which constraints mattered most?

The most importance constraint was task priority because it made sure that absolutely required tasks were completed first. The second most importance constraint was the amount of time the owner had. If the task duration exceeded this, it would be futile adding more tasks to the schedule.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The scheduler sorts by priority in such an order that it considers tasks with high priorities but long durations over tasks with lower priorities but much shorter durations, which could be better in another scenario, but its reasonable in this case because this project is aiming to work with the highest priority tasks first, rather than trying to fit the maxmimum number of tasks in a day.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

Used AI in design, debugging, fixing core implementation, and generating test cases.

- What kinds of prompts or questions were most helpful?

Prompts that were specific and included context were the most helpful.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

I did not accept the unnecessary tests it provided for testing. It included tests that were simply redundant. I evaluated what it suggested by rechecking the tests already included to make sure duplicate ones or unncecessary ones weren't included.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

I checked the ability to add tasks to a pet, assign pets to owners, ability to generate schedules, mark tasks as complete, find conflicts, and provide conflict warnings to the user.

- Why were these tests important?

These tests confirm that the core logic of the app works correctly. It reduces the chances that the main features break.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I'm very confident that the scheduler works as expected. I would check the recurring weekly tasks if I had more time.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I'm satisfied with how every feature works as expected and is able to catch edge cases.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would improve the scheduling aspect of the app, where users can view tasks in a timeline-like format for better user experience and app design.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

Working with AI still requires careful human oversight since it can add things which might not be required for the particular requirements of the system, leading to implementation that is much more complex than what is required.


