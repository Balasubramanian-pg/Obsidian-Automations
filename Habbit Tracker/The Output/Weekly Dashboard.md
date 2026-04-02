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