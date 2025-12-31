const folder = "2. Daily Reflection";
const startDate = dv.date("2025-11-22");
const endDate = dv.date("2025-11-28");
const pages = dv.pages(`"${folder}"`)
    .where(p => p.date && p.date >= startDate && p.date <= endDate)
    .sort(p => p.date, 'asc');

// Extract data
const points = pages.map(p => {
    // Look for task count if numeric field missing, or just use 0
    let work = p.deep_work;
    if (!work) {
        // Fallback: Count tasks containing "Deep work"
        const dwTask = p.file.tasks.find(t => t.text.includes("Deep work") && t.completed);
        work = dwTask ? 4 : 0; // Assume 4 hours if checked but no number
    }
    
    let energy = p.energy || 5; // Default middle energy
    
    return { x: energy, y: work, date: p.date.toFormat('EEE') };
}).values;

const chartId = 'scatter-' + Math.random().toString(36).substr(2, 9);
const container = dv.el('div', '', { 
    attr: { style: 'margin-bottom: 40px; padding: 20px; background: var(--background-secondary); border-radius: 8px; border: 1px solid var(--background-modifier-border);' } 
});

container.innerHTML = `
    <h3 style="font-family: 'Outfit', sans-serif; text-transform: uppercase; letter-spacing: 2px; font-size: 12px; color: var(--text-muted);">Efficiency Matrix (Energy vs. Output)</h3>
    <div style="position: relative; height: 300px; width: 100%;">
        <canvas id="${chartId}"></canvas>
    </div>
    <div style="display: flex; justify-content: space-between; font-size: 10px; color: #666; font-family: 'Outfit'; margin-top: 5px;">
        <span>BURNOUT ZONE (Low Energy, High Work)</span>
        <span>FLOW STATE (High Energy, High Work)</span>
    </div>
`;

const runChart = () => {
    const ctx = document.getElementById(chartId);
    if (!ctx) return;

    new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Daily Performance',
                data: points,
                backgroundColor: '#FFD60A',
                pointRadius: 6,
                pointHoverRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const pt = context.raw;
                            return `${pt.date}: ${pt.y}h Work @ Lvl ${pt.x} Energy`;
                        }
                    }
                },
                legend: { display: false }
            },
            scales: {
                x: {
                    title: { display: true, text: 'Energy Level (1-10)', color: '#666', font: {family: 'Outfit'} },
                    min: 0, max: 10,
                    grid: { color: '#333' },
                    ticks: { color: '#888' }
                },
                y: {
                    title: { display: true, text: 'Deep Work (Hours)', color: '#666', font: {family: 'Outfit'} },
                    min: 0,
                    grid: { color: '#333' },
                    ticks: { color: '#888' }
                }
            }
        }
    });
};

if (!window.Chart) {
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js';
    script.onload = () => setTimeout(runChart, 100);
    document.head.appendChild(script);
} else {
    setTimeout(runChart, 100);
}

