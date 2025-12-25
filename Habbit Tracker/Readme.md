# Obsidian Habit & Time Tracker Dashboard

Alright, let's build you a proper habit tracking system in Obsidian. This will be a full-featured dashboard with daily/weekly/monthly views, charts, and streak tracking.

## The Architecture (aka "How This Won't Fall Apart")

Here's what we're building:

1. **Daily Notes Structure** - YAML frontmatter to log your habits
2. **Dashboard** - Interactive DataviewJS with toggleable views
3. **Charts** - Line graphs, donuts, and streak displays using Chart.js

Let me create the complete solution:---

## What You're Getting

This system gives you:

✅ **Interactive dashboard** with toggleable daily/weekly/monthly views  
✅ **Line charts** showing habit trends over time  
✅ **Donut charts** displaying completion rates  
✅ **Duolingo-style streaks** with current and best streak tracking  
✅ **Automatic aggregation** for weekly/monthly averages  
✅ **Clean UI** that actually looks like an app  

## Key Features Explained

**Daily View**: Shows last 7 days in detail  
**Weekly View**: Aggregates last 12 weeks (averages habits per week)  
**Monthly View**: Aggregates last 12 months (averages habits per month)  

**Streaks**: Counts consecutive days where you completed a habit. For freelance hours, you need to hit your 2-hour target to maintain the streak.

## Important Notes

1. **Folder name matters**: Your daily notes MUST be in a folder called "Daily Notes" (or change it in the code)
2. **Date format matters**: Use YYYY-MM-DD in your frontmatter
3. **YAML structure matters**: Keep the exact structure I showed in the template

## Next Steps

1. Create the folder structure
2. Set up the daily note template
3. Create the dashboard note
4. Add the CSS snippet
5. Start logging your habits!

The dashboard will automatically pull data from all your daily notes and visualize it. As you add more daily notes over time, the charts and streaks will update automatically.

Need help customizing this (adding more habits, changing colors, adjusting the layout)? Let me know what you want to tweak.
