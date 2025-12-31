const folder = "2. Daily Reflection";
const startDate = dv.date("2025-11-22");
const endDate = dv.date("2025-11-28");
const pages = dv.pages(`"${folder}"`)
    .where(p => p.date && p.date >= startDate && p.date <= endDate && !p.file.name.includes("Dashboard"));

// --- 1. Define Attributes & Habits ---
const attributes = {
    "STR (Vitality)": {
        icon: "⚡", 
        habits: ["Exercise", "Sleep", "Healthy meals", "Strength training", "Walk outside", "No junk food", "Drink water"]
    },
    "INT (Intellect)": {
        icon: "🧠", 
        habits: ["Read", "Learn something", "Brain training", "Deep work", "Review goals"]
    },
    "WIS (Serenity)": {
        icon: "👁️", 
        habits: ["Meditate", "Journal", "Tidy space", "No phone", "No social media"]
    },
    "CHA (Connection)": {
        icon: "🤝", 
        habits: ["Social connection", "Call family", "Creative work"]
    }
};

// --- 2. Calculate Levels ---
const stats = Object.keys(attributes).map(key => {
    const attr = attributes[key];
    let totalXP = 0;
    let maxXP = 0;

    pages.forEach(p => {
        attr.habits.forEach(h => {
            maxXP += 10; // Each habit is worth 10 XP
            if (p.file.tasks.some(t => t.text.includes(h) && t.completed)) {
                totalXP += 10;
            }
        });
    });

    const percentage = maxXP > 0 ? Math.round((totalXP / maxXP) * 100) : 0;
    // Level Logic: Level 1-10. 
    // e.g., 45% = Level 4 (50% progress to Level 5)
    const level = Math.floor(percentage / 10);
    const progressToNext = percentage % 10 * 10; // Scaling the remainder to 100%
    
    return { name: key, icon: attr.icon, level: level, bar: progressToNext, totalPct: percentage };
});

// --- 3. Render ---
const container = dv.el('div', '', { 
    attr: { style: 'margin-bottom: 40px; background: var(--background-secondary); padding: 25px; border-radius: 12px; border: 1px solid var(--background-modifier-border);' } 
});

let html = `
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;800&display=swap');
    .rpg-row { display: flex; align-items: center; margin-bottom: 15px; font-family: 'Outfit', sans-serif; }
    .rpg-icon { font-size: 24px; width: 40px; text-align: center; margin-right: 15px; }
    .rpg-info { flex-grow: 1; }
    .rpg-header { display: flex; justify-content: space-between; margin-bottom: 5px; font-size: 14px; color: var(--text-normal); font-weight: 700; }
    .rpg-level { color: #FFD60A; }
    .rpg-bar-bg { height: 8px; background: rgba(255, 255, 255, 0.05); border-radius: 4px; overflow: hidden; position: relative; }
    .rpg-bar-fill { height: 100%; background: linear-gradient(90deg, #FFD60A 0%, #FF9F1C 100%); border-radius: 4px; transition: width 0.5s ease; }
    .rpg-pills { display: flex; gap: 2px; margin-top: 4px; }
    .rpg-pill { width: 10px; height: 3px; background: #FFD60A; opacity: 0.3; border-radius: 1px; }
    .rpg-pill.active { opacity: 1; box-shadow: 0 0 5px #FFD60A; }
</style>
<h3 style="font-family: 'Outfit', sans-serif; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 2px; font-size: 12px; color: var(--text-muted);">Character Attributes</h3>
`;

stats.forEach(s => {
    // Generate Level "Pills" (Visual dots for level)
    let pills = '';
    for(let i=0; i<10; i++) {
        pills += `<div class="rpg-pill ${i < s.level ? 'active' : ''}"></div>`;
    }

    html += `
    <div class="rpg-row">
        <div class="rpg-icon">${s.icon}</div>
        <div class="rpg-info">
            <div class="rpg-header">
                <span>${s.name}</span>
                <span class="rpg-level">LVL ${s.level}</span>
            </div>
            <!-- The Progress Bar to Next Level -->
            <div class="rpg-bar-bg">
                <div class="rpg-bar-fill" style="width: ${s.bar}%;"></div>
            </div>
            <!-- The Total Level Pills -->
            <div class="rpg-pills">${pills}</div>
        </div>
    </div>`;
});

container.innerHTML = html;
