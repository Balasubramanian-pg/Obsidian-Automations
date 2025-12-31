const folder = "2. Daily Reflection";
const startDate = dv.date("2025-11-22");
const endDate = dv.date("2025-11-28");

const pages = dv.pages(`"${folder}"`)
  .where(p => p.date && p.date >= startDate && p.date <= endDate && !p.file.name.includes("Dashboard"))
  .sort(p => p.date, 'asc');

const habits = [
  "Exercise", "Read", "Drink water", "Meditate", "Journal",
  "Sleep", "Healthy meals", "No phone", "Deep work", "Social connection",
  "Tidy space", "Learn something", "Creative work", "Strength training",
  "Walk outside", "Review goals", "No social media", "No junk food",
  "Call family", "Brain training"
];

// --- PRECOMPUTE HABIT SCORES ---
const habitStats = habits.map(habit => {
  const completedDays = pages.filter(p =>
    p.file.tasks.some(t => t.text.includes(habit) && t.completed)
  ).length;

  return {
    name: habit,
    score: completedDays
  };
});

const container = dv.el("div", "");

container.innerHTML = `
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600&display=swap');

.dna-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px 16px;
}

.dna-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.dna-title {
  font-family: 'Outfit', sans-serif;
  font-size: 12px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--text-muted);
}

.sort-controls {
  display: flex;
  gap: 16px;
  font-family: 'Outfit', sans-serif;
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

.dna-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 24px 20px;
}

.dna-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.dna-label {
  font-family: 'Outfit', sans-serif;
  font-size: 11px;
  font-weight: 500;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.6px;
  text-align: center;
}

.dna-sequence {
  display: flex;
  justify-content: center;
  gap: 4px;
  padding: 8px;
  width: 100%;
  background: var(--background-secondary);
  border-radius: 8px;
  border: 1px solid var(--background-modifier-border);
  transition: box-shadow 200ms ease, border-color 200ms ease;
}

.dna-card:hover .dna-sequence {
  border-color: rgba(255, 214, 10, 0.5);
  box-shadow: 0 6px 16px rgba(255, 214, 10, 0.18);
}

.dna-bit {
  width: 10px;
  height: 22px;
  border-radius: 4px;
  background: var(--background-modifier-border);
}

.dna-bit.active {
  background: #FFD60A;
}
</style>

<div class="dna-wrapper">
  <div class="dna-header">
    <div class="dna-title">Weekly DNA Fingerprint</div>

    <div class="sort-controls">
      <label>
        <input type="radio" name="sortMode" value="desc" checked>
        Most achieved
      </label>
      <label>
        <input type="radio" name="sortMode" value="asc">
        Least achieved
      </label>
    </div>
  </div>

  <div id="dnaGrid" class="dna-grid"></div>
</div>
`;

const grid = container.querySelector("#dnaGrid");

function renderGrid(sortMode) {
  grid.innerHTML = "";

  const sorted = [...habitStats].sort((a, b) =>
    sortMode === "asc" ? a.score - b.score : b.score - a.score
  );

  sorted.forEach(habit => {
    const bits = pages.map(p => {
      const done = p.file.tasks.some(
        t => t.text.includes(habit.name) && t.completed
      );
      return `<div class="dna-bit ${done ? "active" : ""}"></div>`;
    }).join("");

    grid.insertAdjacentHTML("beforeend", `
      <div class="dna-card">
        <div class="dna-label">${habit.name}</div>
        <div class="dna-sequence">${bits}</div>
      </div>
    `);
  });
}

// Initial render
renderGrid("desc");

// Radio button handling
container.querySelectorAll('input[name="sortMode"]').forEach(input => {
  input.addEventListener("change", e => {
    renderGrid(e.target.value);
  });
});
