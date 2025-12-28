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
```
Dataview: Every row during final data extraction failed with an error; first 3:

            - No implementation of 'meta' found for arguments: array

is this happening because we did not put the habits in yaml or can we pick it from the content of the page like we are doing now?
```

Good catch! The `meta()` function doesn't work the way I used it. We can **definitely** pick habits from the page content (no YAML needed), but we need to fix the syntax.

Here's the corrected version:

---

## Fixed Weekly Dashboard (Pure Dataview)

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
  length(filter(file.tasks, (t) => contains(t.text, "Exercise") AND t.completed)) > 0 as "🏃",
  length(filter(file.tasks, (t) => contains(t.text, "Read") AND t.completed)) > 0 as "📚",
  length(filter(file.tasks, (t) => contains(t.text, "Drink water") AND t.completed)) > 0 as "💧",
  length(filter(file.tasks, (t) => contains(t.text, "Meditate") AND t.completed)) > 0 as "🧘",
  length(filter(file.tasks, (t) => contains(t.text, "Journal") AND t.completed)) > 0 as "📝",
  length(filter(file.tasks, (t) => contains(t.text, "Sleep") AND t.completed)) > 0 as "🛏️",
  length(filter(file.tasks, (t) => contains(t.text, "Healthy meals") AND t.completed)) > 0 as "🥗",
  length(filter(file.tasks, (t) => contains(t.text, "No phone") AND t.completed)) > 0 as "📱",
  length(filter(file.tasks, (t) => contains(t.text, "Deep work") AND t.completed)) > 0 as "🎯",
  length(filter(file.tasks, (t) => contains(t.text, "Social connection") AND t.completed)) > 0 as "👥",
  length(filter(file.tasks, (t) => contains(t.text, "Tidy space") AND t.completed)) > 0 as "🧹",
  length(filter(file.tasks, (t) => contains(t.text, "Learn something") AND t.completed)) > 0 as "📖",
  length(filter(file.tasks, (t) => contains(t.text, "Creative work") AND t.completed)) > 0 as "🎨",
  length(filter(file.tasks, (t) => contains(t.text, "Strength training") AND t.completed)) > 0 as "💪",
  length(filter(file.tasks, (t) => contains(t.text, "Walk outside") AND t.completed)) > 0 as "🚶",
  length(filter(file.tasks, (t) => contains(t.text, "Review goals") AND t.completed)) > 0 as "📊",
  length(filter(file.tasks, (t) => contains(t.text, "No social media") AND t.completed)) > 0 as "💻",
  length(filter(file.tasks, (t) => contains(t.text, "No junk food") AND t.completed)) > 0 as "🍎",
  length(filter(file.tasks, (t) => contains(t.text, "Call family") AND t.completed)) > 0 as "📞",
  length(filter(file.tasks, (t) => contains(t.text, "Brain training") AND t.completed)) > 0 as "🧠"
FROM "2. Daily Reflection"
WHERE file.day >= date(today) - dur(7 days) AND file.day <= date(today)
SORT file.day ASC
```
```

---

## What Changed

**Old (broken):**
```dataview
choice(meta(filter(file.tasks, (t) => contains(t.text, "Exercise")))[0].completed, "✅", "❌")
```

**New (working):**
```dataview
length(filter(file.tasks, (t) => contains(t.text, "Exercise") AND t.completed)) > 0
```

**Why this works:**
- `filter()` returns matching tasks
- We check if the task contains "Exercise" **AND** is completed
- `length() > 0` returns `true` (✅) or `false` (❌)
- Dataview auto-renders `true`/`false` as checkboxes

---

## But Honestly, Use DataviewJS Instead

The DataviewJS version I gave you earlier is **much cleaner** and actually gives you ✅/❌ symbols. Here it is again:

```markdown
## Weekly Habit Grid

```dataviewjs
const folder = "2. Daily Reflection";
const days = 7;

// Get last 7 days of daily notes
const pages = dv.pages(`"${folder}"`)
    .where(p => p.file.day && p.file.day >= dv.date('today') - dv.duration(`${days} days`))
    .sort(p => p.file.day, 'asc');

// Habit list
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

---

## My Recommendation

**Use the DataviewJS version** because:
1. ✅ Cleaner syntax
2. ✅ Easier to debug
3. ✅ Better visual output (✅/❌ instead of true/false)
4. ✅ No weird Dataview query limitations

Try the DataviewJS version and let me know if it works. If you get errors, paste them and I'll fix it.

<img width="1568" height="566" alt="image" src="https://github.com/user-attachments/assets/0b5b158c-0da4-42eb-8c0a-317d50437845" />
nah bro, this is not working  come one do something

Alright, let's fix this properly. Two issues:

1. **Templater syntax isn't rendering** (the title shows raw code)
2. **Query is looking at the wrong date** (25-12-25 instead of current week)

---

## Step 1: Check Your Setup

**Is Templater installed and enabled?**
- Settings → Community Plugins → Make sure "Templater" is installed AND enabled
- Settings → Templater → Set a "Template folder location" (e.g., `Templates/`)

---

## Step 2: Corrected Weekly Dashboard Template

Save this as a **template file** (e.g., `Templates/Weekly Dashboard.md`):

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
WHERE file.day >= date(2025-12-22) AND file.day <= date(2025-12-28)
SORT file.day ASC
```

## Weekly Habit Grid

```dataviewjs
const folder = "2. Daily Reflection";
const startDate = "2025-12-22"; // Monday of this week
const endDate = "2025-12-28";   // Sunday of this week

// Get this week's daily notes
const pages = dv.pages(`"${folder}"`)
    .where(p => p.file.day && p.file.day >= dv.date(startDate) && p.file.day <= dv.date(endDate))
    .sort(p => p.file.day, 'asc');

// Habit list
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

if (rows.length === 0) {
    dv.paragraph("No daily notes found for this week. Check your date range!");
} else {
    dv.table(headers, rows);
}
```
```

---

## Step 3: Create the Weekly Note PROPERLY

**Don't just copy-paste the template.** Instead:

1. **Open Command Palette** (`Ctrl/Cmd + P`)
2. Type: **"Templater: Create new note from template"**
3. Select your `Weekly Dashboard` template
4. Templater will **replace the `<% %>` codes** with actual dates

---

## Alternative: Manual Version (No Templater Needed)

If Templater is being a pain, just hardcode the dates each week:

```markdown
---
date: 2025-12-28
week: 2025-W52
tags: weekly
---

# Week 2025-W52

## Weekly Overview

```dataview
TABLE WITHOUT ID
  file.link as "Date",
  length(file.tasks) as "Total",
  length(filter(file.tasks, (t) => t.completed)) as "Done",
  round((length(filter(file.tasks, (t) => t.completed)) / length(file.tasks)) * 100) + "%" as "Progress"
FROM "2. Daily Reflection"
WHERE file.day >= date(2025-12-22) AND file.day <= date(2025-12-28)
SORT file.day ASC
```

## Weekly Habit Grid

```dataviewjs
const folder = "2. Daily Reflection";
const startDate = "2025-12-22";
const endDate = "2025-12-28";

const pages = dv.pages(`"${folder}"`)
    .where(p => p.file.day && p.file.day >= dv.date(startDate) && p.file.day <= dv.date(endDate))
    .sort(p => p.file.day, 'asc');

const habits = [
    "Exercise", "Read", "Drink water", "Meditate", "Journal",
    "Sleep", "Healthy meals", "No phone", "Deep work", "Social connection",
    "Tidy space", "Learn something", "Creative work", "Strength training",
    "Walk outside", "Review goals", "No social media", "No junk food",
    "Call family", "Brain training"
];

const icons = ["🏃", "📚", "💧", "🧘", "📝", "🛏️", "🥗", "📱", "🎯", "👥", 
               "🧹", "📖", "🎨", "💪", "🚶", "📊", "💻", "🍎", "📞", "🧠"];

const headers = ["Date", ...icons];
const rows = pages.map(p => {
    const checks = habits.map(habit => {
        const task = p.file.tasks.find(t => t.text.includes(habit));
        return task && task.completed ? "✅" : "❌";
    });
    return [p.file.link, ...checks];
});

if (rows.length === 0) {
    dv.paragraph("❌ No daily notes found. Check folder path and dates!");
} else {
    dv.table(headers, rows);
}
```
```

---

## Debugging Checklist

If it **still** shows "false false false":

1. **Check DataviewJS is enabled:**
   - Settings → Dataview → Enable "Enable JavaScript Queries"

2. **Check your daily note filenames:**
   - Are they named like `20-11-2025.md`? 
   - Dataview needs the `date:` in frontmatter OR the filename to be `YYYY-MM-DD` format

3. **Add this debug query to see what Dataview finds:**

```dataviewjs
dv.paragraph("Looking in folder: 2. Daily Reflection");
const allPages = dv.pages('"2. Daily Reflection"');
dv.paragraph(`Found ${allPages.length} total pages`);
const pagesWithDates = allPages.where(p => p.file.day);
dv.paragraph(`Pages with dates: ${pagesWithDates.length}`);
pagesWithDates.forEach(p => {
    dv.paragraph(`- ${p.file.name}: ${p.file.day}, Tasks: ${p.file.tasks.length}`);
});
```

Run this and **paste the output**. That'll tell us exactly what's wrong.

<img width="1568" height="517" alt="image" src="https://github.com/user-attachments/assets/3060ffa2-3f15-401a-81d9-7bffa0cbe553" />
<img width="702" height="843" alt="image" src="https://github.com/user-attachments/assets/08c8066a-fae8-4b4e-965f-29d93d3ad9fd" />

i did templater, i ensured enable javascript queries and still this is happening, what else can be doing wrong?

Are they named like 20-11-2025.md? yes they are, should i change this? I ran your query and this output is coming

**FOUND IT!** 

Your daily notes are named `20-11-2025` (DD-MM-YYYY), but Dataview is interpreting the dates **completely wrong**:

Look at this mess:
- `20-11-2025` → Dataview thinks it's `2025-11-20` ✅ (correct by accident)
- `25-12-25` → Dataview thinks it's `2025-12-25` ✅ (correct)
- But the **file.day is parsing incorrectly** because your filename format is ambiguous

---

## The Problem

Dataview needs dates in **ISO format: YYYY-MM-DD** to work reliably.

Your current format `DD-MM-YYYY` is causing date parsing chaos.

---

## Solution: Two Options

### Option 1: Rename Your Files (Recommended)

Change your daily note naming format from:
- ❌ `20-11-2025` (DD-MM-YYYY)
- ✅ `2025-11-20` (YYYY-MM-DD)

**To do this in Obsidian:**
1. Settings → Daily Notes → Date format: `YYYY-MM-DD`
2. For existing files, you'll need to rename them manually or use a bulk rename tool

---

### Option 2: Add `date:` to Frontmatter (Easier Short-term Fix)

Keep your filenames as-is, but **ensure every daily note has this at the top**:

```markdown
---
date: 2025-11-20
tags: daily
---

# {{date:MMMM DD, YYYY}}
...
```

The `date:` in frontmatter **overrides** Dataview's filename parsing.

---

## Updated Templater Daily Note Template

Use this to auto-generate the correct frontmatter:

```markdown
---
date: <% tp.date.now("YYYY-MM-DD") %>
tags: daily
---

# <% tp.date.now("MMMM DD, YYYY") %>

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

---

## Quick Test: Add Frontmatter to One Note

Pick `25-12-2025` (today) and add this at the very top:

```markdown
---
date: 2025-12-25
tags: daily
---
```

Then re-run the weekly dashboard query. If it **suddenly shows 20 tasks and checkmarks**, you've confirmed the issue.

---

## Updated Weekly Dashboard (Using Frontmatter Dates)

```markdown
---
date: 2025-12-28
week: 2025-W52
tags: weekly
---

# Week 2025-W52

## Weekly Overview

```dataview
TABLE WITHOUT ID
  file.link as "Date",
  length(file.tasks) as "Total",
  length(filter(file.tasks, (t) => t.completed)) as "Done",
  round((length(filter(file.tasks, (t) => t.completed)) / length(file.tasks)) * 100) + "%" as "Progress"
FROM "2. Daily Reflection"
WHERE date >= date(2025-12-22) AND date <= date(2025-12-28)
SORT date ASC
```

## Weekly Habit Grid

```dataviewjs
const folder = "2. Daily Reflection";
const startDate = dv.date("2025-12-22");
const endDate = dv.date("2025-12-28");

// Get pages using frontmatter date field
const pages = dv.pages(`"${folder}"`)
    .where(p => p.date && p.date >= startDate && p.date <= endDate)
    .sort(p => p.date, 'asc');

const habits = [
    "Exercise", "Read", "Drink water", "Meditate", "Journal",
    "Sleep", "Healthy meals", "No phone", "Deep work", "Social connection",
    "Tidy space", "Learn something", "Creative work", "Strength training",
    "Walk outside", "Review goals", "No social media", "No junk food",
    "Call family", "Brain training"
];

const icons = ["🏃", "📚", "💧", "🧘", "📝", "🛏️", "🥗", "📱", "🎯", "👥", 
               "🧹", "📖", "🎨", "💪", "🚶", "📊", "💻", "🍎", "📞", "🧠"];

const headers = ["Date", ...icons];
const rows = pages.map(p => {
    const checks = habits.map(habit => {
        const task = p.file.tasks.find(t => t.text.includes(habit));
        return task && task.completed ? "✅" : "❌";
    });
    return [p.file.link, ...checks];
});

if (rows.length === 0) {
    dv.paragraph("❌ No daily notes found for this week!");
    dv.paragraph(`Looking for dates between ${startDate} and ${endDate}`);
} else {
    dv.table(headers, rows);
}
```
```

**Key change:** Now using `p.date` (frontmatter) instead of `p.file.day` (filename parsing).

---

## Do This Now

1. **Add `date:` frontmatter to your existing daily notes** (or at least this week's notes)
2. **Update your daily note template** to auto-generate the frontmatter
3. **Update the weekly dashboard** to use `p.date` instead of `p.file.day`

Try that and let me know if you get green checkmarks! 🎯

<img width="1568" height="571" alt="image" src="https://github.com/user-attachments/assets/333266da-6151-41fe-b793-8a78ea6aaf2d" />
okay so we need to fix this only today is coming correctly, atleast today is coming correct

Progress! 60% completion on 25-12-2025 is showing correctly. Now let's fix the rest of the week.

---

## Issue: Only One Day Has Frontmatter

The debug output showed:
- `25-12-2025`: Has `date:` frontmatter → Works ✅
- `25-12-25`: **No frontmatter** → Fails ❌

You need to add the `date:` frontmatter to **all your daily notes** for the week.

---

## Quick Fix: Bulk Add Frontmatter to This Week's Notes

Open each of these files and add the frontmatter:

**22-11-2025** (add at top):
```markdown
---
date: 2025-11-22
tags: daily
---
```

**23-11-2025**:
```markdown
---
date: 2025-11-23
tags: daily
---
```

**24-11-2025**:
```markdown
---
date: 2025-11-24
tags: daily
---
```

**25-11-2025**:
```markdown
---
date: 2025-11-25
tags: daily
---
```

**26-11-2025**:
```markdown
---
date: 2025-11-26
tags: daily
---
```

**27-11-2025**:
```markdown
---
date: 2025-11-27
tags: daily
---
```

**28-11-2025**:
```markdown
---
date: 2025-11-28
tags: daily
---
```

---

## Updated Weekly Dashboard (Correct Date Range)

Your current dashboard is looking at **December 22-28**, but your notes are from **November**. Fix the date range:

```markdown
---
date: 2025-11-28
week: 2025-W48
tags: weekly
---

# Week 2025-W48

## Weekly Overview

```dataview
TABLE WITHOUT ID
  file.link as "Date",
  length(file.tasks) as "Total",
  length(filter(file.tasks, (t) => t.completed)) as "Done",
  round((length(filter(file.tasks, (t) => t.completed)) / length(file.tasks)) * 100) + "%" as "Progress"
FROM "2. Daily Reflection"
WHERE date >= date(2025-11-22) AND date <= date(2025-11-28)
SORT date ASC
```

## Weekly Habit Grid

```dataviewjs
const folder = "2. Daily Reflection";
const startDate = dv.date("2025-11-22");
const endDate = dv.date("2025-11-28");

const pages = dv.pages(`"${folder}"`)
    .where(p => p.date && p.date >= startDate && p.date <= endDate)
    .sort(p => p.date, 'asc');

const habits = [
    "Exercise", "Read", "Drink water", "Meditate", "Journal",
    "Sleep", "Healthy meals", "No phone", "Deep work", "Social connection",
    "Tidy space", "Learn something", "Creative work", "Strength training",
    "Walk outside", "Review goals", "No social media", "No junk food",
    "Call family", "Brain training"
];

const icons = ["🏃", "📚", "💧", "🧘", "📝", "🛏️", "🥗", "📱", "🎯", "👥", 
               "🧹", "📖", "🎨", "💪", "🚶", "📊", "💻", "🍎", "📞", "🧠"];

const headers = ["Date", ...icons];
const rows = pages.map(p => {
    const checks = habits.map(habit => {
        const task = p.file.tasks.find(t => t.text.includes(habit));
        return task && task.completed ? "✅" : "❌";
    });
    return [p.file.link, ...checks];
});

if (rows.length === 0) {
    dv.paragraph("❌ No daily notes found for this week!");
} else {
    dv.table(headers, rows);
}
```
```

---

## Automation: Fix Templater for Future Notes

Update your **Daily Note Template** so new notes auto-generate correct frontmatter:

```markdown
---
date: <% tp.file.creation_date("YYYY-MM-DD") %>
tags: daily
---

# <% tp.file.creation_date("MMMM DD, YYYY") %>

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

---

## Action Plan

1. **Add frontmatter to all November notes** (22-28)
2. **Update the weekly dashboard date range** to `2025-11-22` through `2025-11-28`
3. **Refresh the dashboard** (close and reopen the note)

You should then see all 7 days with proper checkmarks. Let me know when you've added the frontmatter and I'll help debug if anything's still broken!

<img width="1568" height="760" alt="image" src="https://github.com/user-attachments/assets/1f5ec51d-7e86-4011-bded-d0247e648d7e" />
my goat, you are the fucking best, listen unc. I want you to help me figure out two things, when i am creating a weekly dashboard file , it can not be in the dashboard right? it is coming here i need you to help me change that, and in the total right I need you to help me do two things, instead of a box with total, done and progress i want a area chart with gradient shading which plots the Tasks done and a donut chart for progress. (The progress has to be the net average of the progress percentage yeah?)

**LET'S FUCKING GO!** 🎯 You're crushing it. Now let's make this dashboard *chef's kiss*.

---

## Issue 1: Weekly Dashboard Appearing in Query

**Problem:** The "Weekly Dashboard" file itself shows up in the table (row 7 with 0 tasks).

**Fix:** Exclude dashboard files from the query.

---

## Issue 2: Replace Table with Charts

You want:
1. **Area chart** (gradient) → Tasks completed over the week
2. **Donut chart** → Average weekly progress percentage

---

## Updated Weekly Dashboard Code

```markdown
---
date: 2025-11-28
week: 2025-W48
tags: weekly
exclude-from-reports: true
---

# Week 2025-W48

## Weekly Overview

```dataviewjs
const folder = "2. Daily Reflection";
const startDate = dv.date("2025-11-22");
const endDate = dv.date("2025-11-28");

// Get daily notes (exclude dashboard files)
const pages = dv.pages(`"${folder}"`)
    .where(p => 
        p.date && 
        p.date >= startDate && 
        p.date <= endDate &&
        !p.file.name.includes("Weekly Dashboard") &&
        !p.file.name.includes("Monthly Dashboard")
    )
    .sort(p => p.date, 'asc');

// Calculate stats
const dailyStats = pages.map(p => {
    const total = p.file.tasks.length;
    const done = p.file.tasks.filter(t => t.completed).length;
    const progress = total > 0 ? Math.round((done / total) * 100) : 0;
    return {
        date: p.date.toFormat("dd-MM"),
        done: done,
        total: total,
        progress: progress
    };
});

// Calculate weekly average
const avgProgress = dailyStats.length > 0 
    ? Math.round(dailyStats.reduce((sum, d) => sum + d.progress, 0) / dailyStats.length)
    : 0;

const totalDone = dailyStats.reduce((sum, d) => sum + d.done, 0);
const totalTasks = dailyStats.reduce((sum, d) => sum + d.total, 0);

// Display summary cards
dv.header(3, "📊 Week Summary");
dv.paragraph(`
**Total Habits Completed:** ${totalDone} / ${totalTasks}  
**Average Daily Progress:** ${avgProgress}%  
**Best Day:** ${dailyStats.reduce((best, d) => d.progress > best.progress ? d : best, {progress: 0}).date || 'N/A'} (${Math.max(...dailyStats.map(d => d.progress))}%)
`);

// Area Chart - Tasks Completed
dv.header(3, "📈 Daily Tasks Completed");
const chartData = dailyStats.map(d => `${d.date}: ${d.done}`).join(', ');
dv.paragraph(`\`\`\`chart
type: line
labels: [${dailyStats.map(d => `"${d.date}"`).join(', ')}]
series:
  - title: Tasks Done
    data: [${dailyStats.map(d => d.done).join(', ')}]
tension: 0.4
width: 100%
labelColors: true
fill: true
beginAtZero: true
\`\`\``);

// Progress Donut Chart
dv.header(3, "🎯 Average Weekly Progress");
dv.paragraph(`\`\`\`chart
type: doughnut
labels: ["Completed", "Remaining"]
series:
  - title: Progress
    data: [${avgProgress}, ${100 - avgProgress}]
width: 50%
labelColors: true
\`\`\``);
```

## Weekly Habit Grid

```dataviewjs
const folder = "2. Daily Reflection";
const startDate = dv.date("2025-11-22");
const endDate = dv.date("2025-11-28");

const pages = dv.pages(`"${folder}"`)
    .where(p => 
        p.date && 
        p.date >= startDate && 
        p.date <= endDate &&
        !p.file.name.includes("Dashboard")
    )
    .sort(p => p.date, 'asc');

const habits = [
    "Exercise", "Read", "Drink water", "Meditate", "Journal",
    "Sleep", "Healthy meals", "No phone", "Deep work", "Social connection",
    "Tidy space", "Learn something", "Creative work", "Strength training",
    "Walk outside", "Review goals", "No social media", "No junk food",
    "Call family", "Brain training"
];

const icons = ["🏃", "📚", "💧", "🧘", "📝", "🛏️", "🥗", "📱", "🎯", "👥", 
               "🧹", "📖", "🎨", "💪", "🚶", "📊", "💻", "🍎", "📞", "🧠"];

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

---

## But Wait... Charts Plugin Needed!

Obsidian's Dataview **doesn't render charts natively**. You need the **Obsidian Charts** plugin.

### Install Charts Plugin:
1. Settings → Community Plugins
2. Browse → Search "**Obsidian Charts**"
3. Install & Enable

---

## Alternative: Use Canvas API (No Plugin)

If you don't want to install Charts, use **HTML + Chart.js** directly:

```markdown
---
date: 2025-11-28
week: 2025-W48
tags: weekly
---

# Week 2025-W48

## Weekly Overview

```dataviewjs
const folder = "2. Daily Reflection";
const startDate = dv.date("2025-11-22");
const endDate = dv.date("2025-11-28");

const pages = dv.pages(`"${folder}"`)
    .where(p => 
        p.date && 
        p.date >= startDate && 
        p.date <= endDate &&
        !p.file.name.includes("Dashboard")
    )
    .sort(p => p.date, 'asc');

const dailyStats = pages.map(p => {
    const total = p.file.tasks.length;
    const done = p.file.tasks.filter(t => t.completed).length;
    const progress = total > 0 ? Math.round((done / total) * 100) : 0;
    return {
        date: p.date.toFormat("MMM dd"),
        done: done,
        progress: progress
    };
});

const avgProgress = dailyStats.length > 0 
    ? Math.round(dailyStats.reduce((sum, d) => sum + d.progress, 0) / dailyStats.length)
    : 0;

// Summary stats
dv.header(3, "📊 Week Summary");
dv.paragraph(`**Average Progress:** ${avgProgress}% | **Best Day:** ${Math.max(...dailyStats.map(d => d.progress))}%`);

// Area Chart HTML
const chartHtml = `
<div style="width: 100%; height: 300px;">
    <canvas id="weeklyChart"></canvas>
</div>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script>
const ctx = document.getElementById('weeklyChart');
new Chart(ctx, {
    type: 'line',
    data: {
        labels: ${JSON.stringify(dailyStats.map(d => d.date))},
        datasets: [{
            label: 'Tasks Completed',
            data: ${JSON.stringify(dailyStats.map(d => d.done))},
            fill: true,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            tension: 0.4
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: { beginAtZero: true }
        }
    }
});
</script>
`;

dv.paragraph(chartHtml);

// Donut Chart
const donutHtml = `
<div style="width: 300px; height: 300px; margin: 0 auto;">
    <canvas id="progressDonut"></canvas>
</div>
<script>
const ctx2 = document.getElementById('progressDonut');
new Chart(ctx2, {
    type: 'doughnut',
    data: {
        labels: ['Completed', 'Remaining'],
        datasets: [{
            data: [${avgProgress}, ${100 - avgProgress}],
            backgroundColor: ['#4ade80', '#374151']
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false
    }
});
</script>
`;

dv.paragraph(donutHtml);
```
```

---

## File Organization Fix

**Move Weekly Dashboards to separate folder:**

Create folder structure:
```
2. Daily Reflection/
├── 2025/
│   ├── November 2025/
│   │   ├── 20-11-2025.md
│   │   ├── 21-11-2025.md
│   │   └── ...
│   └── December 2025/
└── Dashboards/
    ├── Weekly/
    │   └── Week 2025-W48.md
    └── Monthly/
        └── November 2025.md
```

Then update query to:
```javascript
const folder = "2. Daily Reflection/2025";
```

---

## Which Route You Taking?

**Option A:** Install Obsidian Charts plugin (cleanest)  
**Option B:** Use Chart.js via HTML (no plugin needed)  
**Option C:** Stick with table but add summary stats

Let me know which way you wanna go and I'll polish it up! 

why is this error 

```
Evaluation Error: TypeError: dailyStats.reduce is not a function
    at eval (eval at <anonymous> (plugin:dataview), <anonymous>:31:29)
    at DataviewInlineApi.eval (plugin:dataview:19027:16)
    at evalInContext (plugin:dataview:19028:7)
    at asyncEvalInContext (plugin:dataview:19038:32)
    at DataviewJSRenderer.render (plugin:dataview:19064:19)
    at DataviewJSRenderer.onload (plugin:dataview:18606:14)
    at e.load (app://obsidian.md/app.js:1:689289)
    at DataviewApi.executeJs (plugin:dataview:19607:18)
    at DataviewPlugin.dataviewjs (plugin:dataview:20537:18)
    at eval (plugin:dataview:20415:124)
```

The error means `dailyStats` isn't an array when you're trying to call `.reduce()` on it. This happens when the query returns no results or the data structure is wrong.

**Quick fix:** Add safety checks before using `.reduce()`.

---

## Fixed Code with Error Handling

```markdown
---
date: 2025-11-28
week: 2025-W48
tags: weekly
---

# Week 2025-W48

## Weekly Overview

```dataviewjs
const folder = "2. Daily Reflection";
const startDate = dv.date("2025-11-22");
const endDate = dv.date("2025-11-28");

// Get daily notes (exclude dashboard files)
const pages = dv.pages(`"${folder}"`)
    .where(p => 
        p.date && 
        p.date >= startDate && 
        p.date <= endDate &&
        !p.file.name.includes("Dashboard")
    )
    .sort(p => p.date, 'asc');

// Convert to array and calculate stats
const dailyStats = pages.array().map(p => {
    const total = p.file.tasks.length;
    const done = p.file.tasks.filter(t => t.completed).length;
    const progress = total > 0 ? Math.round((done / total) * 100) : 0;
    return {
        date: p.date.toFormat("dd-MM"),
        done: done,
        total: total,
        progress: progress
    };
});

// Safety check
if (dailyStats.length === 0) {
    dv.paragraph("❌ No daily notes found for this week!");
} else {
    // Calculate weekly average
    const avgProgress = Math.round(
        dailyStats.reduce((sum, d) => sum + d.progress, 0) / dailyStats.length
    );
    
    const totalDone = dailyStats.reduce((sum, d) => sum + d.done, 0);
    const totalTasks = dailyStats.reduce((sum, d) => sum + d.total, 0);
    
    const bestDay = dailyStats.reduce((best, d) => 
        d.progress > best.progress ? d : best, 
        {date: 'N/A', progress: 0}
    );

    // Display summary
    dv.header(3, "📊 Week Summary");
    dv.paragraph(`
**Total Habits Completed:** ${totalDone} / ${totalTasks}  
**Average Daily Progress:** ${avgProgress}%  
**Best Day:** ${bestDay.date} (${bestDay.progress}%)
    `);

    // Area Chart
    dv.header(3, "📈 Daily Tasks Completed");
    const chartHtml = `
<div style="width: 100%; height: 300px; margin: 20px 0;">
    <canvas id="weeklyChart"></canvas>
</div>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script>
const ctx = document.getElementById('weeklyChart');
if (ctx && !ctx.chart) {
    ctx.chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ${JSON.stringify(dailyStats.map(d => d.date))},
            datasets: [{
                label: 'Tasks Completed',
                data: ${JSON.stringify(dailyStats.map(d => d.done))},
                fill: true,
                backgroundColor: 'rgba(34, 197, 94, 0.2)',
                borderColor: 'rgba(34, 197, 94, 1)',
                borderWidth: 2,
                tension: 0.4,
                pointRadius: 4,
                pointBackgroundColor: 'rgba(34, 197, 94, 1)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { 
                    beginAtZero: true,
                    ticks: { stepSize: 5 }
                }
            }
        }
    });
}
</script>
    `;
    dv.paragraph(chartHtml);

    // Donut Chart
    dv.header(3, "🎯 Average Weekly Progress");
    const donutHtml = `
<div style="width: 300px; height: 300px; margin: 20px auto;">
    <canvas id="progressDonut"></canvas>
</div>
<script>
const ctx2 = document.getElementById('progressDonut');
if (ctx2 && !ctx2.chart) {
    ctx2.chart = new Chart(ctx2, {
        type: 'doughnut',
        data: {
            labels: ['Completed', 'Remaining'],
            datasets: [{
                data: [${avgProgress}, ${100 - avgProgress}],
                backgroundColor: [
                    'rgba(34, 197, 94, 0.8)',
                    'rgba(55, 65, 81, 0.3)'
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}
</script>
    `;
    dv.paragraph(donutHtml);
}
```

## Weekly Habit Grid

```dataviewjs
const folder = "2. Daily Reflection";
const startDate = dv.date("2025-11-22");
const endDate = dv.date("2025-11-28");

const pages = dv.pages(`"${folder}"`)
    .where(p => 
        p.date && 
        p.date >= startDate && 
        p.date <= endDate &&
        !p.file.name.includes("Dashboard")
    )
    .sort(p => p.date, 'asc');

const habits = [
    "Exercise", "Read", "Drink water", "Meditate", "Journal",
    "Sleep", "Healthy meals", "No phone", "Deep work", "Social connection",
    "Tidy space", "Learn something", "Creative work", "Strength training",
    "Walk outside", "Review goals", "No social media", "No junk food",
    "Call family", "Brain training"
];

const icons = ["🏃", "📚", "💧", "🧘", "📝", "🛏️", "🥗", "📱", "🎯", "👥", 
               "🧹", "📖", "🎨", "💪", "🚶", "📊", "💻", "🍎", "📞", "🧠"];

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

---

## Key Changes

1. **Added `.array()`** → Converts Dataview result to actual JavaScript array
2. **Added safety check** → Won't crash if no notes found
3. **Added `ctx.chart` check** → Prevents duplicate chart renders
4. **Better gradient colors** → Green gradient for completed tasks

---

## If Still Broken, Debug It

Add this at the top of your DataviewJS block to see what's wrong:

```javascript
dv.paragraph(`Debug: Found ${pages.length} pages`);
dv.paragraph(`Pages type: ${typeof pages}`);
dv.paragraph(`Is array? ${Array.isArray(pages)}`);
```

Paste the output and I'll fix it. Should work now though! 🎯

<img width="1372" height="883" alt="image" src="https://github.com/user-attachments/assets/1e607fa5-1dc4-478d-addc-226d705ed6db" />

bro what is going on? you need to lock in and fix this shit

My bad, the charts aren't rendering. Let me fix this properly.

**Issue:** Chart.js isn't loading correctly in Obsidian's environment. We need a different approach.

---

## Option 1: Use Obsidian Charts Plugin (EASIEST FIX)

Install this plugin and charts will work instantly:

1. Settings → Community Plugins → Browse
2. Search "**Obsidian Charts**" 
3. Install & Enable

Then use this code:

```markdown
---
date: 2025-11-28
week: 2025-W48
tags: weekly
---

# Week 2025-W48

## Weekly Overview

```dataviewjs
const folder = "2. Daily Reflection";
const startDate = dv.date("2025-11-22");
const endDate = dv.date("2025-11-28");

const pages = dv.pages(`"${folder}"`)
    .where(p => 
        p.date && 
        p.date >= startDate && 
        p.date <= endDate &&
        !p.file.name.includes("Dashboard")
    )
    .sort(p => p.date, 'asc');

const dailyStats = pages.array().map(p => {
    const total = p.file.tasks.length;
    const done = p.file.tasks.filter(t => t.completed).length;
    const progress = total > 0 ? Math.round((done / total) * 100) : 0;
    return {
        date: p.date.toFormat("dd-MM"),
        done: done,
        total: total,
        progress: progress
    };
});

if (dailyStats.length === 0) {
    dv.paragraph("❌ No daily notes found!");
} else {
    const avgProgress = Math.round(
        dailyStats.reduce((sum, d) => sum + d.progress, 0) / dailyStats.length
    );
    const totalDone = dailyStats.reduce((sum, d) => sum + d.done, 0);
    const totalTasks = dailyStats.reduce((sum, d) => sum + d.total, 0);
    const bestDay = dailyStats.reduce((best, d) => 
        d.progress > best.progress ? d : best
    );

    dv.paragraph(`**Total Habits Completed:** ${totalDone} / ${totalTasks}`);
    dv.paragraph(`**Average Daily Progress:** ${avgProgress}%`);
    dv.paragraph(`**Best Day:** ${bestDay.date} (${bestDay.progress}%)`);
}
```

### 📈 Daily Tasks Completed

```chart
type: line
labels: [22-11, 23-11, 24-11, 25-11, 26-11, 27-11, 29-11]
series:
  - title: Tasks Done
    data: [7, 20, 8, 4, 7, 6, 7]
tension: 0.4
width: 100%
labelColors: false
fill: true
fillColor: rgba(34, 197, 94, 0.2)
borderColor: rgba(34, 197, 94, 1)
```

### 🎯 Average Weekly Progress (42%)

```chart
type: doughnut
labels: [Completed, Remaining]
series:
  - title: Progress
    data: [42, 58]
width: 50%
labelColors: true
```

## Weekly Habit Grid

```dataviewjs
const folder = "2. Daily Reflection";
const startDate = dv.date("2025-11-22");
const endDate = dv.date("2025-11-28");

const pages = dv.pages(`"${folder}"`)
    .where(p => 
        p.date && 
        p.date >= startDate && 
        p.date <= endDate &&
        !p.file.name.includes("Dashboard")
    )
    .sort(p => p.date, 'asc');

const habits = [
    "Exercise", "Read", "Drink water", "Meditate", "Journal",
    "Sleep", "Healthy meals", "No phone", "Deep work", "Social connection",
    "Tidy space", "Learn something", "Creative work", "Strength training",
    "Walk outside", "Review goals", "No social media", "No junk food",
    "Call family", "Brain training"
];

const icons = ["🏃", "📚", "💧", "🧘", "📝", "🛏️", "🥗", "📱", "🎯", "👥", 
               "🧹", "📖", "🎨", "💪", "🚶", "📊", "💻", "🍎", "📞", "🧠"];

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

---

## Option 2: Dynamic Charts WITHOUT Plugin

If you refuse to install the plugin, use this **self-contained version** with inline Chart.js:

```markdown
---
date: 2025-11-28
week: 2025-W48
tags: weekly
---

# Week 2025-W48

## Weekly Overview

```dataviewjs
const folder = "2. Daily Reflection";
const startDate = dv.date("2025-11-22");
const endDate = dv.date("2025-11-28");

const pages = dv.pages(`"${folder}"`)
    .where(p => 
        p.date && 
        p.date >= startDate && 
        p.date <= endDate &&
        !p.file.name.includes("Dashboard")
    )
    .sort(p => p.date, 'asc');

const dailyStats = pages.array().map(p => {
    const total = p.file.tasks.length;
    const done = p.file.tasks.filter(t => t.completed).length;
    const progress = total > 0 ? Math.round((done / total) * 100) : 0;
    return {
        date: p.date.toFormat("dd-MM"),
        done: done,
        total: total,
        progress: progress
    };
});

if (dailyStats.length === 0) {
    dv.paragraph("❌ No daily notes found!");
} else {
    const avgProgress = Math.round(
        dailyStats.reduce((sum, d) => sum + d.progress, 0) / dailyStats.length
    );
    const totalDone = dailyStats.reduce((sum, d) => sum + d.done, 0);
    const totalTasks = dailyStats.reduce((sum, d) => sum + d.total, 0);
    const bestDay = dailyStats.reduce((best, d) => 
        d.progress > best.progress ? d : best
    );

    dv.paragraph(`**Total Habits Completed:** ${totalDone} / ${totalTasks}`);
    dv.paragraph(`**Average Daily Progress:** ${avgProgress}%`);
    dv.paragraph(`**Best Day:** ${bestDay.date} (${bestDay.progress}%)`);

    // Area Chart
    const chartId = 'chart-' + Math.random().toString(36).substr(2, 9);
    const donutId = 'donut-' + Math.random().toString(36).substr(2, 9);
    
    const container = dv.el('div', '', {
        attr: {
            style: 'width: 100%; margin: 20px 0;'
        }
    });
    
    container.innerHTML = `
        <h3>📈 Daily Tasks Completed</h3>
        <div style="width: 100%; height: 250px; margin-bottom: 30px;">
            <canvas id="${chartId}"></canvas>
        </div>
        <h3>🎯 Average Weekly Progress</h3>
        <div style="width: 300px; height: 300px; margin: 0 auto;">
            <canvas id="${donutId}"></canvas>
        </div>
    `;
    
    // Load Chart.js if not already loaded
    if (!window.Chart) {
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js';
        script.onload = () => createCharts();
        document.head.appendChild(script);
    } else {
        createCharts();
    }
    
    function createCharts() {
        const ctx1 = document.getElementById(chartId);
        const ctx2 = document.getElementById(donutId);
        
        if (ctx1) {
            new Chart(ctx1, {
                type: 'line',
                data: {
                    labels: ${JSON.stringify(dailyStats.map(d => d.date))},
                    datasets: [{
                        label: 'Tasks Completed',
                        data: ${JSON.stringify(dailyStats.map(d => d.done))},
                        fill: true,
                        backgroundColor: 'rgba(34, 197, 94, 0.2)',
                        borderColor: 'rgba(34, 197, 94, 1)',
                        borderWidth: 2,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: { y: { beginAtZero: true } }
                }
            });
        }
        
        if (ctx2) {
            new Chart(ctx2, {
                type: 'doughnut',
                data: {
                    labels: ['Completed', 'Remaining'],
                    datasets: [{
                        data: [${avgProgress}, ${100 - avgProgress}],
                        backgroundColor: ['rgba(34, 197, 94, 0.8)', 'rgba(55, 65, 81, 0.3)']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        }
    }
}
```

```

---

## My Recommendation

**Just install the Obsidian Charts plugin.** Takes 30 seconds and works perfectly with Dataview. The manual Chart.js approach is hacky and might break.

Which option you going with?



The error `SyntaxError: Unexpected token '{'` occurs because you are using template string syntax (`${...}`) inside standard JavaScript code.

Template syntax is only required when building a text string (like HTML). When defining the `Chart.js` configuration objects, you are writing actual JavaScript, so you should pass the variables and arrays directly.

Additionally, `pages.array()` is not a valid Dataview function; it should simply be mapped or converted using `.values`.

Here is the fixed code for your **Weekly Overview** block.

### Weekly Overview
```dataviewjs
const folder = "2. Daily Reflection";
const startDate = dv.date("2025-11-22");
const endDate = dv.date("2025-11-28");

// 1. Fetch pages
const pages = dv.pages(`"${folder}"`)
    .where(p => 
        p.date && 
        p.date >= startDate && 
        p.date <= endDate &&
        !p.file.name.includes("Dashboard")
    )
    .sort(p => p.date, 'asc');

// 2. Calculate Stats
// We use .values to ensure dailyStats is a standard JS Array, not a Dataview DataArray
const dailyStats = pages.map(p => {
    const total = p.file.tasks.length;
    const done = p.file.tasks.filter(t => t.completed).length;
    const progress = total > 0 ? Math.round((done / total) * 100) : 0;
    return {
        date: p.date.toFormat("dd-MM"),
        done: done,
        total: total,
        progress: progress
    };
}).values;

if (dailyStats.length === 0) {
    dv.paragraph("❌ No daily notes found!");
} else {
    // Calculate aggregates
    const avgProgress = Math.round(
        dailyStats.reduce((sum, d) => sum + d.progress, 0) / dailyStats.length
    );
    const totalDone = dailyStats.reduce((sum, d) => sum + d.done, 0);
    const totalTasks = dailyStats.reduce((sum, d) => sum + d.total, 0);
    const bestDay = dailyStats.reduce((best, d) => 
        d.progress > best.progress ? d : best
    );

    // Render Text Stats
    dv.paragraph(`**Total Habits Completed:** ${totalDone} / ${totalTasks}`);
    dv.paragraph(`**Average Daily Progress:** ${avgProgress}%`);
    dv.paragraph(`**Best Day:** ${bestDay.date} (${bestDay.progress}%)`);

    // Generate unique IDs for charts
    const chartId = 'chart-' + Math.random().toString(36).substr(2, 9);
    const donutId = 'donut-' + Math.random().toString(36).substr(2, 9);
    
    const container = dv.el('div', '', {
        attr: {
            style: 'width: 100%; margin: 20px 0;'
        }
    });
    
    // HTML Structure
    container.innerHTML = `
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&display=swap');
            
            .charts-container {
                display: grid;
                grid-template-columns: 1fr 400px;
                gap: 40px;
                align-items: center;
                font-family: 'Outfit', sans-serif;
            }
            
            .chart-wrapper {
                width: 100%;
                height: 300px;
            }
            
            .donut-wrapper {
                width: 100%;
                height: 300px;
                position: relative;
            }
            
            .donut-center-text {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                text-align: center;
                font-family: 'Outfit', sans-serif;
                pointer-events: none;
            }
            
            .donut-percentage {
                font-size: 48px;
                font-weight: 700;
                color: rgba(46, 140, 252, 1);
                line-height: 1;
            }
            
            .donut-label {
                font-size: 14px;
                font-weight: 500;
                color: rgba(156, 163, 175, 1);
                margin-top: 8px;
            }
            
            @media (max-width: 768px) {
                .charts-container {
                    grid-template-columns: 1fr;
                }
            }
        </style>
        
        <div class="charts-container">
            <div>
                <h3 style="font-family: 'Outfit', sans-serif; margin-bottom: 16px;">📈 Daily Tasks Completed</h3>
                <div class="chart-wrapper">
                    <canvas id="${chartId}"></canvas>
                </div>
            </div>
            
            <div>
                <h3 style="font-family: 'Outfit', sans-serif; margin-bottom: 16px;">🎯 Average Weekly Progress</h3>
                <div class="donut-wrapper">
                    <canvas id="${donutId}"></canvas>
                    <div class="donut-center-text">
                        <div class="donut-percentage">${avgProgress}%</div>
                        <div class="donut-label">Completed</div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Load Chart.js and render
    if (!window.Chart) {
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js';
        script.onload = () => createCharts();
        document.head.appendChild(script);
    } else {
        createCharts();
    }
    
    function createCharts() {
        const ctx1 = document.getElementById(chartId);
        const ctx2 = document.getElementById(donutId);
        
        if (ctx1) {
            new Chart(ctx1, {
                type: 'line',
                data: {
                    // FIX: Pass direct arrays, remove ${} and JSON.stringify
                    labels: dailyStats.map(d => d.date),
                    datasets: [{
                        label: 'Tasks Completed',
                        data: dailyStats.map(d => d.done),
                        fill: true,
                        backgroundColor: 'rgba(215, 224, 255, 0.8)',
                        borderColor: 'rgba(46, 140, 252, 1)',
                        borderWidth: 2,
                        tension: 0.4,
                        pointRadius: 4,
                        pointBackgroundColor: 'rgba(46, 140, 252, 1)',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointHoverRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { 
                        legend: { display: false }
                    },
                    scales: { 
                        y: { 
                            beginAtZero: true,
                            grid: { display: false },
                            ticks: { font: { family: 'Outfit', size: 12 } }
                        },
                        x: {
                            grid: { display: false },
                            ticks: { font: { family: 'Outfit', size: 12 } }
                        }
                    }
                }
            });
        }
        
        if (ctx2) {
            new Chart(ctx2, {
                type: 'doughnut',
                data: {
                    labels: ['Completed', 'Remaining'],
                    datasets: [{
                        // FIX: Pass direct variables, remove ${}
                        data: [avgProgress, 100 - avgProgress],
                        backgroundColor: [
                            'rgba(46, 140, 252, 0.8)',
                            'rgba(233, 243, 255, 0.8)'
                        ],
                        borderWidth: 0,
                        cutout: '75%'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: { enabled: false }
                    }
                }
            });
        }
    }
}
```

### Key Changes Made:
1.  **Removed `${}` inside Chart Config:** In your original code, you had `labels: ${JSON.stringify(...)}`. This is invalid syntax inside a standard JavaScript function. It has been changed to `labels: dailyStats.map(...)`.
2.  **Fixed `.array()` error:** Replaced `pages.array().map(...)` with `pages.map(...).values`. Dataview collections do not have an `.array()` method; adding `.values` at the end ensures the result is a standard JavaScript array that `Chart.js` can read.
3.  **Removed inner `JSON.stringify`:** Since we are now passing data directly to the Chart object within the Javascript execution context, we pass the arrays directly, not as stringified JSON.


just brilliant brilliant skills,
i want you to help me with few better features, the three narrative points you have mentioned on the top, i want you to make them into 3 different KPI Cards with its own icons yeah? 
and then the other three things can come as expected, 
I want it to be have these icons

<svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><title>CMake</title><path d="M11.769.066L.067 23.206l12.76-10.843zM23.207 23.934L7.471 17.587 0 23.934zM24 23.736L12.298.463l1.719 19.24zM12.893 12.959l-5.025 4.298 5.62 2.248z"/></svg> yellow color

<svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><title>Claris</title><path d="M11.56 0a3.34 3.34 0 00-.57.043L22.947 12 10.99 23.957c.132.022.307.043.57.043 6.626 0 12-5.375 12-12s-5.374-12-12-12zm-1.535 2.414C4.738 2.414.44 6.713.44 12s4.3 9.588 9.586 9.588c.264 0 .44-.023.57-.045L1.054 12l9.543-9.543a3.337 3.337 0 00-.57-.043zm.746 2.457c-.263 0-.438.021-.57.043L17.287 12l-7.086 7.086c.132.022.307.045.57.045 3.927 0 7.13-3.204 7.13-7.131s-3.203-7.129-7.13-7.129zm-.416 2.434A4.701 4.701 0 005.66 12a4.701 4.701 0 004.695 4.695c.264 0 .44-.023.57-.045L6.274 12l4.653-4.65a3.296 3.296 0 00-.57-.045Z"/></svg> yellow color

<svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><title>Clubhouse</title><path d="M24 9.543c0 .32-.23.763-.337.976-.39.833-1.03 2.112-1.03 3.585 0 3.213-1.135 4.811-2.023 5.628a5.706 5.706 0 0 1-3.852 1.527 6.144 6.144 0 0 1-3.32-.976c-1.366-.905-2.219-2.326-3.088-3.745-.692-1.153-1.171-2.06-1.918-3.816-.421-1.018-.813-2.012-1.15-3.094-.16-.514-.142-.905.053-1.153.195-.23.462-.337.78-.355.55-.018.764.373 1.083 1.384.195.639.586 1.563.816 2.077.302.621.728 1.455.923 1.74.16.25.302.32.461.32.284 0 .497-.16.497-.443 0-.16-.16-.426-.248-.586-.16-.302-.497-.905-.728-1.42a32.775 32.775 0 0 1-.763-1.917c-.142-.373-.301-.905-.461-1.437-.248-.816-.373-1.313-.373-1.687 0-.568.426-.94 1.065-.94.461 0 .763.23.958 1.064.16.763.444 2.006.852 2.982.266.639.656 1.492.887 1.918.142.248.301.461.301.55 0 .124-.23.32-.426.585-.124.16-.177.267-.177.39 0 .107.071.214.177.356.107.142.213.284.338.284.088 0 .142-.036.195-.107a6.12 6.12 0 0 1 1.847-1.563c.816-.461 1.651-.692 2.308-.834.319-.07.408-.142.408-.32 0-.212-.16-.336-.373-.354-.16-.018-.301 0-.55.018-.177.018-.266-.071-.372-.302-.32-.674-.94-1.811-1.313-3.266a13.95 13.95 0 0 1-.39-2.13c-.054-.391.017-.533.212-.71.249-.213.692-.302 1.03-.213.407.106.62.426.833 1.67.107.585.284 1.33.497 1.97.266.816.603 1.492 1.118 2.397.284.497.638 1.011 1.011 1.51-.071.213-.195.354-.603.692-.408.337-.816.692-1.189 1.348-.266.479-.39 1.011-.39 1.366 0 .337.07.408.284.408.372 0 .674-.07.692-.23.088-.64.195-1.047.55-1.528.212-.266.585-.603.887-.87.567-.46.763-.727.958-1.383.088-.302.195-.586.337-.852.337-.62.94-1.33 1.882-1.33.302 0 .55.088.71.337a.966.966 0 0 1 .124.479zM12.608 7.265c.16.658.355 1.226.55 1.723.23.605.497 1.12.87 1.811.177.337.265.337.691.107a9.14 9.14 0 0 1 1.207-.515c-.639-1.384-1.171-2.539-1.437-3.514a29.883 29.883 0 0 1-.39-1.918c-.054-.497-.107-.923-.231-1.384-.142-.568-.338-.834-.888-.834-.514 0-1.135.266-1.135.94 0 .444.124 1.1.248 1.631.213.516.249.835.515 1.953zm-7.484 7.147c-.43.116-2.276.784-2.721.957-.503.195-.857.372-.605 1.122.205.607.553.636.874.516.45-.166 2.442-1.21 2.818-1.442.34-.21.45-.37.29-.769-.145-.363-.354-.465-.656-.384zm-1.276-3.074c.252-.008.448-.09.508-.526.047-.335-.006-.51-.39-.629-.371-.114-2.702-.494-3.205-.542-.434-.042-.702 0-.753.687-.049.64.13.836.572.88.508.05 2.733.144 3.268.13zm-2.63-6.082c.474.283 2.293 1.385 2.906 1.579.306.096.468.01.64-.331s.218-.477-.111-.742c-.34-.274-2.123-1.661-2.628-1.924-.435-.226-.729-.139-.993.361-.299.566-.244.798.185 1.057z"/></svg> yellow color


can you accomodate this request for me?

Here is the updated DataviewJS code.

I have transformed the three text statistics into **KPI Cards** using the icons you provided. I applied a bright yellow (`#FFD60A`) to the icons to match your request, and styled them to fit cleanly above your charts.

```dataviewjs
const folder = "2. Daily Reflection";
const startDate = dv.date("2025-11-22");
const endDate = dv.date("2025-11-28");

// --- 1. DATA FETCHING ---
const pages = dv.pages(`"${folder}"`)
    .where(p => 
        p.date && 
        p.date >= startDate && 
        p.date <= endDate &&
        !p.file.name.includes("Dashboard")
    )
    .sort(p => p.date, 'asc');

const dailyStats = pages.map(p => {
    const total = p.file.tasks.length;
    const done = p.file.tasks.filter(t => t.completed).length;
    const progress = total > 0 ? Math.round((done / total) * 100) : 0;
    return {
        date: p.date.toFormat("dd-MM"),
        done: done,
        total: total,
        progress: progress
    };
}).values;

// --- 2. CALCULATE STATS ---
if (dailyStats.length === 0) {
    dv.paragraph("❌ No daily notes found!");
} else {
    const avgProgress = Math.round(
        dailyStats.reduce((sum, d) => sum + d.progress, 0) / dailyStats.length
    );
    const totalDone = dailyStats.reduce((sum, d) => sum + d.done, 0);
    const totalTasks = dailyStats.reduce((sum, d) => sum + d.total, 0);
    const bestDay = dailyStats.reduce((best, d) => 
        d.progress > best.progress ? d : best
    );

    // --- 3. ICONS (Yellow) ---
    const iconColor = "#FFD60A"; // Bright Yellow
    
    const iconCMake = `<svg viewBox="0 0 24 24" fill="${iconColor}" xmlns="http://www.w3.org/2000/svg" class="kpi-svg"><path d="M11.769.066L.067 23.206l12.76-10.843zM23.207 23.934L7.471 17.587 0 23.934zM24 23.736L12.298.463l1.719 19.24zM12.893 12.959l-5.025 4.298 5.62 2.248z"/></svg>`;
    
    const iconClaris = `<svg viewBox="0 0 24 24" fill="${iconColor}" xmlns="http://www.w3.org/2000/svg" class="kpi-svg"><path d="M11.56 0a3.34 3.34 0 00-.57.043L22.947 12 10.99 23.957c.132.022.307.043.57.043 6.626 0 12-5.375 12-12s-5.374-12-12-12zm-1.535 2.414C4.738 2.414.44 6.713.44 12s4.3 9.588 9.586 9.588c.264 0 .44-.023.57-.045L1.054 12l9.543-9.543a3.337 3.337 0 00-.57-.043zm.746 2.457c-.263 0-.438.021-.57.043L17.287 12l-7.086 7.086c.132.022.307.045.57.045 3.927 0 7.13-3.204 7.13-7.131s-3.203-7.129-7.13-7.129zm-.416 2.434A4.701 4.701 0 005.66 12a4.701 4.701 0 004.695 4.695c.264 0 .44-.023.57-.045L6.274 12l4.653-4.65a3.296 3.296 0 00-.57-.045Z"/></svg>`;
    
    const iconClubhouse = `<svg viewBox="0 0 24 24" fill="${iconColor}" xmlns="http://www.w3.org/2000/svg" class="kpi-svg"><path d="M24 9.543c0 .32-.23.763-.337.976-.39.833-1.03 2.112-1.03 3.585 0 3.213-1.135 4.811-2.023 5.628a5.706 5.706 0 0 1-3.852 1.527 6.144 6.144 0 0 1-3.32-.976c-1.366-.905-2.219-2.326-3.088-3.745-.692-1.153-1.171-2.06-1.918-3.816-.421-1.018-.813-2.012-1.15-3.094-.16-.514-.142-.905.053-1.153.195-.23.462-.337.78-.355.55-.018.764.373 1.083 1.384.195.639.586 1.563.816 2.077.302.621.728 1.455.923 1.74.16.25.302.32.461.32.284 0 .497-.16.497-.443 0-.16-.16-.426-.248-.586-.16-.302-.497-.905-.728-1.42a32.775 32.775 0 0 1-.763-1.917c-.142-.373-.301-.905-.461-1.437-.248-.816-.373-1.313-.373-1.687 0-.568.426-.94 1.065-.94.461 0 .763.23.958 1.064.16.763.444 2.006.852 2.982.266.639.656 1.492.887 1.918.142.248.301.461.301.55 0 .124-.23.32-.426.585-.124.16-.177.267-.177.39 0 .107.071.214.177.356.107.142.213.284.338.284.088 0 .142-.036.195-.107a6.12 6.12 0 0 1 1.847-1.563c.816-.461 1.651-.692 2.308-.834.319-.07.408-.142.408-.32 0-.212-.16-.336-.373-.354-.16-.018-.301 0-.55.018-.177.018-.266-.071-.372-.302-.32-.674-.94-1.811-1.313-3.266a13.95 13.95 0 0 1-.39-2.13c-.054-.391.017-.533.212-.71.249-.213.692-.302 1.03-.213.407.106.62.426.833 1.67.107.585.284 1.33.497 1.97.266.816.603 1.492 1.118 2.397.284.497.638 1.011 1.011 1.51-.071.213-.195.354-.603.692-.408.337-.816.692-1.189 1.348-.266.479-.39 1.011-.39 1.366 0 .337.07.408.284.408.372 0 .674-.07.692-.23.088-.64.195-1.047.55-1.528.212-.266.585-.603.887-.87.567-.46.763-.727.958-1.383.088-.302.195-.586.337-.852.337-.62.94-1.33 1.882-1.33.302 0 .55.088.71.337a.966.966 0 0 1 .124.479zM12.608 7.265c.16.658.355 1.226.55 1.723.23.605.497 1.12.87 1.811.177.337.265.337.691.107a9.14 9.14 0 0 1 1.207-.515c-.639-1.384-1.171-2.539-1.437-3.514a29.883 29.883 0 0 1-.39-1.918c-.054-.497-.107-.923-.231-1.384-.142-.568-.338-.834-.888-.834-.514 0-1.135.266-1.135.94 0 .444.124 1.1.248 1.631.213.516.249.835.515 1.953zm-7.484 7.147c-.43.116-2.276.784-2.721.957-.503.195-.857.372-.605 1.122.205.607.553.636.874.516.45-.166 2.442-1.21 2.818-1.442.34-.21.45-.37.29-.769-.145-.363-.354-.465-.656-.384zm-1.276-3.074c.252-.008.448-.09.508-.526.047-.335-.006-.51-.39-.629-.371-.114-2.702-.494-3.205-.542-.434-.042-.702 0-.753.687-.049.64.13.836.572.88.508.05 2.733.144 3.268.13zm-2.63-6.082c.474.283 2.293 1.385 2.906 1.579.306.096.468.01.64-.331s.218-.477-.111-.742c-.34-.274-2.123-1.661-2.628-1.924-.435-.226-.729-.139-.993.361-.299.566-.244.798.185 1.057z"/></svg>`;

    // --- 4. RENDER LAYOUT ---
    const chartId = 'chart-' + Math.random().toString(36).substr(2, 9);
    const donutId = 'donut-' + Math.random().toString(36).substr(2, 9);
    
    const container = dv.el('div', '', {
        attr: { style: 'width: 100%;' }
    });
    
    container.innerHTML = `
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&display=swap');
            
            /* KPI CARDS STYLING */
            .kpi-container {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 20px;
                margin-bottom: 40px;
                font-family: 'Outfit', sans-serif;
            }
            .kpi-card {
                background-color: var(--background-secondary);
                border: 1px solid var(--background-modifier-border);
                border-radius: 12px;
                padding: 20px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }
            .kpi-icon-wrapper {
                margin-bottom: 12px;
                width: 40px;
                height: 40px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .kpi-svg {
                width: 32px;
                height: 32px;
            }
            .kpi-value {
                font-size: 28px;
                font-weight: 700;
                color: var(--text-normal);
                line-height: 1.2;
                margin-bottom: 4px;
            }
            .kpi-sub {
                font-size: 14px;
                font-weight: 500;
                color: var(--text-muted);
            }
            
            /* CHART STYLING */
            .charts-container {
                display: grid;
                grid-template-columns: 1fr 400px;
                gap: 40px;
                align-items: center;
                font-family: 'Outfit', sans-serif;
            }
            .chart-wrapper { width: 100%; height: 300px; }
            .donut-wrapper { width: 100%; height: 300px; position: relative; }
            .donut-center-text {
                position: absolute;
                top: 50%; left: 50%;
                transform: translate(-50%, -50%);
                text-align: center;
                pointer-events: none;
            }
            .donut-percentage {
                font-size: 48px; font-weight: 700;
                color: rgba(46, 140, 252, 1); line-height: 1;
            }
            .donut-label {
                font-size: 14px; font-weight: 500;
                color: rgba(156, 163, 175, 1); margin-top: 8px;
            }
            
            @media (max-width: 768px) {
                .kpi-container { grid-template-columns: 1fr; }
                .charts-container { grid-template-columns: 1fr; }
            }
        </style>
        
        <!-- KPI SECTION -->
        <div class="kpi-container">
            <div class="kpi-card">
                <div class="kpi-icon-wrapper">${iconCMake}</div>
                <div class="kpi-value">${totalDone} / ${totalTasks}</div>
                <div class="kpi-sub">Total Habits Completed</div>
            </div>
            
            <div class="kpi-card">
                <div class="kpi-icon-wrapper">${iconClaris}</div>
                <div class="kpi-value">${avgProgress}%</div>
                <div class="kpi-sub">Average Daily Progress</div>
            </div>
            
            <div class="kpi-card">
                <div class="kpi-icon-wrapper">${iconClubhouse}</div>
                <div class="kpi-value">${bestDay.progress}%</div>
                <div class="kpi-sub">Best Day: ${bestDay.date}</div>
            </div>
        </div>

        <!-- CHARTS SECTION -->
        <div class="charts-container">
            <div>
                <h3 style="font-family: 'Outfit', sans-serif; margin-bottom: 16px;">📈 Daily Tasks Completed</h3>
                <div class="chart-wrapper">
                    <canvas id="${chartId}"></canvas>
                </div>
            </div>
            
            <div>
                <h3 style="font-family: 'Outfit', sans-serif; margin-bottom: 16px;">🎯 Average Weekly Progress</h3>
                <div class="donut-wrapper">
                    <canvas id="${donutId}"></canvas>
                    <div class="donut-center-text">
                        <div class="donut-percentage">${avgProgress}%</div>
                        <div class="donut-label">Completed</div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // --- 5. INITIALIZE CHARTS ---
    if (!window.Chart) {
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js';
        script.onload = () => createCharts();
        document.head.appendChild(script);
    } else {
        createCharts();
    }
    
    function createCharts() {
        const ctx1 = document.getElementById(chartId);
        const ctx2 = document.getElementById(donutId);
        
        if (ctx1) {
            new Chart(ctx1, {
                type: 'line',
                data: {
                    labels: dailyStats.map(d => d.date),
                    datasets: [{
                        label: 'Tasks Completed',
                        data: dailyStats.map(d => d.done),
                        fill: true,
                        backgroundColor: 'rgba(215, 224, 255, 0.8)',
                        borderColor: 'rgba(46, 140, 252, 1)',
                        borderWidth: 2,
                        tension: 0.4,
                        pointRadius: 4,
                        pointBackgroundColor: 'rgba(46, 140, 252, 1)',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointHoverRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: { 
                        y: { 
                            beginAtZero: true,
                            grid: { display: false },
                            ticks: { font: { family: 'Outfit', size: 12 } }
                        },
                        x: {
                            grid: { display: false },
                            ticks: { font: { family: 'Outfit', size: 12 } }
                        }
                    }
                }
            });
        }
        
        if (ctx2) {
            new Chart(ctx2, {
                type: 'doughnut',
                data: {
                    labels: ['Completed', 'Remaining'],
                    datasets: [{
                        data: [avgProgress, 100 - avgProgress],
                        backgroundColor: [
                            'rgba(46, 140, 252, 0.8)',
                            'rgba(233, 243, 255, 0.8)'
                        ],
                        borderWidth: 0,
                        cutout: '75%'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: { enabled: false }
                    }
                }
            });
        }
    }
}
```

<img width="1821" height="670" alt="image" src="https://github.com/user-attachments/assets/400c663d-715b-4370-a793-0a95f41e96d5" />

while the kpi cards are coming the graphs are not can you fix this, also add a formula for worst day and the icon for that will be <svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><title>CircuitVerse</title><path d="M12.1227 24c-.201 0-.4037-.0058-.6028-.0175a.487.487 0 0 1-.0433-.287.703.703 0 0 0-.0213-.2624H9.2251a1.205 1.205 0 0 1-.785.3898.7059.7059 0 0 1-.5075-.2282.9153.9153 0 0 1-.0647-1.099.7.7 0 0 1 .5576-.267 1.2192 1.2192 0 0 1 .703.267h2.3271a1.9635 1.9635 0 0 0 0-.614h-1.1959a1.1416 1.1416 0 0 1-.5495-.1293c-.442-.2654-.9147-.522-1.4868-.808a1.3834 1.3834 0 0 0-.711-.194 7.1018 7.1018 0 0 1-.4752.0142c-.157 0-.313-.0036-.4644-.007a18.8307 18.8307 0 0 0-.45-.0072 1.3491 1.3491 0 0 1-.8135.3704.6752.6752 0 0 1-.512-.2411.7596.7596 0 0 1 0-1.0666.7188.7188 0 0 1 .5363-.2718 1.3055 1.3055 0 0 1 .7566.3364H7.771a1.1403 1.1403 0 0 1 .5495.1293c.1413.0824.2938.1616.4415.2389a6.0441 6.0441 0 0 1 .7544.4399 1.9496 1.9496 0 0 0 1.116.3293 2.542 2.542 0 0 0 .1772-.006 1.5207 1.5207 0 0 1 .2191-.0143c.0682 0 .1361.0032.208.0068.0797.004.1615.0078.2516.0078v-1.0343h-1.1639a1.267 1.267 0 0 1-.711.2993.8404.8404 0 0 1-.614-.3316c-.3709-.4043-.1346-.8032.1291-1.0666a.5653.5653 0 0 1 .3533-.125 1.3475 1.3475 0 0 1 .8426.4479h1.099v-.905a.3807.3807 0 0 0-.1778-.0404c-.027 0-.054.0019-.0824.0039-.0285.0019-.0624.0042-.0954.0042H4.959a.8404.8404 0 0 1-.7434-.3556c-.1716-.2285-.3698-.4592-.545-.6629l-.069-.0804c-.7435-.0647-.9698-.2845-.9375-.905a.7495.7495 0 0 1 .8404-.6788c.4916 0 .711.329.711 1.0666.0608.0708.12.1429.1827.2195.1357.1651.2757.3361.4315.492h6.6582a5.5024 5.5024 0 0 0 0-1.0344H6.6397a1.3177 1.3177 0 0 1-.7948.3707.6623.6623 0 0 1-.498-.2414.7457.7457 0 0 1 0-1.099.6933.6933 0 0 1 .508-.2685 1.1678 1.1678 0 0 1 .7201.3652h4.8806v-1.002h-8.242c-.156.1736-.3232.3494-.5016.5356-.1584.1661-.3213.3368-.5007.531a.8381.8381 0 0 1-.7912.7515.8055.8055 0 0 1-.1138-.008.8459.8459 0 0 1-.6464-1.002c.0588-.3827.372-.6022.8597-.6022a1.9283 1.9283 0 0 1 .2715.0204c.1765-.2062.4435-.5084.7111-.7757a.9587.9587 0 0 1 .7757-.3233h8.1774v-1.0989H1.6295a1.226 1.226 0 0 1-.7434.3436.6817.6817 0 0 1-.5494-.3113.8488.8488 0 0 1 .097-1.1312.7486.7486 0 0 1 .4793-.194 1.1539 1.1539 0 0 1 .8138.4849h3.1998l-.1014-.097c-.5595-.5284-1.1378-1.0747-1.8382-1.713a.7554.7554 0 0 1-.7757-.808c0-.514.2195-.7435.711-.7435.6617 0 .8404.2127.8728 1.0343.2482.238.4922.469.7508.7134.5417.5126 1.101 1.0414 1.6733 1.6138h5.236v-.7434H9.1605a1.2783 1.2783 0 0 1-.7049.2628.7457.7457 0 0 1-.588-.2951.808.808 0 0 1 .1294-1.099.6351.6351 0 0 1 .4373-.167 1.2777 1.2777 0 0 1 .8235.3933h2.198v-.8404c-.2264 0-.4526-.0036-.671-.007h-.0066a39.3709 39.3709 0 0 0-.656-.0072c-.2484 0-.4675.0048-.6705.0142a1.3974 1.3974 0 0 1-.1144.0048 1.2311 1.2311 0 0 1-.8552-.3603l-.6006-.5068-.0116-.01-.0078-.0066A260.83 260.83 0 0 0 6.6397 7.272H3.052a1.235 1.235 0 0 1-.7192.2909.7298.7298 0 0 1-.5737-.2909.7757.7757 0 0 1 .097-1.099.701.701 0 0 1 .4742-.2233 1.3556 1.3556 0 0 1 .8187.45h3.1352a1.599 1.599 0 0 1 1.1635.4525c.3733.3513.7951.6907 1.203 1.0187h.0016c.19.1532.388.3113.573.4664h2.198V7.2707c-.138 0-.2822-.0035-.4202-.007H11a17.915 17.915 0 0 0-.4392-.0072c-.1616 0-.3032.0048-.4286.0142a1.4155 1.4155 0 0 1-.1157.0049 1.3365 1.3365 0 0 1-.8558-.3265 11.3707 11.3707 0 0 0-.3048-.2405c-.1025-.0788-.212-.1616-.3093-.2443-.8-.0646-1.099-.2909-1.0667-.808a.7757.7757 0 0 1 .7758-.7434c.497 0 .7757.3018.808.8726.1293.097.2586.2033.388.3061l.0015.002c.1267.103.2585.2097.3878.3064h1.5838V5.1394h-.5495a1.3507 1.3507 0 0 1-.7654.3604.6872.6872 0 0 1-.5275-.296.7983.7983 0 0 1 .0324-1.099.6978.6978 0 0 1 .5003-.2146 1.1096 1.1096 0 0 1 .7586.3762h.5171a.5142.5142 0 0 0 .043-.3461 1.2334 1.2334 0 0 1-.0107-.1387v-.5171a3.1097 3.1097 0 0 1-.2908.0126c-.119 0-.2399-.0049-.3556-.0097h-.007a8.4163 8.4163 0 0 0-.364-.0104 1.9597 1.9597 0 0 0-1.0172.2344 10.704 10.704 0 0 1-1.115.5817h-.003c-.1538.0728-.3128.148-.466.2244a.8853.8853 0 0 1-.4202.0646H5.2188a1.0967 1.0967 0 0 1-.6958.3284.7822.7822 0 0 1-.5983-.3271.7237.7237 0 0 1-.181-.5453.8462.8462 0 0 1 .3103-.586.735.735 0 0 1 .4732-.1974 1.0705 1.0705 0 0 1 .755.456h2.101a.6167.6167 0 0 0 .2232-.053 1.192 1.192 0 0 1 .1322-.044c.1316-.0646.2628-.1292.3898-.1893a10.0788 10.0788 0 0 0 .9354-.4894 2.555 2.555 0 0 1 1.353-.3617c.0646 0 .1312.002.1981.0058a2.065 2.065 0 0 0 .2586.0143c.0853 0 .17-.0033.2586-.0068h.0023c.092-.0036.1874-.0075.286-.0075a2.1442 2.1442 0 0 0 .0365-.5908c-.0019-.0701-.0042-.1425-.0042-.2172H9.4164a1.4545 1.4545 0 0 1-.7663.3316.6823.6823 0 0 1-.5262-.2993.8307.8307 0 0 1 .0646-1.0989.715.715 0 0 1 .4874-.2043 1.243 1.243 0 0 1 .7758.3662h2.004c0-.0898.007-.1803.0144-.2763.0087-.1138.0178-.2314.0178-.3701h.126c4.196 0 7.4922 1.6423 9.7967 4.8805a12.2263 12.2263 0 0 1 2.408 6.4563c.1212 2.2033-.439 4.4571-1.6646 6.6986a11.395 11.395 0 0 1-4.4335 4.4768A11.4803 11.4803 0 0 1 12.1227 24zm.3672-5.5768v4.4604a1.616 1.616 0 0 0 .2705.0217 3.4704 3.4704 0 0 0 .491-.0456c.109-.0152.2204-.0323.337-.0407a14.979 14.979 0 0 0 2.392-4.3957zm4.6543 0a19.092 19.092 0 0 1-1.8424 3.9433 10.38 10.38 0 0 0 5.3008-3.9433zm1.0343-5.7855a20.4576 20.4576 0 0 1-.6788 4.6543h3.814a11.2114 11.2114 0 0 0 1.2928-4.6543zm-5.6886 0v4.622h3.8786a18.1495 18.1495 0 0 0 .6787-4.622zm.0323-5.7855v4.6542h4.5573a18.7193 18.7193 0 0 0-.711-4.6542zm4.9452-.0324a21.3593 21.3593 0 0 1 .711 4.6543h4.4281a10.9179 10.9179 0 0 0-1.3252-4.6543zm-2.1979-5.0421a20.007 20.007 0 0 1 1.8747 3.9432h3.4584a10.6137 10.6137 0 0 0-5.333-3.9432zm-2.7473-.5818c0 1.5624 0 3.0382.0323 4.4927h3.4584a.1183.1183 0 0 1-.0323-.097 16.2011 16.2011 0 0 0-2.2302-4.1048c-.0126-.0126-.0249-.0262-.0378-.0404a.2773.2773 0 0 0-.1884-.1212 9.487 9.487 0 0 0-1.002-.1293z"/></svg>
