const folder = "2. Daily Reflection";
const startDate = dv.date("2025-11-22");
const endDate = dv.date("2025-11-28");

const pagesRaw = dv.pages(`"${folder}"`)
  .where(p => p.date && p.date >= startDate && p.date <= endDate);

// --- NORMALIZE WEEKDAY (MON = 1, SUN = 7) ---
const pages = pagesRaw.map(p => {
  const wd = p.date.weekday === 0 ? 7 : p.date.weekday;
  return { page: p, weekday: wd };
});

const container = dv.el("div", "");

// ---------- STYLE + SHELL ----------
let html = `
<style>
@import url('https://fonts.googleapis.com/css2?family=Afacad:wght@400;500;600&display=swap');

.mind-wrapper {
  margin: 36px 0;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--background-modifier-border);
}

.mind-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.mind-title {
  font-family: 'Afacad', sans-serif;
  font-size: 12px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--text-muted);
}

/* CONTROLS */
.mind-controls {
  display: flex;
  gap: 16px;
  font-family: 'Afacad', sans-serif;
  font-size: 11px;
  color: var(--text-muted);
}

.mind-controls label {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
}

.mind-controls input {
  accent-color: #FFD60A;
  cursor: pointer;
}

/* TRACK */
.mind-track {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* NODE */
.mind-node {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

/* CORE */
.mind-core {
  position: relative;
  border-radius: 50%;
  background: rgba(255,255,255,0.06);
  transition: transform 200ms ease;
}

.state-zen {
  background: #FFD60A;
  box-shadow: 0 0 10px rgba(255,214,10,0.6);
}

/* FOCUS RING */
.focus-ring {
  position: absolute;
  inset: -6px;
  border-radius: 50%;
  border: 1px solid rgba(46,140,252,0.8);
  box-shadow: 0 0 10px rgba(46,140,252,0.45);
}

/* INTERACTION */
.mind-core:hover {
  transform: scale(1.15);
}

/* LABEL */
.mind-day {
  font-family: 'Afacad', sans-serif;
  font-size: 10px;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: var(--text-muted);
}
</style>

<div class="mind-wrapper">
  <div class="mind-header">
    <div class="mind-title">Mind-Space Topology</div>

    <div class="mind-controls">
      <label><input type="radio" name="mindSort" value="default" checked> Default</label>
      <label><input type="radio" name="mindSort" value="asc"> Asc</label>
      <label><input type="radio" name="mindSort" value="desc"> Desc</label>
    </div>
  </div>

  <div id="mindTrack" class="mind-track"></div>
</div>
`;

container.innerHTML = html;
const track = container.querySelector("#mindTrack");

// ---------- DATA MODEL ----------
const data = pages.map(({ page, weekday }) => {
  const meditated = page.file.tasks.some(t => t.text.includes("Meditate") && t.completed);
  const deepWork = page.file.tasks.some(t => t.text.includes("Deep work") && t.completed);

  let score = 0;
  if (meditated) score += 1;
  if (deepWork) score += 1;

  return {
    day: page.date.toFormat("EEE"),
    weekday,
    meditated,
    deepWork,
    score
  };
});

// ---------- RENDER ----------
function render(mode) {
  track.innerHTML = "";

  let sorted = [...data];

  if (mode === "default") sorted.sort((a, b) => a.weekday - b.weekday);
  if (mode === "asc") sorted.sort((a, b) => a.score - b.score);
  if (mode === "desc") sorted.sort((a, b) => b.score - a.score);

  sorted.forEach(d => {
    let size = 8;
    let cls = "";
    let ring = "";

    if (d.meditated) {
      size = 14;
      cls = "state-zen";
    }

    if (d.deepWork) {
      size = d.meditated ? 20 : 12;
      ring = `<div class="focus-ring"></div>`;
    }

    track.insertAdjacentHTML("beforeend", `
      <div class="mind-node">
        <div class="mind-core ${cls}" style="width:${size}px;height:${size}px;">
          ${ring}
        </div>
        <div class="mind-day">${d.day}</div>
      </div>
    `);
  });
}

// INITIAL RENDER (MONDAY FIRST)
render("default");

// CONTROLS
container.querySelectorAll('input[name="mindSort"]').forEach(r =>
  r.addEventListener("change", e => render(e.target.value))
);
