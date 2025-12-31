const folder = "2. Daily Reflection";
const startDate = dv.date("2025-11-22");
const endDate = dv.date("2025-11-28");

const pages = dv.pages(`"${folder}"`)
  .where(p => p.date && p.date >= startDate && p.date <= endDate && !p.file.name.includes("Dashboard"));

const habits = [
  "Exercise", "Read", "Drink water", "Meditate", "Journal",
  "Sleep", "Healthy meals", "No phone", "Deep work", "Social connection",
  "Tidy space", "Learn something", "Creative work", "Strength training",
  "Walk outside", "Review goals", "No social media", "No junk food",
  "Call family", "Brain training"
];

// Compute stats once
const stats = habits.map((habit, index) => {
  const totalDays = pages.length || 1;
  const completedDays = pages.filter(p =>
    p.file.tasks.some(t => t.text.includes(habit) && t.completed)
  ).length;

  return {
    name: habit,
    index,
    completed: completedDays,
    total: totalDays,
    level: Math.round((completedDays / totalDays) * 10)
  };
});

const container = dv.el("div", "");

container.innerHTML = `
<style>
@import url('https://fonts.googleapis.com/css2?family=Afacad:wght@400;500;600&display=swap');

.synth-wrapper {
  width: 100%;
  background: var(--background-secondary);
  padding: 28px 24px;
  border-radius: 16px;
  border: 1px solid var(--background-modifier-border);
}

.synth-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 22px;
}

.synth-title {
  font-family: 'Afacad', sans-serif;
  font-size: 12px;
  letter-spacing: 2px;
  text-transform: uppercase;
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

/* GRID */
.synth-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(48px, 1fr));
  align-items: end;
  gap: 16px;
  width: 100%;
}

/* CHANNEL */
.synth-channel {
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* BAR */
.synth-bar {
  display: flex;
  flex-direction: column-reverse;
  gap: 4px;
  padding: 8px 6px;
  border-radius: 10px;
  transition: transform 180ms ease, box-shadow 180ms ease;
}

.synth-channel:hover .synth-bar {
  transform: translateY(-3px);
  box-shadow: 0 10px 24px rgba(255, 214, 10, 0.22);
}

/* LED */
.synth-led {
  width: 22px;
  height: 11px;
  border-radius: 4px;
  background: var(--background-modifier-border);
  opacity: 0.25;
}

.synth-led.active {
  opacity: 1;
  background: #FFD60A;
}

.synth-led.peak {
  background: #FFB703;
}

/* LABEL */
.synth-label {
  margin-top: 10px;
  font-family: 'Afacad', sans-serif;
  font-size: 11px;
  font-weight: 500;
  color: var(--text-muted);
  text-align: center;
  line-height: 1.3;
  max-width: 80px;
}

/* TOOLTIP */
.synth-tooltip {
  margin-top: 10px;
  padding: 8px 10px;
  background: rgba(18, 18, 18, 0.95);
  border-radius: 10px;
  border: 1px solid rgba(255, 214, 10, 0.45);
  font-family: 'Afacad', sans-serif;
  font-size: 11px;
  color: #fff;
  white-space: nowrap;
  opacity: 0;
  transform: translateY(-4px);
  transition: opacity 160ms ease, transform 160ms ease;
  pointer-events: none;
}

.synth-channel:hover .synth-tooltip {
  opacity: 1;
  transform: translateY(0);
}

.synth-tooltip .name {
  font-weight: 600;
  margin-bottom: 4px;
}

.synth-tooltip .meta {
  color: #FFD60A;
  font-weight: 500;
}
</style>

<div class="synth-wrapper">
  <div class="synth-header">
    <div class="synth-title">Habit Frequency Response</div>

    <div class="sort-controls">
      <label>
        <input type="radio" name="sortModeSynth" value="default" checked>
        Default
      </label>
      <label>
        <input type="radio" name="sortModeSynth" value="desc">
        Most frequent
      </label>
      <label>
        <input type="radio" name="sortModeSynth" value="asc">
        Least frequent
      </label>
    </div>
  </div>

  <div id="synthGrid" class="synth-container"></div>
</div>
`;

const grid = container.querySelector("#synthGrid");

function renderSynth(sortMode) {
  grid.innerHTML = "";

  let sorted = [...stats];

  if (sortMode === "asc") {
    sorted.sort((a, b) => a.level - b.level);
  } else if (sortMode === "desc") {
    sorted.sort((a, b) => b.level - a.level);
  } else {
    sorted.sort((a, b) => a.index - b.index);
  }

  sorted.forEach(stat => {
    const leds = Array.from({ length: 10 }, (_, i) => {
      const active = i < stat.level;
      const peak = i === 9 && active;
      return `<div class="synth-led ${active ? "active" : ""} ${peak ? "peak" : ""}"></div>`;
    }).join("");

    grid.insertAdjacentHTML("beforeend", `
      <div class="synth-channel">
        <div class="synth-bar">
          ${leds}
        </div>

        <div class="synth-tooltip">
          <div class="name">${stat.name}</div>
          <div class="meta">${stat.completed} / ${stat.total} days</div>
        </div>

        <div class="synth-label">${stat.name}</div>
      </div>
    `);
  });
}

// Initial render
renderSynth("default");

// Radio listeners
container.querySelectorAll('input[name="sortModeSynth"]').forEach(radio => {
  radio.addEventListener("change", e => {
    renderSynth(e.target.value);
  });
});
