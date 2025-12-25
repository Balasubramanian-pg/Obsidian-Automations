# Obsidian Habit & Time Tracker - Complete Setup Guide

## Step 1: Daily Note Template

Create this template for your daily notes (store it in your templates folder):

```yaml
---
date: {{date:YYYY-MM-DD}}
habits:
  work_tasks: []  # List what you did at work
  free_time: []   # List what you did in free time
  got_chia_seeds: false
  cooked_dinner: false
  went_to_gym: false
  slept_before_1145: false
  freelance_hours: 0  # Number of hours spent on freelance
tags: daily-note
---

# {{date:YYYY-MM-DD}}

## Work
- 

## Free Time
- 

## Notes
- 
```

**How to use**: Each day, fill in the YAML frontmatter with your actual data. Mark booleans as `true`/`false`, add hours as numbers, and list items as bullet points.
