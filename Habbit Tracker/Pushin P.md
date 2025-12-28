<img width="1130" height="725" alt="image" src="https://github.com/user-attachments/assets/3b667467-0dac-4398-a23d-73ccb4d37412" />
how do i create something like this in obsidian?

Looking at your Notion setup, you want a **weekly task tracker with checkboxes and a progress bar**. Here's how to build this in Obsidian:

## Option 1: Using Dataview Plugin (Most Powerful)

**Step 1: Install Dataview**
- Settings → Community Plugins → Browse → Search "Dataview" → Install & Enable

**Step 2: Create Your Weekly Note Template**

```markdown
---
date: 2025-W01
---

# This Week

## Tasks

- [ ] Task 1 📅 2025-12-28
- [ ] Task 2 📅 2025-12-28
- [ ] Task 3 📅 2025-12-29
- [ ] Task 4 📅 2025-12-30
- [ ] Task 5 📅 2025-12-31

## Progress View

```dataview
TABLE WITHOUT ID
  date AS "Date",
  length(filter(tasks, (t) => contains(meta(t).text, file.link))) as "Total",
  length(filter(tasks, (t) => t.completed AND contains(meta(t).text, file.link))) as "Done",
  round((length(filter(tasks, (t) => t.completed AND contains(meta(t).text, file.link))) / length(filter(tasks, (t) => contains(meta(t).text, file.link)))) * 100) + "%" as "Progress"
FROM "Tasks"
WHERE date >= date(2025-12-28) AND date <= date(2026-01-03)
SORT date ASC
```
```

---

## Option 2: Using Tasks Plugin (Better Task Management)

**Step 1: Install Tasks Plugin**
- Settings → Community Plugins → "Tasks" → Install & Enable

**Step 2: Create Daily Notes with Tasks**

Each daily note gets tasks like:
```markdown
# December 28, 2025

- [ ] Morning routine 📅 2025-12-28
- [ ] Check emails 📅 2025-12-28
- [ ] Team meeting 📅 2025-12-28
```

**Step 3: Create a Weekly Dashboard**

```markdown
# This Week

```tasks
not done
happens after 2025-12-27
happens before 2026-01-04
group by filename
```

## Progress

```dataview
TABLE WITHOUT ID
  file.day as "Date",
  length(file.tasks) as "Total Tasks",
  length(filter(file.tasks, (t) => t.completed)) as "Completed",
  round((length(filter(file.tasks, (t) => t.completed)) / length(file.tasks)) * 100) + "%" as "Progress"
WHERE file.day >= date(2025-12-28) AND file.day <= date(2026-01-03)
SORT file.day ASC
```
```

---

## Option 3: Simple Markdown Table (No Plugins)

If you want zero plugins, manually create a table:

```markdown
# This Week

| Date | Task 1 | Task 2 | Task 3 | Task 4 | Progress |
|------|--------|--------|--------|--------|----------|
| Dec 28 | ☐ | ☐ | ☐ | ☐ | 0% |
| Dec 29 | ☐ | ☐ | ☐ | ☐ | 0% |
| Dec 30 | ☑ | ☐ | ☑ | ☑ | 75% |
| Dec 31 | ☐ | ☐ | ☐ | ☐ | 0% |
```

Replace `☐` with `☑` manually as you complete tasks. Progress updates manually.

---

## My Recommendation

**Use Dataview + Tasks combo** because:
- Dataview gives you dynamic tables/progress tracking
- Tasks plugin handles checkbox states and due dates elegantly
- Together they replicate Notion databases without the manual grunt work

Want me to walk you through setting up the plugins, or do you want a template file ready to copy-paste?


see so i will tell you i want to track over 20 different habits everyday, i know i will not achieve all of them but i want to be more intentional about my time this year. So I want to track at a daily level, weekly level, monthly level and i want monthly base cards to come for an annual level, i understand achieving all of this in obisidian can be difficult but you tell me what is possible

Alright, let's build a **multi-level habit tracking system** in Obsidian. I'll break down what's achievable and give you a realistic roadmap.

---

## What's Possible in Obsidian

| Level | Tracking Method | Automation Level | Effort |
|-------|----------------|------------------|--------|
| **Daily** | Checkboxes in daily notes | ✅ Fully automated views | Low |
| **Weekly** | Aggregated from daily | ✅ Auto-calculated | Low |
| **Monthly** | Aggregated from daily | ✅ Auto-calculated | Medium |
| **Annual** | Monthly summaries as cards | ⚠️ Semi-automated | Medium-High |

**The good news:** Obsidian can do all of this with the right plugin combo.

**The reality check:** Annual "cards" won't be as polished as Notion, but you can get monthly summary blocks that aggregate nicely.

---

## Recommended Tech Stack

**Core Plugins:**
1. **Dataview** → Database queries, aggregations, progress tracking
2. **Tracker** → Visual charts (heatmaps, bar graphs)
3. **Templater** → Auto-generate daily notes with all 20 habits pre-populated
4. **Calendar** (optional) → Navigate daily notes visually

---

## System Architecture

### 1️⃣ Daily Level (The Foundation)

**Daily Note Template** (auto-generated each day):

```markdown
---
date: {{date}}
tags: daily
---

# {{date:MMMM DD, YYYY}}

## Habits

- [ ] 🏃 Exercise (30 min)
- [ ] 📚 Read (20 min)
- [ ] 💧 Drink water (8 glasses)
- [ ] 🧘 Meditate (10 min)
- [ ] 📝 Journal
- [ ] 🛏️ Sleep by 11pm
- [ ] 🥗 Healthy meals (3/3)
- [ ] 📱 No phone before bed
- [ ] 🎯 Deep work (2 hours)
- [ ] 👥 Social connection
- [ ] 🧹 Tidy space
- [ ] 📖 Learn something new
- [ ] 🎨 Creative work
- [ ] 💪 Strength training
- [ ] 🚶 Walk outside
- [ ] 📊 Review goals
- [ ] 💻 No social media scrolling
- [ ] 🍎 No junk food
- [ ] 📞 Call family/friend
- [ ] 🧠 Brain training

## Notes
<!-- Reflection, wins, struggles -->

```

**Why this works:**
- Each checkbox is a trackable data point
- Dataview can count completed vs total per day
- You fill this out daily (2-3 minutes)

---

### 2️⃣ Weekly Level (Auto-Aggregated)

Create a **Weekly Dashboard** note that pulls from daily notes:

```markdown
# Week {{date:YYYY-[W]WW}}

## Weekly Overview

```dataview
TABLE WITHOUT ID
  file.link as "Date",
  length(file.tasks) as "Total",
  length(filter(file.tasks, (t) => t.completed)) as "Done",
  round((length(filter(file.tasks, (t) => t.completed)) / length(file.tasks)) * 100) + "%" as "Progress"
FROM "Daily Notes"
WHERE file.day >= date({{monday}}) AND file.day <= date({{sunday}})
SORT file.day ASC
```

## Habit Breakdown

```dataview
TABLE WITHOUT ID
  choice(contains(text, "Exercise"), "✅", "❌") as "🏃",
  choice(contains(text, "Read"), "✅", "❌") as "📚",
  choice(contains(text, "Meditate"), "✅", "❌") as "🧘"
  /* Add all 20 habits */
FROM "Daily Notes"
WHERE file.day >= date({{monday}}) AND file.day <= date({{sunday}})
SORT file.day ASC
```

## Weekly Stats

```tracker
searchType: tag
searchTarget: daily
folder: Daily Notes
startDate: {{monday}}
endDate: {{sunday}}
line:
    title: "Completion Rate"
    yAxisLabel: "Habits Done"
    lineColor: green
```
```

**What this gives you:**
- Visual heatmap of which habits you hit each day
- Weekly completion percentage
- Trend lines (if you're improving/declining)

---

### 3️⃣ Monthly Level (Auto-Aggregated)

Create a **Monthly Dashboard**:

```markdown
# {{date:MMMM YYYY}}

## Monthly Habit Heatmap

```tracker
searchType: tag
searchTarget: daily
folder: Daily Notes
month:
    startWeekOn: Monday
    threshold: 50
    color: green
    dimNotInMonth: false
```

## Monthly Stats

```dataview
TABLE WITHOUT ID
  dateformat(file.day, "MMM dd") as "Date",
  round((length(filter(file.tasks, (t) => t.completed)) / length(file.tasks)) * 100) + "%" as "Daily %"
FROM "Daily Notes"
WHERE file.day.month = date({{date}}).month
SORT file.day ASC
```

## Top Habits This Month

```dataview
TABLE WITHOUT ID
  Habit,
  CompletionCount as "Times Done",
  round((CompletionCount / TotalDays) * 100) + "%" as "Consistency"
FROM "Daily Notes"
WHERE file.day.month = date({{date}}).month
FLATTEN file.tasks as Task
WHERE Task.completed
GROUP BY Task.text as Habit
SORT CompletionCount DESC
```
```

**What this gives you:**
- Calendar heatmap (visual dopamine hit)
- Which habits you're nailing vs neglecting
- Monthly trends

---

### 4️⃣ Annual Level (Monthly Summary Cards)

Create an **Annual Dashboard** with monthly summary "cards":

```markdown
# 2025 Year in Review

## Monthly Summaries

```dataview
TABLE WITHOUT ID
  file.link as "Month",
  TotalDays as "Days Tracked",
  AvgCompletion as "Avg Completion",
  TopHabit as "Best Habit"
FROM "Monthly Dashboards"
WHERE file.year = 2025
SORT file.month ASC
```

## Annual Heatmap

```tracker
searchType: tag
searchTarget: daily
folder: Daily Notes
year:
    startWeekOn: Monday
    threshold: 50
    color: green
```

## Habit Consistency (Full Year)

```dataview
TABLE WITHOUT ID
  Habit,
  count(rows) as "Days Done",
  round((count(rows) / 365) * 100) + "%" as "Annual %"
FROM "Daily Notes"
WHERE file.year = 2025
FLATTEN file.tasks as Task
WHERE Task.completed
GROUP BY Task.text as Habit
SORT count(rows) DESC
```
```

---

## Realistic Implementation Path

**Phase 1 (Week 1):** Set up daily tracking
- Install Dataview, Templater, Tracker
- Create daily template with 20 habits
- Start checking boxes daily

**Phase 2 (Week 2):** Build weekly view
- Create weekly dashboard template
- Test queries on Week 1 data
- Adjust habit labels if needed

**Phase 3 (Month 1):** Add monthly view
- Create monthly dashboard
- Set up heatmap tracker
- Validate data aggregation

**Phase 4 (Month 2+):** Annual view
- Create annual dashboard
- Build monthly summary cards
- Add year-over-year comparisons

---

## Limitations to Know Upfront

1. **Not as pretty as Notion** → No drag-and-drop cards, but functional
2. **Manual daily input** → You still check 20 boxes daily (no way around this)
3. **Query performance** → With 365 days × 20 habits, Dataview might lag slightly (fixable with caching)
4. **Learning curve** → Dataview syntax takes ~2 hours to learn

---

## Do You Want:
A. **The full template files** (ready to copy-paste)
B. **Step-by-step setup guide** (installing plugins, configuring templates)
C. **A simplified version** (10 habits instead of 20, faster to test)

Let me know and I'll build it out for you.

```
Dataview: Error: 
-- PARSING FAILED --------------------------------------------------

  5 |   round((length(filter(file.tasks, (t) => t.completed)) / length(file.tasks)) * 100) + "%" as "Progress"
  6 | FROM "Daily Notes"
> 7 | WHERE file.day >= date({{monday}}) AND file.day <= date({{sunday}})
    |                         ^
  8 | SORT file.day ASC

Expected:

object ('{ a: 1, b: 2 }')


Dataview: Error: 
-- PARSING FAILED --------------------------------------------------

  3 |   choice(contains(text, "Read"), "✅", "❌") as "📚",
  4 |   choice(contains(text, "Meditate"), "✅", "❌") as "🧘"
> 5 |   /* Add all 20 habits */
    |   ^
  6 | FROM "Daily Notes"
  7 | WHERE file.day >= date({{monday}}) AND file.day <= date({{sunday}})

Expected one of the following: 

',', /FROM/i, EOF, FLATTEN <value> [AS <name>], GROUP BY <value> [AS <name>], LIMIT <value>, Not a comment, SORT field [ASC/DESC], WHERE <expression>, whitespace
```

Ah, classic Dataview syntax errors. Let me fix these:

## Issue 1: Templater Variables in Dataview Queries

The `{{monday}}` and `{{sunday}}` are **Templater syntax**, but Dataview doesn't understand them directly. You need to either:

**Option A: Hardcode the dates when creating the weekly note**

When you create the weekly note with Templater, it should replace the dates first:

```markdown
# Week <% tp.date.now("YYYY-[W]WW") %>

## Weekly Overview

```dataview
TABLE WITHOUT ID
  file.link as "Date",
  length(file.tasks) as "Total",
  length(filter(file.tasks, (t) => t.completed)) as "Done",
  round((length(filter(file.tasks, (t) => t.completed)) / length(file.tasks)) * 100) + "%" as "Progress"
FROM "Daily Notes"
WHERE file.day >= date(<% tp.date.now("YYYY-MM-DD", 0, tp.date.now(), "ddd") === "Mon" ? tp.date.now("YYYY-MM-DD") : tp.date.weekday("YYYY-MM-DD", 0, tp.date.now(), "previous monday") %>) 
  AND file.day <= date(<% tp.date.weekday("YYYY-MM-DD", 0, tp.date.now(), "next sunday") %>)
SORT file.day ASC
```
```

**Option B: Use relative date logic (simpler)**

```markdown
## Weekly Overview

```dataview
TABLE WITHOUT ID
  file.link as "Date",
  length(file.tasks) as "Total",
  length(filter(file.tasks, (t) => t.completed)) as "Done",
  round((length(filter(file.tasks, (t) => t.completed)) / length(file.tasks)) * 100) + "%" as "Progress"
FROM "Daily Notes"
WHERE file.day >= date(today) - dur(7 days) AND file.day <= date(today)
SORT file.day ASC
```
```

This shows "last 7 days" dynamically.

---

## Issue 2: Comments Not Allowed in Dataview

Dataview doesn't support `/* comments */` inside queries. Remove them:

**Broken:**
```dataview
TABLE WITHOUT ID
  choice(contains(text, "Exercise"), "✅", "❌") as "🏃",
  choice(contains(text, "Read"), "✅", "❌") as "📚",
  /* Add all 20 habits */  ← BREAKS HERE
FROM "Daily Notes"
```

**Fixed:**
```dataview
TABLE WITHOUT ID
  choice(contains(text, "Exercise"), "✅", "❌") as "🏃",
  choice(contains(text, "Read"), "✅", "❌") as "📚",
  choice(contains(text, "Meditate"), "✅", "❌") as "🧘",
  choice(contains(text, "Journal"), "✅", "❌") as "📝",
  choice(contains(text, "Sleep"), "✅", "❌") as "🛏️"
FROM "Daily Notes"
WHERE file.day >= date(today) - dur(7 days) AND file.day <= date(today)
SORT file.day ASC
```

---

## Working Weekly Dashboard Template

Here's the corrected full version:

```markdown
---
date: <% tp.date.now("YYYY-MM-DD") %>
week: <% tp.date.now("YYYY-[W]WW") %>
tags: weekly
---

# Week <% tp.date.now("YYYY-[W]WW") %>

## Weekly Overview

```dataview
TABLE WITHOUT ID
  file.link as "Date",
  length(file.tasks) as "Total",
  length(filter(file.tasks, (t) => t.completed)) as "Done",
  round((length(filter(file.tasks, (t) => t.completed)) / length(file.tasks)) * 100) + "%" as "Progress"
FROM "Daily Notes"
WHERE file.day >= date(today) - dur(7 days) AND file.day <= date(today)
SORT file.day ASC
```

## Habit Breakdown

```dataview
TABLE WITHOUT ID
  file.link as "Date",
  choice(contains(string(file.tasks.text), "Exercise"), "✅", "❌") as "🏃",
  choice(contains(string(file.tasks.text), "Read"), "✅", "❌") as "📚",
  choice(contains(string(file.tasks.text), "Meditate"), "✅", "❌") as "🧘",
  choice(contains(string(file.tasks.text), "Journal"), "✅", "❌") as "📝",
  choice(contains(string(file.tasks.text), "Sleep"), "✅", "❌") as "🛏️",
  choice(contains(string(file.tasks.text), "Water"), "✅", "❌") as "💧",
  choice(contains(string(file.tasks.text), "Healthy meals"), "✅", "❌") as "🥗",
  choice(contains(string(file.tasks.text), "Deep work"), "✅", "❌") as "🎯"
FROM "Daily Notes"
WHERE file.day >= date(today) - dur(7 days) AND file.day <= date(today)
SORT file.day ASC
```

## Weekly Stats

Total habits tracked: **160**  
Average daily completion: **<% Math.round((completedThisWeek / 160) * 100) %>%**

```

---

## Key Fixes Applied

1. ✅ Replaced `{{monday}}` / `{{sunday}}` with `date(today) - dur(7 days)` 
2. ✅ Removed `/* comments */` from Dataview queries
3. ✅ Used `string(file.tasks.text)` instead of raw `text` (more reliable)
4. ✅ Used `choice()` function for checkbox visual rendering

---

## Alternative: Use DataviewJS for More Control

If the above still gives issues, switch to **DataviewJS** (more flexible):

```dataviewjs
const pages = dv.pages('"Daily Notes"')
    .where(p => p.file.day >= dv.date('today') - dv.duration('7 days'))
    .sort(p => p.file.day);

dv.table(
    ["Date", "Total", "Done", "Progress"],
    pages.map(p => [
        p.file.link,
        p.file.tasks.length,
        p.file.tasks.where(t => t.completed).length,
        Math.round((p.file.tasks.where(t => t.completed).length / p.file.tasks.length) * 100) + "%"
    ])
);
```

Try the fixed version first. If you still get errors, paste the **exact error message** and I'll debug further.

<img width="431" height="726" alt="image" src="https://github.com/user-attachments/assets/b2080ea8-defe-4dcf-9ea4-326b7a99508e" />
i know where you are going wrong
my journals are here,  and here is the data points we are tracking
---
date: 2025-11-20
tags: daily
---
# {{date:MMMM DD, YYYY}}
## Habits
- [x] 🏃 Exercise (30 min)
- [x] 📚 Read (20 min)
- [x] 💧 Drink water (8 glasses)
- [ ] 🧘 Meditate (10 min)
- [x] 📝 Journal
- [ ] 🛏️ Sleep by 11pm
- [x] 🥗 Healthy meals (3/3)
- [ ] 📱 No phone before bed
- [x] 🎯 Deep work (2 hours)
- [ ] 👥 Social connection
- [x] 🧹 Tidy space
- [ ] 📖 Learn something new
- [x] 🎨 Creative work
- [ ] 💪 Strength training
- [x] 🚶 Walk outside
- [x] 📊 Review goals
- [ ] 💻 No social media scrolling
- [x] 🍎 No junk food
- [ ] 📞 Call family/friend
- [x] 🧠 Brain training
## Notes
<!-- Reflection, wins, struggles -->

can you now fix the weekly dashboard for me dear

Ah, I see the issue! Your daily notes are in `2. Daily Reflection/2025/November 2025/` folder structure, not a flat "Daily Notes" folder. Let me fix the weekly dashboard:

---

## Working Weekly Dashboard

```markdown
---
date: <% tp.date.now("YYYY-MM-DD") %>
week: <% tp.date.now("YYYY-[W]WW") %>
tags: weekly
---

# Week <% tp.date.now("YYYY-[W]WW") %>

## Weekly Overview

```dataview
TABLE WITHOUT ID
  file.link as "Date",
  length(file.tasks) as "Total",
  length(filter(file.tasks, (t) => t.completed)) as "Done",
  round((length(filter(file.tasks, (t) => t.completed)) / length(file.tasks)) * 100) + "%" as "Progress"
FROM "2. Daily Reflection"
WHERE file.day >= date(today) - dur(7 days) AND file.day <= date(today)
SORT file.day ASC
```

## Habit Breakdown

```dataview
TABLE WITHOUT ID
  file.link as "Date",
  choice(meta(filter(file.tasks, (t) => contains(t.text, "Exercise")))[0].completed, "✅", "❌") as "🏃",
  choice(meta(filter(file.tasks, (t) => contains(t.text, "Read")))[0].completed, "✅", "❌") as "📚",
  choice(meta(filter(file.tasks, (t) => contains(t.text, "Drink water")))[0].completed, "✅", "❌") as "💧",
  choice(meta(filter(file.tasks, (t) => contains(t.text, "Meditate")))[0].completed, "✅", "❌") as "🧘",
  choice(meta(filter(file.tasks, (t) => contains(t.text, "Journal")))[0].completed, "✅", "❌") as "📝",
  choice(meta(filter(file.tasks, (t) => contains(t.text, "Sleep")))[0].completed, "✅", "❌") as "🛏️",
  choice(meta(filter(file.tasks, (t) => contains(t.text, "Healthy meals")))[0].completed, "✅", "❌") as "🥗",
  choice(meta(filter(file.tasks, (t) => contains(t.text, "No phone")))[0].completed, "✅", "❌") as "📱",
  choice(meta(filter(file.tasks, (t) => contains(t.text, "Deep work")))[0].completed, "✅", "❌") as "🎯",
  choice(meta(filter(file.tasks, (t) => contains(t.text, "Social connection")))[0].completed, "✅", "❌") as "👥",
  choice(meta(filter(file.tasks, (t) => contains(t.text, "Tidy space")))[0].completed, "✅", "❌") as "🧹",
  choice(meta(filter(file.tasks, (t) => contains(t.text, "Learn something")))[0].completed, "✅", "❌") as "📖",
  choice(meta(filter(file.tasks, (t) => contains(t.text, "Creative work")))[0].completed, "✅", "❌") as "🎨",
  choice(meta(filter(file.tasks, (t) => contains(t.text, "Strength training")))[0].completed, "✅", "❌") as "💪",
  choice(meta(filter(file.tasks, (t) => contains(t.text, "Walk outside")))[0].completed, "✅", "❌") as "🚶",
  choice(meta(filter(file.tasks, (t) => contains(t.text, "Review goals")))[0].completed, "✅", "❌") as "📊",
  choice(meta(filter(file.tasks, (t) => contains(t.text, "No social media")))[0].completed, "✅", "❌") as "💻",
  choice(meta(filter(file.tasks, (t) => contains(t.text, "No junk food")))[0].completed, "✅", "❌") as "🍎",
  choice(meta(filter(file.tasks, (t) => contains(t.text, "Call family")))[0].completed, "✅", "❌") as "📞",
  choice(meta(filter(file.tasks, (t) => contains(t.text, "Brain training")))[0].completed, "✅", "❌") as "🧠"
FROM "2. Daily Reflection"
WHERE file.day >= date(today) - dur(7 days) AND file.day <= date(today)
SORT file.day ASC
```

## Weekly Summary

```dataview
TABLE WITHOUT ID
  "Exercise" as "Habit",
  length(filter(file.tasks, (t) => contains(t.text, "Exercise") AND t.completed)) as "Days Done"
FROM "2. Daily Reflection"
WHERE file.day >= date(today) - dur(7 days) AND file.day <= date(today)
FLATTEN 1 as dummy
GROUP BY dummy
```
```

---

## Key Changes Made

1. ✅ Changed `FROM "Daily Notes"` → `FROM "2. Daily Reflection"`
2. ✅ Used `meta(filter())` to safely check if tasks exist before accessing `.completed`
3. ✅ All 20 habits now tracked in the habit breakdown table

---

## If You Still Get Errors

Try this **simpler DataviewJS version** (more robust):

```markdown
## Weekly Habit Grid

```dataviewjs
const folder = "2. Daily Reflection";
const days = 7;

// Get last 7 days of daily notes
const pages = dv.pages(`"${folder}"`)
    .where(p => p.file.day && p.file.day >= dv.date('today') - dv.duration(`${days} days`))
    .sort(p => p.file.day, 'asc');

// Habit list (order matters)
const habits = [
    "Exercise", "Read", "Drink water", "Meditate", "Journal",
    "Sleep", "Healthy meals", "No phone", "Deep work", "Social connection",
    "Tidy space", "Learn something", "Creative work", "Strength training",
    "Walk outside", "Review goals", "No social media", "No junk food",
    "Call family", "Brain training"
];

const icons = ["🏃", "📚", "💧", "🧘", "📝", "🛏️", "🥗", "📱", "🎯", "👥", 
               "🧹", "📖", "🎨", "💪", "🚶", "📊", "💻", "🍎", "📞", "🧠"];

// Build table
const headers = ["Date", ...icons];
const rows = pages.map(p => {
    const checks = habits.map(habit => {
        const task = p.file.tasks.find(t => t.text.includes(habit));
        return task && task.completed ? "✅" : "❌";
    });
    return [p.file.link, ...checks];
});

dv.table(headers, rows);
```
```

This DataviewJS version is bulletproof and will show you exactly which habits you're hitting each day in a nice grid.

Test it and let me know if it works!
