{
const folder = "2. Daily Reflection";
const startDate = dv.date("2025-11-22");
const endDate = dv.date("2025-11-28");

const pages = dv.pages(`"${folder}"`)
  .where(p => p.date && p.date >= startDate && p.date <= endDate && !p.file.name.includes("Dashboard"));

// --- FORCE WEEK TO START ON MONDAY ---
const orderedPages = [...pages].sort((a, b) => {
  const da = a.date.weekday === 0 ? 7 : a.date.weekday;
  const db = b.date.weekday === 0 ? 7 : b.date.weekday;
  return da - db;
});

const container = dv.el("div", "");

container.innerHTML = `
<style>
@import url('https://fonts.googleapis.com/css2?family=Afacad:wght@400;500;600&display=swap');

.loot-wrapper {
  margin: 40px 0;
  background: linear-gradient(180deg, var(--background-secondary) 0%, transparent 100%);
  padding: 32px 28px;
  border-radius: 16px;
  border-top: 1px solid var(--background-modifier-border);
}

.loot-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.loot-title {
  font-family: 'Afacad', sans-serif;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: var(--text-muted);
}

/* SORT CONTROLS */
.sort-controls {
  display: flex;
  gap: 16px;
  font-family: 'Afacad', sans-serif;
  font-size: 12px;
  color: var(--text-muted);
}

.sort-controls label {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
}

.sort-controls input[type="radio"] {
  accent-color: #FFD60A;
  cursor: pointer;
}

/* SHELF */
.loot-shelf {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.loot-slot {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  transition: transform 200ms ease;
}

.loot-slot:hover {
  transform: translateY(-6px);
}

.loot-score {
  font-family: 'Afacad', sans-serif;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-normal);
}

/* TRIANGLE STATES */
.loot-triangle {
  width: 42px;
  height: 42px;
  transition: filter 200ms ease, opacity 200ms ease;
}

/* < 50% */
.loot-low {
  fill: #FFD60A;
  opacity: 0.25;
}

/* 50–89% */
.loot-mid {
  fill: #FFD60A;
  opacity: 0.65;
  filter: drop-shadow(0 0 6px rgba(255, 214, 10, 0.35));
}

/* DIAMOND (100%) */
.loot-diamond {
  width: 42px;
  height: 42px;
}

.loot-diamond.loot-high {
  fill: #FFD60A;
  filter: drop-shadow(0 0 14px rgba(255, 214, 10, 0.85));
}

.loot-date {
  font-family: 'Afacad', sans-serif;
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--text-muted);
}
</style>

<div class="loot-wrapper">
  <div class="loot-header">
    <div class="loot-title">Weekly Loot Collection</div>

    <div class="sort-controls">
      <label>
        <input type="radio" name="lootSort" value="default" checked>
        Default
      </label>
      <label>
        <input type="radio" name="lootSort" value="asc">
        Least
      </label>
      <label>
        <input type="radio" name="lootSort" value="desc">
        Most
      </label>
    </div>
  </div>

  <div id="lootShelf" class="loot-shelf"></div>
</div>
`;

const shelf = container.querySelector("#lootShelf");

// --- BUILD DATA ONCE ---
const lootData = orderedPages.map(p => {
  const total = p.file.tasks.length || 1;
  const done = p.file.tasks.filter(t => t.completed).length;
  const pct = Math.round((done / total) * 100);

  return {
    day: p.date.toFormat("EEE"),
    pct,
    order: p.date.weekday === 0 ? 7 : p.date.weekday
  };
});

// --- RENDER FUNCTION ---
function renderLoot(mode) {
  shelf.innerHTML = "";

  let data = [...lootData];

  if (mode === "asc") data.sort((a, b) => a.pct - b.pct);
  if (mode === "desc") data.sort((a, b) => b.pct - a.pct);
  if (mode === "default") data.sort((a, b) => a.order - b.order);

  data.forEach(d => {
    let svg = "";
    let cls = "loot-low";

    if (d.pct === 100) {
      cls = "loot-high";
      svg = `
        <svg viewBox="0 0 24 24" class="loot-diamond ${cls}">
          <path d="M12 2l10 6-10 14L2 8z"/>
        </svg>
      `;
    } else {
      if (d.pct >= 50) cls = "loot-mid";
      svg = `
        <svg viewBox="0 0 24 24" class="loot-triangle ${cls}">
          <path d="M12 2L2 22h20L12 2z"/>
        </svg>
      `;
    }

    shelf.insertAdjacentHTML("beforeend", `
      <div class="loot-slot">
        <div class="loot-score">${d.pct}%</div>
        ${svg}
        <div class="loot-date">${d.day}</div>
      </div>
    `);
  });
}

// INITIAL RENDER
renderLoot("default");

// SORT HANDLERS
container.querySelectorAll('input[name="lootSort"]').forEach(radio => {
  radio.addEventListener("change", e => renderLoot(e.target.value));
});
}
