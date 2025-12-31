const folder = "2. Daily Reflection";
const startDate = dv.date("2025-11-22");
const endDate = dv.date("2025-11-28");

const pages = dv.pages(`"${folder}"`)
  .where(p => p.date && p.date >= startDate && p.date <= endDate && !p.file.name.includes("Dashboard"));

// ---------------- CATEGORIES ----------------
const categories = [
  { name: "Body", icon: "💪" },
  { name: "Mind", icon: "🧠" },
  { name: "Focus", icon: "🎯" },
  { name: "Spirit", icon: "✨" }
];

// ---------------- HABITS PER CATEGORY ----------------
const habitsMap = {
  Body: ["Exercise","Sleep","Healthy meals","Strength training","Walk outside","No junk food","Drink water"],
  Mind: ["Read","Learn something","Brain training","Review goals","Journal"],
  Focus: ["Deep work","No phone","No social media"],
  Spirit: ["Meditate","Tidy space","Creative work","Social connection","Call family"]
};

// ---------------- SCORE CALCULATION ----------------
const scores = categories.map(cat => {
  let possible = 0;
  let actual = 0;

  pages.forEach(p => {
    habitsMap[cat.name].forEach(h => {
      possible++;
      if (p.file.tasks?.some(t => t.text.includes(h) && t.completed)) {
        actual++;
      }
    });
  });

  return possible ? Math.round((actual / possible) * 100) : 0;
});

// ---------------- DOM ----------------
const radarId = "radar-" + Math.random().toString(36).slice(2);

this.container.innerHTML = `
<style>
@import url('https://fonts.googleapis.com/css2?family=Afacad:wght@400;500;600&display=swap');

.balance-wrapper {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.balance-title {
  font-family: 'Afacad', sans-serif;
  font-size: 16px;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: #888;
  margin-bottom: 30px;
}

.radar-container {
  position: relative;
  width: 400px;
  height: 400px;
}
</style>

<div class="balance-wrapper">
  <div class="balance-title">LIFE BALANCE ARCHITECTURE</div>
  <div class="radar-container">
    <canvas id="${radarId}"></canvas>
  </div>
</div>
`;

// ---------------- CHART ----------------
const runChart = () => {
  const canvas = document.getElementById(radarId);
  if (!canvas) return;

  const ctx = canvas.getContext("2d");

  new Chart(ctx, {
    type: "radar",
    data: {
      labels: categories.map(c => `${c.icon} ${c.name}`),
      datasets: [{
        data: scores,
        fill: true,
        backgroundColor: "rgba(255, 214, 10, 0.2)",
        borderColor: "#FFD60A",
        borderWidth: 3,
        pointRadius: 6,
        pointBackgroundColor: "#FFD60A",
        pointBorderColor: "#fff",
        pointBorderWidth: 2,
        pointHoverRadius: 8
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "rgba(20,20,20,0.95)",
          borderColor: "#FFD60A",
          borderWidth: 1,
          callbacks: {
            label: ctx => `${ctx.raw}% complete`
          }
        }
      },
      scales: {
        r: {
          min: 0,
          max: 100,
          ticks: {
            stepSize: 25,
            color: "#666",
            backdropColor: "transparent"
          },
          grid: { color: "rgba(255,255,255,0.1)" },
          angleLines: { color: "rgba(255,255,255,0.1)" },
          pointLabels: {
            color: "#FFD60A",
            font: { size: 14, weight: "600" }
          }
        }
      }
    }
  });
};

// ---------------- LOAD CHART.JS ----------------
if (!window.Chart) {
  const script = document.createElement("script");
  script.src = "https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js";
  script.onload = runChart;
  document.head.appendChild(script);
} else {
  runChart();
}
