const folder = "2. Daily Reflection";
const startDate = dv.date("2025-11-22");
const endDate = dv.date("2025-11-28");

// 1. Fetch Data
const pages = dv.pages(`"${folder}"`)
    .where(p => p.date && p.date >= startDate && p.date <= endDate && !p.file.name.includes("Dashboard"));

// Calculate daily progress for every page first
const pageData = pages.map(p => {
    const total = p.file.tasks.length;
    const done = p.file.tasks.filter(t => t.completed).length;
    const progress = total > 0 ? (done / total) * 100 : 0;
    return { file: p.file, progress: progress };
});

// 2. Define Keystone Habits to Analyze
// These are the "Input" habits that likely affect your "Output"
const keystoneHabits = ["Sleep", "Meditate", "Exercise", "Deep work", "No phone"];

const correlations = keystoneHabits.map(habit => {
    // Filter days where habit was DONE
    const daysWith = pageData.filter(d => 
        d.file.tasks.some(t => t.text.includes(habit) && t.completed)
    );
    
    // Filter days where habit was MISSED
    const daysWithout = pageData.filter(d => 
        !d.file.tasks.some(t => t.text.includes(habit) && t.completed)
    );

    // Calculate Averages
    // We use .reduce on standard arrays (pageData is derived from .map so it's a DataArray, need to handle carefully)
    const getAvg = (arr) => {
        if (arr.length === 0) return 0;
        // Convert to standard array if it's a proxy
        const values = arr.map(x => x.progress); 
        // Sum
        let sum = 0;
        for(let v of values) sum += v;
        return sum / arr.length;
    };

    const avgWith = getAvg(daysWith);
    const avgWithout = getAvg(daysWithout);
    const diff = Math.round(avgWith - avgWithout);

    return { name: habit, diff: diff, avgWith: Math.round(avgWith) };
}).filter(x => x.diff > 0) // Only show positive correlations
  .sort((a, b) => b.diff - a.diff); // Sort by highest impact

// 3. Render
if (correlations.length > 0) {
    const container = dv.el('div', '', { 
        attr: { style: 'display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 40px;' } 
    });

    let html = `
    <style>
        .impact-card {
            background-color: var(--background-secondary);
            border: 1px solid var(--background-modifier-border);
            border-radius: 12px;
            padding: 20px;
            font-family: 'Outfit', sans-serif;
            position: relative;
            overflow: hidden;
        }
        .impact-badge {
            background: rgba(255, 214, 10, 0.15);
            color: #FFD60A;
            display: inline-block;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }
        .impact-text {
            font-size: 15px;
            color: var(--text-normal);
            line-height: 1.5;
        }
        .impact-highlight {
            color: #FFD60A;
            font-weight: 700;
        }
        .impact-arrow {
            font-size: 20px;
            vertical-align: middle;
            margin-right: 5px;
        }
    </style>
    `;

    // Take top 3 impacts
    correlations.slice(0, 3).forEach(c => {
        html += `
        <div class="impact-card">
            <div class="impact-badge">⚡ Impact Analysis</div>
            <div class="impact-text">
                On days you <b>${c.name}</b>, your overall performance is <span class="impact-highlight">+${c.diff}%</span> higher.
            </div>
        </div>`;
    });

    container.innerHTML = html;
}
