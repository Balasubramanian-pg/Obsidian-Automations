// ================================
// HABIT INTERFERENCE ANALYZER
// ================================

// -------- SOURCE CONFIG --------
const folder = "2. Daily Reflection";
const startDate = dv.date("2025-11-22");
const endDate   = dv.date("2025-11-28");

const pages = dv.pages(`"${folder}"`)
  .where(p => p.date && p.date >= startDate && p.date <= endDate);

// -------- HABIT CONFIG --------
const targetHabit = "Deep work";

const suspects = [
  "Sleep",
  "No junk food",
  "No phone",
  "Meditate",
  "Exercise"
];

// -------- FAILURE DAYS --------
const failDays = pages.filter(p =>
  !p.file.tasks.some(t =>
    t.text.includes(targetHabit) && t.completed
  )
);

// -------- NO FAILURES CASE --------
if (failDays.length === 0) {
  dv.el("div", `You protected **${targetHabit}** perfectly in this range.`);
} else {

  // -------- ANALYSIS --------
  const sabotageStats = suspects.map(suspect => {
    let present = 0;
    let failed  = 0;

    failDays.forEach(day => {
      const task = day.file.tasks.find(t =>
        t.text.includes(suspect)
      );

      if (task) {
        present++;
        if (!task.completed) failed++;
      }

      const fieldKey = suspect
        .toLowerCase()
        .replace(/\s/g, "");

      if (day[fieldKey] !== undefined) {
        present++;
        if (Number(day[fieldKey]) < 7) failed++;
      }
    });

    const confidence =
      present === 0
        ? 0
        : Math.round((failed / present) * 100);

    return {
      name: suspect,
      confidence
    };
  }).sort((a, b) => b.confidence - a.confidence);

  const primary = sabotageStats[0];

  // -------- RENDER --------
  const container = dv.el("div", "", {
    attr: {
      style: `
        margin: 40px 0;
        padding: 22px;
        border-left: 4px solid #AFAC2D;
        background: rgba(175, 172, 45, 0.12);
        border-radius: 10px;
        font-family: 'Afacad', system-ui, sans-serif;
      `
    }
  });

  container.innerHTML = `
  <style>
    .habit-header {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 12px;
    }

    .habit-title {
      font-weight: 700;
      letter-spacing: 1.6px;
      text-transform: uppercase;
      font-size: 12px;
      color: #AFAC2D;
    }

    .habit-icon svg {
      width: 22px;
      height: 22px;
      fill: #AFAC2D;
    }

    .habit-message {
      font-size: 18px;
      line-height: 1.55;
      color: var(--text-normal);
      margin-bottom: 18px;
    }

    .habit-list {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }

    .habit-chip {
      padding: 6px 14px;
      border-radius: 999px;
      font-size: 13px;
      font-weight: 600;
      background: rgba(175, 172, 45, 0.18);
      color: var(--text-normal);
    }

    .habit-focus {
      margin-top: 16px;
      font-size: 14px;
      color: var(--text-muted);
    }
  </style>

  <div class="habit-header">
    <span class="habit-icon">
      <svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <title>Spacemacs</title>
        <path d="M11.997.011c-1.79.015-3.452.397-4.968 1.093l.005-.002c3.638 2.026 6.955 5.634 8.932 8.241.398.534.753 1.006 1.078 1.434l.004-.019c.412-1.738-.313-5.239-1.518-7.331..."/>
      </svg>
    </span>
    <div class="habit-title">Habit Interference Pattern</div>
  </div>

  <div class="habit-message">
    When <b>${targetHabit}</b> breaks down, the strongest interference comes from
    <b>${primary.name}</b>, appearing in <b>${primary.confidence}%</b> of failure contexts.
  </div>

  <div class="habit-list">
    ${sabotageStats.map(s =>
      `<span class="habit-chip">${s.name}: ${s.confidence}%</span>`
    ).join("")}
  </div>

  <div class="habit-focus">
    Stabilize <b>${primary.name}</b> first. Everything else becomes cheaper after that.
  </div>
  `;
}
