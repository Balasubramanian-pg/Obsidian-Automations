const folder = "2. Daily Reflection";
const startDate = dv.date("2025-11-22");
const endDate = dv.date("2025-11-28");

// --- 1. CONFIGURATION ---
const habits = [
    "Exercise", "Read", "Drink water", "Meditate", "Journal",
    "Sleep", "Healthy meals", "No phone", "Deep work", "Social connection",
    "Tidy space", "Learn something", "Creative work", "Strength training",
    "Walk outside", "Review goals", "No social media", "No junk food",
    "Call family", "Brain training"
];

// COLORS
const colorPower = "#10B981"; // Emerald Green
const colorBuild = "#FFD60A"; // Gold
const colorFocus = "#FF453A"; // Red

// ICONS (SVG)
const iconPuma = `<svg viewBox="0 0 24 24" class="cat-icon"><path d="M23.845 3.008c-.417-.533-1.146-.106-1.467.08-2.284 1.346-2.621 3.716-3.417 5.077-.626 1.09-1.652 1.89-2.58 1.952-.686.049-1.43-.084-2.168-.405-1.807-.781-2.78-1.792-3.017-1.97-.487-.37-4.23-4.015-7.28-4.164 0 0-.372-.75-.465-.763-.222-.025-.45.451-.616.501-.15.053-.413-.512-.565-.487-.153.02-.302.586-.6.877-.22.213-.486.2-.637.463-.052.096-.034.265-.093.42-.127.32-.551.354-.555.697 0 .381.357.454.669.72.248.212.265.362.554.461.258.088.632-.187.964-.088.277.081.543.14.602.423.054.256 0 .658-.34.613-.112-.015-.598-.174-1.198-.11-.725.077-1.553.309-1.634 1.11-.041.447.514.97 1.055.866.371-.071.196-.506.399-.716.267-.27 1.772.944 3.172.944.593 0 1.031-.15 1.467-.605.04-.029.093-.102.155-.11a.632.632 0 01.195.088c1.131.897 1.984 2.7 6.13 2.721.582.007 1.25.279 1.796.777.48.433.764 1.125 1.037 1.825.418 1.053 1.161 2.069 2.292 3.203.06.068.99.78 1.06.833.012.01.084.167.053.255-.02.69-.123 2.67 1.365 2.753.366.02.275-.231.275-.41-.005-.341-.065-.685.113-1.04.253-.478-.526-.709-.509-1.756.019-.784-.645-.651-.984-1.25-.19-.343-.368-.532-.35-.946.073-2.38-.517-3.948-.805-4.327-.227-.294-.423-.403-.207-.54 1.24-.815 1.525-1.574 1.525-1.574.66-1.541 1.256-2.945 2.075-3.57.166-.12.589-.44.852-.56.763-.362 1.173-.578 1.388-.788.356-.337.635-1.053.294-1.48z"/></svg>`;
const iconPoetry = `<svg viewBox="0 0 24 24" class="cat-icon"><path d="M21.604 0a19.144 19.144 0 0 1-5.268 13.213L2.396 0l13.583 13.583a19.149 19.149 0 0 1-13.583 5.624V0h19.208Zm-1.911 17.297A24.455 24.455 0 0 1 7.189 24l-4.053-4.053a19.91 19.91 0 0 0 13.37-5.838l3.187 3.188Z"/></svg>`;
const iconPrometheus = `<svg viewBox="0 0 24 24" class="cat-icon"><path d="M12 0C5.373 0 0 5.372 0 12c0 6.627 5.373 12 12 12s12-5.373 12-12c0-6.628-5.373-12-12-12zm0 22.46c-1.885 0-3.414-1.26-3.414-2.814h6.828c0 1.553-1.528 2.813-3.414 2.813zm5.64-3.745H6.36v-2.046h11.28v2.046zm-.04-3.098H6.391c-.037-.043-.075-.086-.111-.13-1.155-1.401-1.427-2.133-1.69-2.879-.005-.025 1.4.287 2.395.511 0 0 .513.119 1.262.255-.72-.843-1.147-1.915-1.147-3.01 0-2.406 1.845-4.508 1.18-6.207.648.053 1.34 1.367 1.387 3.422.689-.951.977-2.69.977-3.755 0-1.103.727-2.385 1.454-2.429-.648 1.069.168 1.984.894 4.256.272.854.237 2.29.447 3.201.07-1.892.395-4.652 1.595-5.605-.529 1.2.079 2.702.494 3.424.671 1.164 1.078 2.047 1.078 3.716a4.642 4.642 0 01-1.11 2.996c.792-.149 1.34-.283 1.34-.283l2.573-.502s-.374 1.538-1.81 3.019z"/></svg>`;

// --- 2. DATA CALCULATION ---
const pages = dv.pages(`"${folder}"`)
    .where(p => p.date && p.date >= startDate && p.date <= endDate)
    .sort(p => p.date, 'asc');

if (pages.length === 0) {
    dv.paragraph("No data found for the selected range.");
} else {

    let habitStats = habits.map(habit => {
        let total = 0;
        let completed = 0;
        
        pages.forEach(p => {
            if (!p.file.tasks) return;
            // Check if this file has a task with this habit name
            const t = p.file.tasks.find(x => x.text.includes(habit));
            if (t) {
                total++;
                if (t.completed) completed++;
            }
        });
        
        // Avoid division by zero
        const percent = total === 0 ? 0 : Math.round((completed / total) * 100);
        return { name: habit, percent: percent };
    }).sort((a, b) => b.percent - a.percent);

    // Grouping
    const powerHabits = habitStats.filter(h => h.percent >= 90);
    const buildingHabits = habitStats.filter(h => h.percent >= 60 && h.percent < 90);
    const needsFocus = habitStats.filter(h => h.percent < 60);

    // --- 3. RENDERING ---
    
    // Create CSS for styling
    const css = `
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&display=swap');

        .lb-container {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 40px;
            font-family: 'Outfit', sans-serif;
            margin-top: 20px;
        }

        .lb-column {
            background-color: var(--background-secondary);
            border-radius: 12px;
            padding: 24px;
            border: 1px solid var(--background-modifier-border);
        }

        .lb-header {
            display: flex;
            align-items: center;
            gap: 10px;
            padding-bottom: 20px;
            margin-bottom: 24px;
            border-bottom: 1px solid var(--background-modifier-border);
            font-weight: 700;
            font-size: 14px;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }

        .cat-icon {
            width: 20px;
            height: 20px;
        }

        .habit-row {
            display: flex;
            align-items: center;
            margin-bottom: 24px; /* INCREASED VERTICAL SPACING */
            font-size: 14px;
        }

        .habit-name {
            width: 35%;
            font-weight: 500;
            color: var(--text-normal);
            padding-right: 15px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .habit-bar-bg {
            flex-grow: 1;
            height: 8px;
            background-color: rgba(255, 255, 255, 0.08);
            border-radius: 4px;
            overflow: hidden;
            margin-right: 15px;
        }

        .habit-bar-fill {
            height: 100%;
            border-radius: 4px;
        }

        .habit-percent {
            width: 35px;
            text-align: right;
            font-weight: 700;
            font-size: 13px;
        }

        /* MEDIA QUERIES FOR MOBILE */
        @media (max-width: 900px) {
            .lb-container { grid-template-columns: 1fr; }
        }
    </style>
    `;

    // Helper Function to Render a Column
    const renderColumn = (title, iconSvg, data, color) => {
        const rows = data.map(h => `
            <div class="habit-row">
                <div class="habit-name">${h.name}</div>
                <div class="habit-bar-bg">
                    <div class="habit-bar-fill" style="width: ${h.percent}%; background-color: ${color};"></div>
                </div>
                <div class="habit-percent" style="color: ${color};">${h.percent}%</div>
            </div>
        `).join("");

        return `
            <div class="lb-column" style="border-top: 3px solid ${color};">
                <div class="lb-header" style="color: ${color};">
                    <div style="fill: ${color}; display:flex;">${iconSvg}</div>
                    ${title}
                </div>
                <div class="lb-content">
                    ${rows.length ? rows : '<div style="color:var(--text-muted); padding:10px 0;">No habits here yet.</div>'}
                </div>
            </div>
        `;
    };

    dv.container.innerHTML = `
        ${css}
        <h3 style="margin-bottom: 20px; font-family: 'Outfit', sans-serif;">🏆 Habit Consistency Leaderboard</h3>
        <div class="lb-container">
            ${renderColumn("Power Habits", iconPuma, powerHabits, colorPower)}
            ${renderColumn("Building", iconPoetry, buildingHabits, colorBuild)}
            ${renderColumn("Needs Focus", iconPrometheus, needsFocus, colorFocus)}
        </div>
    `;
}
