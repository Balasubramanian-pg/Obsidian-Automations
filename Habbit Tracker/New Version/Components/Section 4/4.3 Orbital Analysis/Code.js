const folder = "2. Daily Reflection";
const startDate = dv.date("2025-11-22");
const endDate = dv.date("2025-11-28");
const pages = dv.pages(`"${folder}"`)
    .where(p => p.date && p.date >= startDate && p.date <= endDate);

// Select 5 Key Habits to visualize as planets
const planets = [
    { name: "Deep work", icon: "⚡" },
    { name: "Exercise", icon: "💪" },
    { name: "Sleep", icon: "🌙" },
    { name: "Meditate", icon: "👁️" },
    { name: "No phone", icon: "📵" }
];

const planetStats = planets.map(h => {
    const total = pages.length || 1;
    const done = pages.filter(p => p.file.tasks.some(t => t.text.includes(h.name) && t.completed)).length;
    const pct = Math.round((done / total) * 100);
    
    // Physics Math
    // Higher % = Closer Orbit (Smaller Radius) + Faster Speed (Lower Duration)
    // Radius: 50px (closest) to 150px (farthest)
    const orbitRadius = 160 - (pct * 1.1); 
    // Speed: 3s (fastest) to 20s (slowest)
    const speed = 20 - (pct * 0.17); 
    
    return { ...h, pct, radius: orbitRadius, speed: speed };
});

const container = dv.el('div', '', { 
    attr: { style: 'height: 350px; background: radial-gradient(circle at center, #1a1a1a 0%, #000 70%); border: 1px solid #333; border-radius: 12px; position: relative; overflow: hidden; margin-bottom: 40px;' } 
});

let html = `
<style>
    .solar-system { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 300px; height: 300px; }
    .sun { 
        position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
        width: 40px; height: 40px; background: #FFD60A; border-radius: 50%;
        box-shadow: 0 0 30px #FFD60A; z-index: 10;
        display: flex; align-items: center; justify-content: center; font-size: 20px;
    }
    .orbit-ring {
        position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
        border: 1px dashed rgba(255,255,255,0.1); border-radius: 50%;
    }
    .planet-container {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        animation: spin linear infinite;
    }
    .planet {
        position: absolute; top: 50%; left: 100%; transform: translate(-50%, -50%);
        width: 24px; height: 24px; background: #222; border: 1px solid #FFD60A;
        border-radius: 50%; color: #fff; display: flex; align-items: center; justify-content: center; font-size: 12px;
        box-shadow: 0 0 5px rgba(255, 214, 10, 0.5);
    }
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
</style>
<div style="position: absolute; top: 15px; left: 15px; font-family: 'Outfit'; font-size: 12px; color: #666; letter-spacing: 2px;">GRAVITY WELL SIMULATION</div>
<div class="solar-system">
    <div class="sun">🧘</div>
`;

planetStats.forEach(p => {
    // We create a ring and a rotator for each planet
    html += `
    <div class="orbit-ring" style="width: ${p.radius * 2}px; height: ${p.radius * 2}px;"></div>
    <div class="orbit-ring" style="width: ${p.radius * 2}px; height: ${p.radius * 2}px; border: none; animation: spin ${p.speed}s linear infinite;">
        <div class="planet" title="${p.name}: ${p.pct}% consistency">${p.icon}</div>
    </div>
    `;
});

html += `</div>`;
container.innerHTML = html;
