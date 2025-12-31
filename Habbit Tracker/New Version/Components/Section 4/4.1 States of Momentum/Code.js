// =====================================
// HABIT MOMENTUM PHASE STATES
// =====================================

// -------- SOURCE --------
const folder = "2. Daily Reflection";
const startDate = dv.date("2025-11-22");
const endDate   = dv.date("2025-11-28");

const pages = dv.pages(`"${folder}"`)
  .where(p => p.date && p.date >= startDate && p.date <= endDate)
  .sort(p => p.date, "asc");

// -------- CONFIG --------
const habits = [
  "Exercise",
  "Deep work",
  "Sleep",
  "Read",
  "Meditate",
  "No phone"
];

// -------- HELPERS --------
const midpoint = Math.floor(pages.length / 2);
const firstHalf = pages.slice(0, midpoint);
const secondHalf = pages.slice(midpoint);

const completionRate = (arr, habit) => {
  if (!arr.length) return 0;
  const hits = arr.filter(p =>
    p.file.tasks.some(t => t.text.includes(habit) && t.completed)
  ).length;
  return Math.round((hits / arr.length) * 100);
};

// -------- ANALYSIS --------
const results = habits.map(habit => {
  const startRate = completionRate(firstHalf, habit);
  const endRate   = completionRate(secondHalf, habit);
  const diff      = endRate - startRate;

  const totalRate = completionRate(pages, habit);

  let state = "STABLE";

  if (diff <= -10) {
    state = "DECAYING";
  } else if (diff >= 10 && totalRate >= 60) {
    state = "BUILDING";
  } else if (diff >= 0 && totalRate < 60) {
    state = "FRAGILE";
  }

  return {
    habit,
    state,
    diff,
    totalRate
  };
});

// -------- RENDER --------
const container = dv.el("div", "", {
  attr: {
    style: `
      margin: 32px 0;
      padding: 20px;
      background: var(--background-secondary);
      border-radius: 14px;
      font-family: 'Afacad', system-ui, sans-serif;
    `
  }
});

const stateColor = {
  BUILDING: "#2EB086",
  STABLE:   "#4C9AFF",
  FRAGILE:  "#F2C94C",
  DECAYING: "#FF5C5C"
};

container.innerHTML = `
<style>
  .phase-title {
    font-size: 12px;
    letter-spacing: 1.6px;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 16px;
  }

  .phase-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 14px;
  }

  .phase-card {
    padding: 14px;
    border-radius: 12px;
    background: rgba(255,255,255,0.04);
    border-left: 4px solid transparent;
  }

  .phase-habit {
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 6px;
  }

  .phase-state {
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 8px;
  }

  .phase-meta {
    font-size: 13px;
    color: var(--text-muted);
  }
</style>

<div class="phase-title">Habit Momentum States</div>

<div class="phase-grid">
  ${results.map(r => `
    <div
      class="phase-card"
      style="border-left-color: ${stateColor[r.state]};"
    >
      <div class="phase-habit">${r.habit}</div>
      <div
        class="phase-state"
        style="color: ${stateColor[r.state]};"
      >
        ${r.state}
      </div>
      <div class="phase-meta">
        Change: ${r.diff > 0 ? "+" : ""}${r.diff}%<br>
        Consistency: ${r.totalRate}%
      </div>
    </div>
  `).join("")}
</div>
`;
