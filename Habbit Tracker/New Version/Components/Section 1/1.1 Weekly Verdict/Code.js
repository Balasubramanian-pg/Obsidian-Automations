const folder = "2. Daily Reflection";
const startDate = dv.date("2025-11-22");
const endDate = dv.date("2025-11-28");

// Fetch pages
const pages = dv.pages(`"${folder}"`)
    .where(p => p.date && p.date >= startDate && p.date <= endDate && !p.file.name.includes("Dashboard"));

// --- 1. Calculate Grade ---
// FIX: Added .values before .reduce()
const totalTasks = pages.map(p => p.file.tasks.length).values.reduce((a, b) => a + b, 0);

// FIX: Added .values before .reduce()
const totalDone = pages.map(p => p.file.tasks.filter(t => t.completed).length).values.reduce((a, b) => a + b, 0);

const overallPct = totalTasks > 0 ? Math.round((totalDone / totalTasks) * 100) : 0;

let grade = "F";
let gradeColor = "#FF5C5C"; // Red
let message = "Time to reset and restart.";

if (overallPct >= 95) { grade = "S"; gradeColor = "#FFD60A"; message = "God Tier Discipline."; } // Gold
else if (overallPct >= 85) { grade = "A"; gradeColor = "#2EB086"; message = "Excellent execution."; } // Green
else if (overallPct >= 70) { grade = "B"; gradeColor = "#2e8cfc"; message = "Solid, consistent week."; } // Blue
else if (overallPct >= 50) { grade = "C"; gradeColor = "#A0A0A0"; message = "Average. Room for growth."; } // Grey
else { grade = "D"; gradeColor = "#FF9F1C"; message = "Struggling. Focus on basics."; } // Orange

// --- 2. Find "The One Thing" (Lowest Performing Habit) ---
const habits = [
    "Exercise", "Read", "Drink water", "Meditate", "Journal",
    "Sleep", "Healthy meals", "No phone", "Deep work", "Social connection",
    "Tidy space", "Learn something", "Creative work", "Strength training",
    "Walk outside", "Review goals", "No social media", "No junk food",
    "Call family", "Brain training"
];

const habitStats = habits.map(habit => {
    // Note: pages.length works on DataArrays, so no .values needed here
    const completed = pages.filter(p => p.file.tasks.some(t => t.text.includes(habit) && t.completed)).length;
    const total = pages.length || 1;
    return { name: habit, pct: Math.round((completed / total) * 100) };
}).sort((a, b) => a.pct - b.pct); // Sort Low to High

// Get the worst habit
const focusHabit = habitStats[0];

// --- 3. Render ---
const container = dv.el('div', '', { 
    attr: { style: 'margin-top: 40px; margin-bottom: 20px;' } 
});

container.innerHTML = `
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&display=swap');
        
        .verdict-container {
            display: flex;
            background: linear-gradient(145deg, var(--background-secondary) 0%, var(--background-primary) 100%);
            border: 1px solid var(--background-modifier-border);
            border-radius: 16px;
            padding: 30px;
            align-items: center;
            gap: 40px;
            font-family: 'Outfit', sans-serif;
            position: relative;
            overflow: hidden;
        }
        
        /* The Grade Stamp */
        .grade-circle {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            border: 4px solid ${gradeColor};
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 48px;
            font-weight: 900;
            color: ${gradeColor};
            box-shadow: 0 0 20px ${gradeColor}40; /* Glow effect */
            flex-shrink: 0;
        }

        .verdict-content {
            flex-grow: 1;
        }
        
        .verdict-title {
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: var(--text-muted);
            margin-bottom: 8px;
        }
        
        .verdict-message {
            font-size: 24px;
            font-weight: 700;
            color: var(--text-normal);
            margin-bottom: 4px;
        }
        
        .verdict-sub {
            font-size: 14px;
            color: var(--text-muted);
            font-style: italic;
        }

        /* The Focus Section */
        .focus-box {
            background: rgba(255, 214, 10, 0.1);
            border-left: 4px solid #FFD60A;
            padding: 15px 25px;
            border-radius: 0 8px 8px 0;
            min-width: 250px;
        }
        
        .focus-label {
            color: #FFD60A;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            margin-bottom: 5px;
        }
        
        .focus-value {
            color: var(--text-normal);
            font-size: 18px;
            font-weight: 600;
        }
        
        @media (max-width: 768px) {
            .verdict-container { flex-direction: column; text-align: center; gap: 20px; }
            .focus-box { width: 100%; text-align: center; border-left: none; border-top: 4px solid #FFD60A; }
        }
    </style>

    <div class="verdict-container">
        <div class="grade-circle">${grade}</div>
        
        <div class="verdict-content">
            <div class="verdict-title">Weekly Verdict</div>
            <div class="verdict-message">${message}</div>
            <div class="verdict-sub">You completed ${totalDone} out of ${totalTasks} scheduled habits.</div>
        </div>
        
        <div class="focus-box">
            <div class="focus-label">⚠️ Priority Fix For Next Week</div>
            <div class="focus-value">${focusHabit.name}</div>
            <div style="font-size: 12px; color: var(--text-muted); margin-top: 4px;">Only ${focusHabit.pct}% consistency</div>
        </div>
    </div>
`;
