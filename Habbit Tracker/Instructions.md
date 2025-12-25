## How to Use

1. **Daily**: Create a new note using your template each day (or automate with Templater/Daily Notes plugin)
2. **Fill in habits**: Update the YAML frontmatter with your actual data
3. **View dashboard**: Open `📊 Habit Dashboard` to see your progress
4. **Toggle views**: Click Daily/Weekly/Monthly buttons to switch perspectives

---

## What Each View Shows

- **Daily**: Last 7 days, day-by-day trends
- **Weekly**: Last 12 weeks, averaged by week
- **Monthly**: Last 12 months, averaged by month

---

## Troubleshooting

**Charts not showing?**
- Make sure Chart.js loads (check console for errors)
- Verify your daily notes are in the "Daily Notes" folder

**No data appearing?**
- Check that your daily notes have the `date` field in YAML
- Ensure the `habits` object exists in frontmatter

**Streaks seem wrong?**
- Streaks only count consecutive days where you completed the habit
- For numeric habits, you must meet or exceed the target (2 hours for freelance)

---

## Customization Tips

**Add more habits**: Edit `habitConfig` in the dashboard code
**Change colors**: Modify the `color` values in `habitConfig`
**Adjust targets**: Change `target` value for numeric habits
**Change folder**: Replace `"Daily Notes"` in `getDailyNotes()` function

---

## Example Daily Note

```yaml
---
date: 2025-01-15
habits:
  work_tasks: 
    - Finished Q4 report
    - Team standup
    - Code review
  free_time: 
    - Read for 30 mins
    - Watched a movie
  got_chia_seeds: true
  cooked_dinner: true
  went_to_gym: true
  slept_before_1145: false
  freelance_hours: 2.5
tags: daily-note
---

# 2025-01-15

## Work
- Crushed that Q4 report
- Helped junior dev with Python debugging

## Free Time
- Finally watched that movie everyone's been talking about

## Notes
- Need to fix sleep schedule (again)
```
