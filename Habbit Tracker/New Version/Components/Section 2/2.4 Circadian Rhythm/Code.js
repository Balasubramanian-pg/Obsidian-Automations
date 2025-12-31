const folder = "2. Daily Reflection";
const startDate = dv.date("2025-11-22");
const endDate = dv.date("2025-11-28");
const pages = dv.pages(`"${folder}"`)
    .where(p => p.date && p.date >= startDate && p.date <= endDate && !p.file.name.includes("Dashboard"));

// --- 1. Define Routines ---
// You must categorize your habits here manually
const morningHabits = ["Exercise", "Meditate", "Journal", "Drink water", "No phone", "Walk outside", "Plan day"];
const eveningHabits = ["Read", "Sleep", "Healthy meals", "Tidy space", "Review goals", "Call family", "No junk food"];

// --- 2. Calculate Balance ---
const calculateRate = (habitList) => {
    let possible = 0;
    let actual = 0;
    pages.forEach(p => {
        habitList.forEach(h => {
            possible++;
            if (p.file.tasks.some(t => t.text.includes(h) && t.completed)) actual++;
        });
    });
    return possible > 0 ? Math.round((actual / possible) * 100) : 0;
};

const amRate = calculateRate(morningHabits);
const pmRate = calculateRate(eveningHabits);

// --- 3. Render ---
const container = dv.el('div', '', { 
    attr: { style: 'margin-bottom: 40px; background: var(--background-secondary); padding: 25px; border-radius: 12px; border: 1px solid var(--background-modifier-border);' } 
});

container.innerHTML = `
    <style>
        .circadian-wrapper { font-family: 'Outfit', sans-serif; display: flex; align-items: center; gap: 20px; }
        .circadian-side { flex: 1; }
        .circadian-label { display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 14px; font-weight: 700; }
        .circadian-icon { font-size: 18px; }
        
        .bar-container { height: 12px; background: rgba(255,255,255,0.05); border-radius: 6px; overflow: hidden; position: relative; }
        
        /* Sun Style (Left) */
        .bar-sun { height: 100%; background: linear-gradient(90deg, #FFD60A 0%, #FF9F1C 100%); border-radius: 6px; }
        .sun-text { color: #FFD60A; text-shadow: 0 0 10px rgba(255, 214, 10, 0.4); }
        
        /* Moon Style (Right) */
        .bar-moon { height: 100%; background: linear-gradient(90deg, #2e8cfc 0%, #6c5ce7 100%); border-radius: 6px; }
        .moon-text { color: #2e8cfc; text-shadow: 0 0 10px rgba(46, 140, 252, 0.4); }
        
        .vs-badge { background: var(--background-primary); border: 1px solid var(--background-modifier-border); padding: 5px 10px; border-radius: 20px; font-size: 10px; color: var(--text-muted); font-weight: 700; }
    </style>

    <h3 style="font-family: 'Outfit', sans-serif; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 2px; font-size: 12px; color: var(--text-muted);">Circadian Rhythm</h3>

    <div class="circadian-wrapper">
        <!-- AM SIDE -->
        <div class="circadian-side">
            <div class="circadian-label sun-text">
                <span><span class="circadian-icon">☀</span> Morning Routine</span>
                <span>${amRate}%</span>
            </div>
            <div class="bar-container">
                <div class="bar-sun" style="width: ${amRate}%"></div>
            </div>
        </div>

        <div class="vs-badge">VS</div>

        <!-- PM SIDE -->
        <div class="circadian-side">
            <div class="circadian-label moon-text">
                <span>${pmRate}%</span>
                <span>Evening Ritual <span class="circadian-icon">🌙</span></span>
            </div>
            <div class="bar-container" style="display:flex; justify-content: flex-end;">
                <div class="bar-moon" style="width: ${pmRate}%"></div>
            </div>
        </div>
    </div>
    
    <div style="text-align: center; margin-top: 15px; font-size: 12px; color: var(--text-muted); font-style: italic;">
        ${amRate > pmRate + 10 ? "⚠️ You are starting strong but fading at night." : pmRate > amRate + 10 ? "⚠️ You are struggling to wake up, but ending strong." : "✨ Perfect Energy Balance."}
    </div>
`;
