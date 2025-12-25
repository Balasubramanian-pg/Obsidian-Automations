## Step 2: The Dashboard (Main Event)

Create a new note called `📊 Habit Dashboard` and paste this code:

```dataviewjs
// ============================================
// CONFIGURATION
// ============================================
const habitConfig = {
    booleanHabits: [
        { key: 'got_chia_seeds', label: 'Chia Seeds', color: '#10b981' },
        { key: 'cooked_dinner', label: 'Cooked Dinner', color: '#f59e0b' },
        { key: 'went_to_gym', label: 'Gym', color: '#ef4444' },
        { key: 'slept_before_1145', label: 'Sleep < 11:45pm', color: '#8b5cf6' }
    ],
    numericHabits: [
        { key: 'freelance_hours', label: 'Freelance Hours', color: '#3b82f6', target: 2 }
    ]
};

// ============================================
// UTILITY FUNCTIONS
// ============================================
function getDateRange(view, referenceDate = moment()) {
    const today = referenceDate.clone().startOf('day');
    
    switch(view) {
        case 'daily':
            return {
                start: today.clone().subtract(6, 'days'),
                end: today,
                format: 'MMM DD',
                days: 7
            };
        case 'weekly':
            return {
                start: today.clone().subtract(11, 'weeks').startOf('isoWeek'),
                end: today.clone().endOf('isoWeek'),
                format: 'MMM DD',
                days: 84
            };
        case 'monthly':
            return {
                start: today.clone().subtract(11, 'months').startOf('month'),
                end: today.clone().endOf('month'),
                format: 'MMM YYYY',
                days: 365
            };
    }
}

function getDailyNotes(startDate, endDate) {
    const pages = dv.pages('"Daily Notes"')
        .where(p => p.date && p.habits);
    
    const notes = [];
    let current = startDate.clone();
    
    while (current <= endDate) {
        const dateStr = current.format('YYYY-MM-DD');
        const page = pages.find(p => moment(p.date).format('YYYY-MM-DD') === dateStr);
        
        notes.push({
            date: current.clone(),
            habits: page?.habits || null,
            exists: !!page
        });
        
        current.add(1, 'day');
    }
    
    return notes;
}

function calculateStreak(notes, habitKey) {
    let currentStreak = 0;
    let maxStreak = 0;
    let tempStreak = 0;
    
    // Current streak (from today backwards)
    for (let i = notes.length - 1; i >= 0; i--) {
        if (!notes[i].exists) continue;
        
        const value = notes[i].habits?.[habitKey];
        if (typeof value === 'boolean' && value === true) {
            currentStreak++;
        } else if (typeof value === 'number' && value >= habitConfig.numericHabits.find(h => h.key === habitKey)?.target) {
            currentStreak++;
        } else {
            break;
        }
    }
    
    // Max streak (scan all)
    for (const note of notes) {
        if (!note.exists) continue;
        
        const value = note.habits?.[habitKey];
        let completed = false;
        
        if (typeof value === 'boolean' && value === true) {
            completed = true;
        } else if (typeof value === 'number' && value >= habitConfig.numericHabits.find(h => h.key === habitKey)?.target) {
            completed = true;
        }
        
        if (completed) {
            tempStreak++;
            maxStreak = Math.max(maxStreak, tempStreak);
        } else {
            tempStreak = 0;
        }
    }
    
    return { current: currentStreak, max: maxStreak };
}

function aggregateByPeriod(notes, period) {
    const groups = {};
    
    notes.forEach(note => {
        if (!note.exists) return;
        
        let key;
        if (period === 'week') {
            key = note.date.clone().startOf('isoWeek').format('YYYY-MM-DD');
        } else if (period === 'month') {
            key = note.date.clone().startOf('month').format('YYYY-MM');
        } else {
            key = note.date.format('YYYY-MM-DD');
        }
        
        if (!groups[key]) {
            groups[key] = { date: note.date.clone(), notes: [] };
        }
        groups[key].notes.push(note);
    });
    
    return Object.values(groups).map(group => ({
        date: group.date,
        habits: calculateAverages(group.notes)
    }));
}

function calculateAverages(notes) {
    const totals = {};
    const counts = {};
    
    habitConfig.booleanHabits.forEach(h => {
        totals[h.key] = 0;
        counts[h.key] = 0;
    });
    
    habitConfig.numericHabits.forEach(h => {
        totals[h.key] = 0;
        counts[h.key] = 0;
    });
    
    notes.forEach(note => {
        if (!note.habits) return;
        
        habitConfig.booleanHabits.forEach(h => {
            if (note.habits[h.key] === true) totals[h.key]++;
            counts[h.key]++;
        });
        
        habitConfig.numericHabits.forEach(h => {
            if (typeof note.habits[h.key] === 'number') {
                totals[h.key] += note.habits[h.key];
                counts[h.key]++;
            }
        });
    });
    
    const averages = {};
    Object.keys(totals).forEach(key => {
        averages[key] = counts[key] > 0 ? totals[key] / counts[key] : 0;
    });
    
    return averages;
}

// ============================================
// RENDER FUNCTIONS
// ============================================
function renderControls(currentView, container) {
    const controls = container.createDiv({ cls: 'habit-controls' });
    
    ['daily', 'weekly', 'monthly'].forEach(view => {
        const btn = controls.createEl('button', {
            text: view.charAt(0).toUpperCase() + view.slice(1),
            cls: view === currentView ? 'active' : ''
        });
        
        btn.onclick = () => {
            container.innerHTML = '';
            renderDashboard(view, container);
        };
    });
    
    return controls;
}

function renderStreaks(notes, container) {
    const streakContainer = container.createDiv({ cls: 'streak-container' });
    streakContainer.createEl('h3', { text: '🔥 Current Streaks' });
    
    const streakGrid = streakContainer.createDiv({ cls: 'streak-grid' });
    
    [...habitConfig.booleanHabits, ...habitConfig.numericHabits].forEach(habit => {
        const streak = calculateStreak(notes, habit.key);
        const card = streakGrid.createDiv({ cls: 'streak-card' });
        
        card.createEl('div', { text: habit.label, cls: 'streak-label' });
        card.createEl('div', { text: streak.current.toString(), cls: 'streak-current' });
        card.createEl('div', { text: `Best: ${streak.max}`, cls: 'streak-max' });
    });
}

function renderCharts(notes, view, container) {
    const range = getDateRange(view);
    let chartData = notes;
    
    if (view === 'weekly') {
        chartData = aggregateByPeriod(notes, 'week');
    } else if (view === 'monthly') {
        chartData = aggregateByPeriod(notes, 'month');
    }
    
    // Line Chart
    const lineChartContainer = container.createDiv({ cls: 'chart-container' });
    lineChartContainer.createEl('h3', { text: '📈 Habit Trends' });
    const lineCanvas = lineChartContainer.createEl('canvas');
    
    const labels = chartData.map(d => d.date.format(range.format));
    const datasets = [...habitConfig.booleanHabits, ...habitConfig.numericHabits].map(habit => ({
        label: habit.label,
        data: chartData.map(d => {
            const val = d.habits?.[habit.key];
            if (typeof val === 'boolean') return val ? 1 : 0;
            if (typeof val === 'number') return val;
            return 0;
        }),
        borderColor: habit.color,
        backgroundColor: habit.color + '20',
        tension: 0.4,
        fill: true
    }));
    
    new Chart(lineCanvas, {
        type: 'line',
        data: { labels, datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
    
    // Donut Chart - Completion Rate
    const donutContainer = container.createDiv({ cls: 'chart-container' });
    donutContainer.createEl('h3', { text: '🍩 Completion Rate' });
    const donutCanvas = donutContainer.createEl('canvas');
    
    const completionData = [...habitConfig.booleanHabits, ...habitConfig.numericHabits].map(habit => {
        const completed = notes.filter(n => {
            if (!n.exists || !n.habits) return false;
            const val = n.habits[habit.key];
            if (typeof val === 'boolean') return val === true;
            if (typeof val === 'number') {
                const target = habitConfig.numericHabits.find(h => h.key === habit.key)?.target || 0;
                return val >= target;
            }
            return false;
        }).length;
        
        return {
            label: habit.label,
            value: (completed / notes.filter(n => n.exists).length) * 100,
            color: habit.color
        };
    });
    
    new Chart(donutCanvas, {
        type: 'doughnut',
        data: {
            labels: completionData.map(d => d.label),
            datasets: [{
                data: completionData.map(d => d.value),
                backgroundColor: completionData.map(d => d.color)
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom' }
            }
        }
    });
}

function renderDashboard(view, container) {
    const range = getDateRange(view);
    const notes = getDailyNotes(range.start, range.end);
    
    renderControls(view, container);
    renderStreaks(notes, container);
    renderCharts(notes, view, container);
}

// ============================================
// INITIALIZE
// ============================================
const container = dv.container;
container.className = 'habit-dashboard';

// Add Chart.js if not already loaded
if (typeof Chart === 'undefined') {
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
    script.onload = () => renderDashboard('daily', container);
    document.head.appendChild(script);
} else {
    renderDashboard('daily', container);
}
```
