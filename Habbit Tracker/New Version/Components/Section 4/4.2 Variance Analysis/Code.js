// ===============================
// CONFIGURATION
// ===============================
const config = {
  folder: "2. Daily Reflection",
  startDate: "2025-11-22",
  endDate: "2025-11-28",
  targetCompliance: 85,
  criticalThreshold: 50
};

// ===============================
// DATA INGESTION
// ===============================
const start = dv.date(config.startDate);
const end   = dv.date(config.endDate);

const pages = dv.pages(`"${config.folder}"`)
  .where(p => p.date && p.date >= start && p.date <= end && !p.file.name.includes("Dashboard"))
  .sort(p => p.date, "asc");

const habits = [
  "Exercise","Read","Drink water","Meditate","Journal",
  "Sleep","Healthy meals","No phone","Deep work","Social connection",
  "Tidy space","Learn something","Creative work","Strength training",
  "Walk outside","Review goals","No social media","No junk food",
  "Call family","Brain training"
];

// ===============================
// CALCULATIONS
// ===============================
const dailyData = pages.map(p => {
  const total = p.file.tasks.length;
  const completed = p.file.tasks.filter(t => t.completed).length;
  return {
    displayDate: p.date.toFormat("dd MMM"),
    completed,
    total
  };
}).values;

const habitPerformance = habits.map(h => {
  const totalOpp = pages.length || 1;
  const actual = pages.filter(p =>
    p.file.tasks.some(t => t.text.includes(h) && t.completed)
  ).length;

  const rate = Math.round((actual / totalOpp) * 100);
  const variance = rate - config.targetCompliance;

  let status = "ON TRACK";
  let cls = "status-green";

  if (rate < config.criticalThreshold) {
    status = "CRITICAL";
    cls = "status-red";
  } else if (rate < config.targetCompliance) {
    status = "AT RISK";
    cls = "status-yellow";
  }

  return { name: h, actual: rate, variance, status, cls };
}).sort((a, b) => a.actual - b.actual);

const totalTasks = dailyData.reduce((a,d) => a + d.total, 0);
const totalDone  = dailyData.reduce((a,d) => a + d.completed, 0);
const overallCompliance = totalTasks ? Math.round((totalDone / totalTasks) * 100) : 0;
const criticalCount = habitPerformance.filter(h => h.status === "CRITICAL").length;
const atRiskCount   = habitPerformance.filter(h => h.status === "AT RISK").length;

// ===============================
// RENDER
// ===============================
const chartId = "kpi-chart-" + Math.random().toString(36).slice(2);
const container = dv.el("div", "", { cls: "dashboard-container" });

// ===============================
// STYLES (AFACAD SEMIBOLD)
// ===============================
const css = `
<style>
@import url('https://fonts.googleapis.com/css2?family=Afacad:wght@500;600;700&family=JetBrains+Mono:wght@500;600&display=swap');

:root {
  --gold: #AFAC2D;
  --gold-soft: #D6D35A;
  --gold-bg: rgba(175,172,45,0.14);
  --gold-border: rgba(175,172,45,0.45);
  --amber: #E6B800;
  --critical: #C94A4A;
}

.dashboard-container {
  font-family: 'Afacad', system-ui, sans-serif;
  font-weight: 600;
  color: var(--text-normal);
}

/* KPI */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4,1fr);
  gap: 20px;
  margin-bottom: 28px;
}

.kpi-card {
  background: var(--background-secondary);
  border: 1px solid var(--gold-border);
  border-radius: 12px;
  padding: 18px;
}

.kpi-label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--text-muted);
  margin-bottom: 4px;
}

.kpi-value {
  font-size: 30px;
  font-weight: 700;
  color: var(--gold);
}

.kpi-sub {
  font-size: 12px;
  color: var(--text-muted);
  display: flex;
  justify-content: space-between;
}

.trend-up { color: var(--gold); }
.trend-down { color: var(--amber); }

/* PANELS */
.mid-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 28px;
  margin-bottom: 28px;
}

.panel {
  background: var(--background-secondary);
  border: 1px solid var(--gold-border);
  border-radius: 12px;
  padding: 18px;
}

.panel-header {
  font-size: 14px;
  font-weight: 700;
  border-bottom: 1px solid var(--gold-border);
  padding-bottom: 8px;
  margin-bottom: 14px;
  display: flex;
  justify-content: space-between;
}

/* TABLE */
.data-table {
  width: 100%;
  border-collapse: collapse;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 600;
  font-size: 12px;
}

.data-table th,
.data-table td {
  border-bottom: 1px solid var(--gold-border);
  padding: 8px 4px;
}

.status-badge {
  padding: 2px 10px;
  border-radius: 999px;
  font-size: 10px;
  font-weight: 700;
}

.status-green { background: var(--gold-bg); color: var(--gold); }
.status-yellow { background: rgba(230,184,0,0.15); color: var(--amber); }
.status-red { background: rgba(201,74,74,0.15); color: var(--critical); }

/* HEATMAP */
.heatmap-grid {
  display: grid;
  grid-template-columns: 120px repeat(${pages.length},1fr);
  gap: 2px;
}

.hm-cell {
  height: 22px;
  border: 1px solid var(--gold-border);
}

.hm-header {
  font-size: 11px;
  color: var(--text-muted);
}

.hm-fill {
  background: linear-gradient(180deg,var(--gold),var(--gold-soft));
}

.hm-miss {
  background: rgba(201,74,74,0.12);
}

@media (max-width: 1200px) {
  .mid-section { grid-template-columns: 1fr; }
}
</style>
`;

// ===============================
// KPI HTML
// ===============================
const kpiHtml = `
<div class="kpi-grid">
  <div class="kpi-card">
    <div class="kpi-label">Compliance</div>
    <div class="kpi-value">${overallCompliance}%</div>
    <div class="kpi-sub">
      <span class="${overallCompliance >= config.targetCompliance ? "trend-up" : "trend-down"}">
        ${overallCompliance >= config.targetCompliance ? "On Target" : "Below Target"}
      </span>
      <span>${config.targetCompliance}%</span>
    </div>
  </div>

  <div class="kpi-card">
    <div class="kpi-label">Completed</div>
    <div class="kpi-value">${totalDone}</div>
    <div class="kpi-sub">of ${totalTasks}</div>
  </div>

  <div class="kpi-card">
    <div class="kpi-label">At Risk</div>
    <div class="kpi-value" style="color:var(--amber)">${atRiskCount}</div>
  </div>

  <div class="kpi-card">
    <div class="kpi-label">Critical</div>
    <div class="kpi-value" style="color:var(--critical)">${criticalCount}</div>
  </div>
</div>
`;

// ===============================
// TABLE
// ===============================
const tableHtml = `
<table class="data-table">
<thead>
<tr><th>Habit</th><th>Actual</th><th>Δ</th><th>Status</th></tr>
</thead>
<tbody>
${habitPerformance.slice(0,8).map(h => `
<tr>
<td>${h.name}</td>
<td>${h.actual}%</td>
<td style="color:${h.variance >= 0 ? 'var(--gold)' : 'var(--critical)'}">
${h.variance > 0 ? '+' : ''}${h.variance}%
</td>
<td><span class="status-badge ${h.cls}">${h.status}</span></td>
</tr>
`).join("")}
</tbody>
</table>
`;

// ===============================
// HEATMAP
// ===============================
let hmHtml = `
<div class="panel-header">Daily Completion Matrix</div>
<div class="heatmap-grid">
<div></div>
${dailyData.map(d => `<div class="hm-cell hm-header">${d.displayDate.split(" ")[0]}</div>`).join("")}
`;

habits.slice(0,10).forEach(h => {
  hmHtml += `<div class="hm-cell hm-header">${h}</div>`;
  pages.forEach(p => {
    const done = p.file.tasks.some(t => t.text.includes(h) && t.completed);
    hmHtml += `<div class="hm-cell ${done ? "hm-fill" : "hm-miss"}"></div>`;
  });
});
hmHtml += `</div>`;

// ===============================
// ASSEMBLE
// ===============================
container.innerHTML = css + kpiHtml + `
<div class="mid-section">
  <div class="panel">
    <div class="panel-header">Weekly Velocity</div>
    <canvas id="${chartId}" style="height:240px;"></canvas>
  </div>
  <div class="panel">
    <div class="panel-header">Variance Analysis</div>
    ${tableHtml}
  </div>
</div>
<div class="panel">${hmHtml}</div>
`;

// ===============================
// CHART
// ===============================
const initChart = () => {
  const ctx = document.getElementById(chartId);
  if (!ctx) return;

  new Chart(ctx, {
    type: "bar",
    data: {
      labels: dailyData.map(d => d.displayDate),
      datasets: [{
        data: dailyData.map(d => d.completed),
        backgroundColor: "rgba(175,172,45,0.65)",
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true },
        x: { grid: { display: false } }
      }
    }
  });
};

if (!window.Chart) {
  const s = document.createElement("script");
  s.src = "https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js";
  s.onload = () => setTimeout(initChart, 100);
  document.head.appendChild(s);
} else {
  setTimeout(initChart, 100);
}
