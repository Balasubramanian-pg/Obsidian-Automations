const folder = "2. Daily Reflection";
const startDate = dv.date("2025-11-22");
const endDate = dv.date("2025-11-28");
const pages = dv.pages(`"${folder}"`)
    .where(p => p.date && p.date >= startDate && p.date <= endDate)
    .sort(p => p.date, 'asc');

const container = dv.el('div', '', { 
    attr: { style: 'margin-bottom: 40px; background: var(--background-secondary); padding: 25px; border-radius: 12px; border: 1px solid var(--background-modifier-border);' } 
});

let html = `
<style>
    .hydro-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 10px; }
    .hydro-day { display: flex; flex-direction: column; align-items: center; gap: 5px; }
    .core-tube { 
        width: 14px; height: 80px; background: #222; border-radius: 10px; position: relative; overflow: hidden; border: 1px solid #444; 
    }
    .water-level { 
        position: absolute; bottom: 0; left: 0; right: 0; 
        background: linear-gradient(0deg, #2e8cfc 0%, #00d2d3 100%);
        box-shadow: 0 0 10px #2e8cfc;
        transition: height 0.5s;
    }
    .impurity {
        position: absolute; top: 0; left: 0; right: 0; height: 100%;
        background: repeating-linear-gradient(45deg, transparent, transparent 5px, rgba(255, 92, 92, 0.3) 5px, rgba(255, 92, 92, 0.3) 10px);
        z-index: 2;
    }
    .day-lbl { font-size: 10px; color: var(--text-muted); font-family: 'Outfit'; margin-top: 5px;}
</style>
<h3 style="font-family: 'Outfit', sans-serif; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 2px; font-size: 12px; color: var(--text-muted);">Hydro-Core Stability</h3>
<div class="hydro-grid">
`;

pages.forEach(p => {
    // Looks for "Drink water" task count OR "water:: X"
    const waterTask = p.file.tasks.some(t => t.text.includes("Drink water") && t.completed);
    let waterLvl = p.water || (waterTask ? 100 : 0); // Default to 100% if task checked, or specific number
    if (typeof waterLvl === 'number' && waterLvl < 10) waterLvl = waterLvl * 10; // Scale 1-10 to 10-100%

    // Check for impurity (Junk Food)
    const junkFood = p.file.tasks.some(t => t.text.includes("No junk food") && !t.completed); // If "No junk food" is UNCHECKED, it means you ate junk
    const impurityHtml = junkFood ? `<div class="impurity" title="System Contaminated: Junk Food Detected"></div>` : '';

    html += `
    <div class="hydro-day">
        <div class="core-tube">
            ${impurityHtml}
            <div class="water-level" style="height: ${waterLvl}%"></div>
        </div>
        <div class="day-lbl">${p.date.toFormat('EEE')}</div>
    </div>`;
});

html += `</div>`;
container.innerHTML = html;
