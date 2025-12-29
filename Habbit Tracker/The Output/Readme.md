The following are the further enhancements

```dataviewjs
const folder = "2. Daily Reflection";
const startDate = dv.date("2025-11-22");
const endDate = dv.date("2025-11-28");

// --- 1. DATA FETCHING ---
const pages = dv.pages(`"${folder}"`)
    .where(p => 
        p.date && 
        p.date >= startDate && 
        p.date <= endDate &&
        !p.file.name.includes("Dashboard")
    )
    .sort(p => p.date, 'asc');

const dailyStats = pages.map(p => {
    const total = p.file.tasks.length;
    const done = p.file.tasks.filter(t => t.completed).length;
    const progress = total > 0 ? Math.round((done / total) * 100) : 0;
    return {
        date: p.date.toFormat("dd-MM"),
        done: done,
        total: total,
        progress: progress
    };
}).values;

// --- 2. CALCULATE STATS ---
if (dailyStats.length === 0) {
    dv.paragraph("❌ No daily notes found!");
} else {
    // Average
    const avgProgress = Math.round(
        dailyStats.reduce((sum, d) => sum + d.progress, 0) / dailyStats.length
    );
    // Totals
    const totalDone = dailyStats.reduce((sum, d) => sum + d.done, 0);
    const totalTasks = dailyStats.reduce((sum, d) => sum + d.total, 0);
    
    // Best Day (Max Progress)
    const bestDay = dailyStats.reduce((best, d) => 
        d.progress > best.progress ? d : best
    );

    // Worst Day (Min Progress)
    const worstDay = dailyStats.reduce((worst, d) => 
        d.progress < worst.progress ? d : worst
    );

    // --- 3. ICONS (Yellow) ---
    const iconColor = "#FFD60A"; // Bright Yellow
    
    const iconCMake = `<svg viewBox="0 0 24 24" fill="${iconColor}" xmlns="http://www.w3.org/2000/svg" class="kpi-svg"><path d="M11.769.066L.067 23.206l12.76-10.843zM23.207 23.934L7.471 17.587 0 23.934zM24 23.736L12.298.463l1.719 19.24zM12.893 12.959l-5.025 4.298 5.62 2.248z"/></svg>`;
    
    const iconClaris = `<svg viewBox="0 0 24 24" fill="${iconColor}" xmlns="http://www.w3.org/2000/svg" class="kpi-svg"><path d="M11.56 0a3.34 3.34 0 00-.57.043L22.947 12 10.99 23.957c.132.022.307.043.57.043 6.626 0 12-5.375 12-12s-5.374-12-12-12zm-1.535 2.414C4.738 2.414.44 6.713.44 12s4.3 9.588 9.586 9.588c.264 0 .44-.023.57-.045L1.054 12l9.543-9.543a3.337 3.337 0 00-.57-.043zm.746 2.457c-.263 0-.438.021-.57.043L17.287 12l-7.086 7.086c.132.022.307.045.57.045 3.927 0 7.13-3.204 7.13-7.131s-3.203-7.129-7.13-7.129zm-.416 2.434A4.701 4.701 0 005.66 12a4.701 4.701 0 004.695 4.695c.264 0 .44-.023.57-.045L6.274 12l4.653-4.65a3.296 3.296 0 00-.57-.045Z"/></svg>`;
    
    const iconClubhouse = `<svg viewBox="0 0 24 24" fill="${iconColor}" xmlns="http://www.w3.org/2000/svg" class="kpi-svg"><path d="M24 9.543c0 .32-.23.763-.337.976-.39.833-1.03 2.112-1.03 3.585 0 3.213-1.135 4.811-2.023 5.628a5.706 5.706 0 0 1-3.852 1.527 6.144 6.144 0 0 1-3.32-.976c-1.366-.905-2.219-2.326-3.088-3.745-.692-1.153-1.171-2.06-1.918-3.816-.421-1.018-.813-2.012-1.15-3.094-.16-.514-.142-.905.053-1.153.195-.23.462-.337.78-.355.55-.018.764.373 1.083 1.384.195.639.586 1.563.816 2.077.302.621.728 1.455.923 1.74.16.25.302.32.461.32.284 0 .497-.16.497-.443 0-.16-.16-.426-.248-.586-.16-.302-.497-.905-.728-1.42a32.775 32.775 0 0 1-.763-1.917c-.142-.373-.301-.905-.461-1.437-.248-.816-.373-1.313-.373-1.687 0-.568.426-.94 1.065-.94.461 0 .763.23.958 1.064.16.763.444 2.006.852 2.982.266.639.656 1.492.887 1.918.142.248.301.461.301.55 0 .124-.23.32-.426.585-.124.16-.177.267-.177.39 0 .107.071.214.177.356.107.142.213.284.338.284.088 0 .142-.036.195-.107a6.12 6.12 0 0 1 1.847-1.563c.816-.461 1.651-.692 2.308-.834.319-.07.408-.142.408-.32 0-.212-.16-.336-.373-.354-.16-.018-.301 0-.55.018-.177.018-.266-.071-.372-.302-.32-.674-.94-1.811-1.313-3.266a13.95 13.95 0 0 1-.39-2.13c-.054-.391.017-.533.212-.71.249-.213.692-.302 1.03-.213.407.106.62.426.833 1.67.107.585.284 1.33.497 1.97.266.816.603 1.492 1.118 2.397.284.497.638 1.011 1.011 1.51-.071.213-.195.354-.603.692-.408.337-.816.692-1.189 1.348-.266.479-.39 1.011-.39 1.366 0 .337.07.408.284.408.372 0 .674-.07.692-.23.088-.64.195-1.047.55-1.528.212-.266.585-.603.887-.87.567-.46.763-.727.958-1.383.088-.302.195-.586.337-.852.337-.62.94-1.33 1.882-1.33.302 0 .55.088.71.337a.966.966 0 0 1 .124.479zM12.608 7.265c.16.658.355 1.226.55 1.723.23.605.497 1.12.87 1.811.177.337.265.337.691.107a9.14 9.14 0 0 1 1.207-.515c-.639-1.384-1.171-2.539-1.437-3.514a29.883 29.883 0 0 1-.39-1.918c-.054-.497-.107-.923-.231-1.384-.142-.568-.338-.834-.888-.834-.514 0-1.135.266-1.135.94 0 .444.124 1.1.248 1.631.213.516.249.835.515 1.953zm-7.484 7.147c-.43.116-2.276.784-2.721.957-.503.195-.857.372-.605 1.122.205.607.553.636.874.516.45-.166 2.442-1.21 2.818-1.442.34-.21.45-.37.29-.769-.145-.363-.354-.465-.656-.384zm-1.276-3.074c.252-.008.448-.09.508-.526.047-.335-.006-.51-.39-.629-.371-.114-2.702-.494-3.205-.542-.434-.042-.702 0-.753.687-.049.64.13.836.572.88.508.05 2.733.144 3.268.13zm-2.63-6.082c.474.283 2.293 1.385 2.906 1.579.306.096.468.01.64-.331s.218-.477-.111-.742c-.34-.274-2.123-1.661-2.628-1.924-.435-.226-.729-.139-.993.361-.299.566-.244.798.185 1.057z"/></svg>`;

    const iconCircuitVerse = `<svg viewBox="0 0 24 24" fill="${iconColor}" xmlns="http://www.w3.org/2000/svg" class="kpi-svg"><path d="M12.1227 24c-.201 0-.4037-.0058-.6028-.0175a.487.487 0 0 1-.0433-.287.703.703 0 0 0-.0213-.2624H9.2251a1.205 1.205 0 0 1-.785.3898.7059.7059 0 0 1-.5075-.2282.9153.9153 0 0 1-.0647-1.099.7.7 0 0 1 .5576-.267 1.2192 1.2192 0 0 1 .703.267h2.3271a1.9635 1.9635 0 0 0 0-.614h-1.1959a1.1416 1.1416 0 0 1-.5495-.1293c-.442-.2654-.9147-.522-1.4868-.808a1.3834 1.3834 0 0 0-.711-.194 7.1018 7.1018 0 0 1-.4752.0142c-.157 0-.313-.0036-.4644-.007a18.8307 18.8307 0 0 0-.45-.0072 1.3491 1.3491 0 0 1-.8135.3704.6752.6752 0 0 1-.512-.2411.7596.7596 0 0 1 0-1.0666.7188.7188 0 0 1 .5363-.2718 1.3055 1.3055 0 0 1 .7566.3364H7.771a1.1403 1.1403 0 0 1 .5495.1293c.1413.0824.2938.1616.4415.2389a6.0441 6.0441 0 0 1 .7544.4399 1.9496 1.9496 0 0 0 1.116.3293 2.542 2.542 0 0 0 .1772-.006 1.5207 1.5207 0 0 1 .2191-.0143c.0682 0 .1361.0032.208.0068.0797.004.1615.0078.2516.0078v-1.0343h-1.1639a1.267 1.267 0 0 1-.711.2993.8404.8404 0 0 1-.614-.3316c-.3709-.4043-.1346-.8032.1291-1.0666a.5653.5653 0 0 1 .3533-.125 1.3475 1.3475 0 0 1 .8426.4479h1.099v-.905a.3807.3807 0 0 0-.1778-.0404c-.027 0-.054.0019-.0824.0039-.0285.0019-.0624.0042-.0954.0042H4.959a.8404.8404 0 0 1-.7434-.3556c-.1716-.2285-.3698-.4592-.545-.6629l-.069-.0804c-.7435-.0647-.9698-.2845-.9375-.905a.7495.7495 0 0 1 .8404-.6788c.4916 0 .711.329.711 1.0666.0608.0708.12.1429.1827.2195.1357.1651.2757.3361.4315.492h6.6582a5.5024 5.5024 0 0 0 0-1.0344H6.6397a1.3177 1.3177 0 0 1-.7948.3707.6623.6623 0 0 1-.498-.2414.7457.7457 0 0 1 0-1.099.6933.6933 0 0 1 .508-.2685 1.1678 1.1678 0 0 1 .7201.3652h4.8806v-1.002h-8.242c-.156.1736-.3232.3494-.5016.5356-.1584.1661-.3213.3368-.5007.531a.8381.8381 0 0 1-.7912.7515.8055.8055 0 0 1-.1138-.008.8459.8459 0 0 1-.6464-1.002c.0588-.3827.372-.6022.8597-.6022a1.9283 1.9283 0 0 1 .2715.0204c.1765-.2062.4435-.5084.7111-.7757a.9587.9587 0 0 1 .7757-.3233h8.1774v-1.0989H1.6295a1.226 1.226 0 0 1-.7434.3436.6817.6817 0 0 1-.5494-.3113.8488.8488 0 0 1 .097-1.1312.7486.7486 0 0 1 .4793-.194 1.1539 1.1539 0 0 1 .8138.4849h3.1998l-.1014-.097c-.5595-.5284-1.1378-1.0747-1.8382-1.713a.7554.7554 0 0 1-.7757-.808c0-.514.2195-.7435.711-.7435.6617 0 .8404.2127.8728 1.0343.2482.238.4922.469.7508.7134.5417.5126 1.101 1.0414 1.6733 1.6138h5.236v-.7434H9.1605a1.2783 1.2783 0 0 1-.7049.2628.7457.7457 0 0 1-.588-.2951.808.808 0 0 1 .1294-1.099.6351.6351 0 0 1 .4373-.167 1.2777 1.2777 0 0 1 .8235.3933h2.198v-.8404c-.2264 0-.4526-.0036-.671-.007h-.0066a39.3709 39.3709 0 0 0-.656-.0072c-.2484 0-.4675.0048-.6705.0142a1.3974 1.3974 0 0 1-.1144.0048 1.2311 1.2311 0 0 1-.8552-.3603l-.6006-.5068-.0116-.01-.0078-.0066A260.83 260.83 0 0 0 6.6397 7.272H3.052a1.235 1.235 0 0 1-.7192.2909.7298.7298 0 0 1-.5737-.2909.7757.7757 0 0 1 .097-1.099.701.701 0 0 1 .4742-.2233 1.3556 1.3556 0 0 1 .8187.45h3.1352a1.599 1.599 0 0 1 1.1635.4525c.3733.3513.7951.6907 1.203 1.0187h.0016c.19.1532.388.3113.573.4664h2.198V7.2707c-.138 0-.2822-.0035-.4202-.007H11a17.915 17.915 0 0 0-.4392-.0072c-.1616 0-.3032.0048-.4286.0142a1.4155 1.4155 0 0 1-.1157.0049 1.3365 1.3365 0 0 1-.8558-.3265 11.3707 11.3707 0 0 0-.3048-.2405c-.1025-.0788-.212-.1616-.3093-.2443-.8-.0646-1.099-.2909-1.0667-.808a.7757.7757 0 0 1 .7758-.7434c.497 0 .7757.3018.808.8726.1293.097.2586.2033.388.3061l.0015.002c.1267.103.2585.2097.3878.3064h1.5838V5.1394h-.5495a1.3507 1.3507 0 0 1-.7654.3604.6872.6872 0 0 1-.5275-.296.7983.7983 0 0 1 .0324-1.099.6978.6978 0 0 1 .5003-.2146 1.1096 1.1096 0 0 1 .7586.3762h.5171a.5142.5142 0 0 0 .043-.3461 1.2334 1.2334 0 0 1-.0107-.1387v-.5171a3.1097 3.1097 0 0 1-.2908.0126c-.119 0-.2399-.0049-.3556-.0097h-.007a8.4163 8.4163 0 0 0-.364-.0104 1.9597 1.9597 0 0 0-1.0172.2344 10.704 10.704 0 0 1-1.115.5817h-.003c-.1538.0728-.3128.148-.466.2244a.8853.8853 0 0 1-.4202.0646H5.2188a1.0967 1.0967 0 0 1-.6958.3284.7822.7822 0 0 1-.5983-.3271.7237.7237 0 0 1-.181-.5453.8462.8462 0 0 1 .3103-.586.735.735 0 0 1 .4732-.1974 1.0705 1.0705 0 0 1 .755.456h2.101a.6167.6167 0 0 0 .2232-.053 1.192 1.192 0 0 1 .1322-.044c.1316-.0646.2628-.1292.3898-.1893a10.0788 10.0788 0 0 0 .9354-.4894 2.555 2.555 0 0 1 1.353-.3617c.0646 0 .1312.002.1981.0058a2.065 2.065 0 0 0 .2586.0143c.0853 0 .17-.0033.2586-.0068h.0023c.092-.0036.1874-.0075.286-.0075a2.1442 2.1442 0 0 0 .0365-.5908c-.0019-.0701-.0042-.1425-.0042-.2172H9.4164a1.4545 1.4545 0 0 1-.7663.3316.6823.6823 0 0 1-.5262-.2993.8307.8307 0 0 1 .0646-1.0989.715.715 0 0 1 .4874-.2043 1.243 1.243 0 0 1 .7758.3662h2.004c0-.0898.007-.1803.0144-.2763.0087-.1138.0178-.2314.0178-.3701h.126c4.196 0 7.4922 1.6423 9.7967 4.8805a12.2263 12.2263 0 0 1 2.408 6.4563c.1212 2.2033-.439 4.4571-1.6646 6.6986a11.395 11.395 0 0 1-4.4335 4.4768A11.4803 11.4803 0 0 1 12.1227 24zm.3672-5.5768v4.4604a1.616 1.616 0 0 0 .2705.0217 3.4704 3.4704 0 0 0 .491-.0456c.109-.0152.2204-.0323.337-.0407a14.979 14.979 0 0 0 2.392-4.3957zm4.6543 0a19.092 19.092 0 0 1-1.8424 3.9433 10.38 10.38 0 0 0 5.3008-3.9433zm1.0343-5.7855a20.4576 20.4576 0 0 1-.6788 4.6543h3.814a11.2114 11.2114 0 0 0 1.2928-4.6543zm-5.6886 0v4.622h3.8786a18.1495 18.1495 0 0 0 .6787-4.622zm.0323-5.7855v4.6542h4.5573a18.7193 18.7193 0 0 0-.711-4.6542zm4.9452-.0324a21.3593 21.3593 0 0 1 .711 4.6543h4.4281a10.9179 10.9179 0 0 0-1.3252-4.6543zm-2.1979-5.0421a20.007 20.007 0 0 1 1.8747 3.9432h3.4584a10.6137 10.6137 0 0 0-5.333-3.9432zm-2.7473-.5818c0 1.5624 0 3.0382.0323 4.4927h3.4584a.1183.1183 0 0 1-.0323-.097 16.2011 16.2011 0 0 0-2.2302-4.1048c-.0126-.0126-.0249-.0262-.0378-.0404a.2773.2773 0 0 0-.1884-.1212 9.487 9.487 0 0 0-1.002-.1293z"/></svg>`;

    // --- 4. RENDER LAYOUT ---
    const chartId = 'chart-' + Math.random().toString(36).substr(2, 9);
    const donutId = 'donut-' + Math.random().toString(36).substr(2, 9);
    
    // We create the element first and append it to Dataview container immediately
    const container = dv.el('div', '', {
        attr: { style: 'width: 100%;' }
    });
    
    container.innerHTML = `
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&display=swap');
            
            /* KPI CARDS STYLING */
            .kpi-container {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 20px;
                margin-bottom: 40px;
                font-family: 'Outfit', sans-serif;
            }
            .kpi-card {
                background-color: var(--background-secondary);
                border: 1px solid var(--background-modifier-border);
                border-radius: 12px;
                padding: 20px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }
            .kpi-icon-wrapper {
                margin-bottom: 12px;
                width: 40px;
                height: 40px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .kpi-svg {
                width: 32px;
                height: 32px;
            }
            .kpi-value {
                font-size: 28px;
                font-weight: 700;
                color: var(--text-normal);
                line-height: 1.2;
                margin-bottom: 4px;
            }
            .kpi-sub {
                font-size: 14px;
                font-weight: 500;
                color: var(--text-muted);
            }
            
            /* CHART STYLING */
            .charts-container {
                display: grid;
                grid-template-columns: 1fr 400px;
                gap: 40px;
                align-items: center;
                font-family: 'Outfit', sans-serif;
            }
            .chart-wrapper { width: 100%; height: 300px; position: relative; }
            .donut-wrapper { width: 100%; height: 300px; position: relative; }
            .donut-center-text {
                position: absolute;
                top: 50%; left: 50%;
                transform: translate(-50%, -50%);
                text-align: center;
                pointer-events: none;
            }
            .donut-percentage {
                font-size: 48px; font-weight: 700;
                color: #FFD60A; /* CHANGED TO YELLOW GOLD */
                line-height: 1;
            }
            .donut-label {
                font-size: 14px; font-weight: 500;
                color: rgba(156, 163, 175, 1); margin-top: 8px;
            }
            
            @media (max-width: 1000px) {
                .kpi-container { grid-template-columns: repeat(2, 1fr); }
            }
            @media (max-width: 768px) {
                .kpi-container { grid-template-columns: 1fr; }
                .charts-container { grid-template-columns: 1fr; }
            }
        </style>
        
        <!-- KPI SECTION -->
        <div class="kpi-container">
            <div class="kpi-card">
                <div class="kpi-icon-wrapper">${iconCMake}</div>
                <div class="kpi-value">${totalDone} / ${totalTasks}</div>
                <div class="kpi-sub">Total Habits Completed</div>
            </div>
            
            <div class="kpi-card">
                <div class="kpi-icon-wrapper">${iconClaris}</div>
                <div class="kpi-value">${avgProgress}%</div>
                <div class="kpi-sub">Average Daily Progress</div>
            </div>
            
            <div class="kpi-card">
                <div class="kpi-icon-wrapper">${iconClubhouse}</div>
                <div class="kpi-value">${bestDay.progress}%</div>
                <div class="kpi-sub">Best Day: ${bestDay.date}</div>
            </div>
            
            <div class="kpi-card">
                <div class="kpi-icon-wrapper">${iconCircuitVerse}</div>
                <div class="kpi-value">${worstDay.progress}%</div>
                <div class="kpi-sub">Worst Day: ${worstDay.date}</div>
            </div>
        </div>

        <!-- CHARTS SECTION -->
        <div class="charts-container">
            <div>
                <h3 style="font-family: 'Outfit', sans-serif; margin-bottom: 16px;">📈 Daily Tasks Completed</h3>
                <div class="chart-wrapper">
                    <canvas id="${chartId}"></canvas>
                </div>
            </div>
            
            <div>
                <h3 style="font-family: 'Outfit', sans-serif; margin-bottom: 16px;">🎯 Average Weekly Progress</h3>
                <div class="donut-wrapper">
                    <canvas id="${donutId}"></canvas>
                    <div class="donut-center-text">
                        <div class="donut-percentage">${avgProgress}%</div>
                        <div class="donut-label">Completed</div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // --- 5. INITIALIZE CHARTS ---
    const runCharts = () => setTimeout(createCharts, 100);

    if (!window.Chart) {
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js';
        script.onload = runCharts;
        document.head.appendChild(script);
    } else {
        runCharts();
    }
    
    function createCharts() {
        const ctx1 = document.getElementById(chartId);
        const ctx2 = document.getElementById(donutId);
        
        if (!ctx1 || !ctx2) return;

        new Chart(ctx1, {
            type: 'line',
            data: {
                labels: dailyStats.map(d => d.date),
                datasets: [{
                    label: 'Tasks Completed',
                    data: dailyStats.map(d => d.done),
                    fill: true,
                    // CHANGED: Light gold fill, Gold border
                    backgroundColor: 'rgba(255, 214, 10, 0.2)',
                    borderColor: '#FFD60A',
                    borderWidth: 2,
                    tension: 0.4,
                    pointRadius: 4,
                    pointBackgroundColor: '#FFD60A',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: { 
                    y: { 
                        beginAtZero: true,
                        grid: { display: false },
                        ticks: { font: { family: 'Outfit', size: 12 } }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { font: { family: 'Outfit', size: 12 } }
                    }
                }
            }
        });

        new Chart(ctx2, {
            type: 'doughnut',
            data: {
                labels: ['Completed', 'Remaining'],
                datasets: [{
                    data: [avgProgress, 100 - avgProgress],
                    // CHANGED: Gold for completed, Faint gold for remaining
                    backgroundColor: [
                        '#FFD60A',
                        'rgba(255, 214, 10, 0.1)'
                    ],
                    borderWidth: 0,
                    cutout: '75%'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: { enabled: false }
                }
            }
        });
    }
}
```

i need you to add borders to each kpi card and a golden yellow shadow (lightly do not over do it please) and also the shadow should come only on hover, keep it minimal
I want you to provide the same border and shadow to the area graph and the donut chart, also i want you to make the tool tip of the area graph to have afacad font please

And the two emojis used in the title of the graphs have to be replaced by this please

<svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><title>Hive</title><path d="M6.076 1.637a.103.103 0 00-.09.05L.014 11.95a.102.102 0 000 .104l6.039 10.26c.04.068.14.068.18 0l5.972-10.262a.102.102 0 00-.002-.104L6.166 1.687a.103.103 0 00-.09-.05zm2.863 0c-.079 0-.13.085-.09.154l5.186 8.967a.105.105 0 00.09.053h3.117c.08 0 .13-.088.09-.157l-5.186-8.966a.104.104 0 00-.09-.051H8.94zm5.891 0a.102.102 0 00-.088.154L20.656 12l-5.914 10.209a.102.102 0 00.088.154h3.123a.1.1 0 00.088-.05l5.945-10.262a.1.1 0 000-.102L18.041 1.688a.1.1 0 00-.088-.051H14.83zm-.79 11.7a.1.1 0 00-.089.052l-5.101 8.82c-.04.069.01.154.09.154h3.117a.104.104 0 00.09-.05l5.1-8.82a.103.103 0 00-.09-.155h-3.118z"/></svg>

<svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><title>Haxe</title><path d="M23.784 0a.221.221 0 0 0-.043.003h-5.853a.221.221 0 0 0-.1.023L12 2.918 6.21.026a.221.221 0 0 0-.098-.023H.238a.221.221 0 0 0-.026 0 .221.221 0 0 0-.21.256v5.853a.221.221 0 0 0 .024.1l2.894 5.785L.026 17.79a.221.221 0 0 0-.024.099v5.84a.221.221 0 0 0 .002.078.221.221 0 0 0 .253.19h5.855a.221.221 0 0 0 .099-.023L12 21.076l5.789 2.898a.221.221 0 0 0 .099.023h5.877a.221.221 0 0 0 .232-.257V17.89a.221.221 0 0 0-.023-.1l-2.895-5.792 2.895-5.786a.221.221 0 0 0 .023-.099V.267a.221.221 0 0 0-.005-.098.221.221 0 0 0-.208-.169zM2.022.445H6.06l4.038 2.017zm15.918 0h4.038l-8.075 2.017zM.528.528l11.039 2.76-8.28 8.275-.238-.953zM23.47.535l-2.76 11.031-8.277-8.279zm.084 1.487V6.06l-2.019 4.035zm-23.11.003L2.29 9.398l.175.7L.445 6.06zM12 3.48L20.52 12l-8.517 8.516-8.241-8.234L3.48 12zm8.712 8.952l.088.351 2.672 10.688-11.04-2.76zm-17.424 0l8.274 8.274L.531 23.46l.266-1.065zm18.247 1.466l2.02 4.042v4.027zm-19.07 0l-2.02 8.08v-4.038zm7.626 7.638l-4.032 2.018H2.02zm3.818 0l8.071 2.018h-4.04z"/></svg> (this is for the donut chart title and other icon is for the area graph okay do not confused my dear)

golden yellow color obviously 

Also be creative in rendering any needed animation for the area graph and donut chart upon hover please

## What will change and why

You already have a clean visual system. The request boils down to four controlled upgrades that stay tasteful and quiet:

* Add a visible border and a very light golden shadow that appears only on hover.
* Apply the same visual treatment to KPI cards, the area chart container, and the donut chart container.
* Replace the emoji titles with your provided SVG icons in gold.
* Use the Afacad font for the area chart tooltip and add subtle hover animations to both charts.

No logic changes, only styling and chart configuration.

---

## 1. KPI cards: border and hover-only golden shadow

You already have a border. We will refine it and add a hover shadow that uses gold but stays restrained.

### Replace the `.kpi-card` CSS with this

```css
.kpi-card {
    background-color: var(--background-secondary);
    border: 1px solid rgba(255, 214, 10, 0.35);
    border-radius: 12px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    box-shadow: none;
    transition:
        box-shadow 220ms ease,
        transform 220ms ease,
        border-color 220ms ease;
}

.kpi-card:hover {
    border-color: #FFD60A;
    box-shadow: 0 6px 18px rgba(255, 214, 10, 0.22);
    transform: translateY(-2px);
}
```

This keeps the default state flat and introduces a soft lift only on hover.

---

## 2. Chart containers: same border and hover behavior

We need a wrapper that visually behaves like a card.

### Add this CSS

```css
.chart-surface {
    background-color: var(--background-secondary);
    border: 1px solid rgba(255, 214, 10, 0.35);
    border-radius: 14px;
    padding: 20px;
    transition:
        box-shadow 220ms ease,
        transform 220ms ease,
        border-color 220ms ease;
}

.chart-surface:hover {
    border-color: #FFD60A;
    box-shadow: 0 6px 20px rgba(255, 214, 10, 0.24);
    transform: translateY(-2px);
}
```

### Wrap both charts in this container

Replace your chart section HTML with this structure:

```html
<div class="charts-container">
    <div class="chart-surface">
        <h3 class="chart-title">
            <span class="chart-icon">
                <!-- Hive SVG here -->
            </span>
            Daily Tasks Completed
        </h3>
        <div class="chart-wrapper">
            <canvas id="${chartId}"></canvas>
        </div>
    </div>

    <div class="chart-surface">
        <h3 class="chart-title">
            <span class="chart-icon">
                <!-- Haxe SVG here -->
            </span>
            Average Weekly Progress
        </h3>
        <div class="donut-wrapper">
            <canvas id="${donutId}"></canvas>
            <div class="donut-center-text">
                <div class="donut-percentage">${avgProgress}%</div>
                <div class="donut-label">Completed</div>
            </div>
        </div>
    </div>
</div>
```

---

## 3. SVG icons for chart titles in gold

### Add this CSS

```css
.chart-title {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 16px;
    font-family: 'Outfit', sans-serif;
    font-size: 16px;
    font-weight: 600;
}

.chart-icon svg {
    width: 22px;
    height: 22px;
    fill: #FFD60A;
}
```

### Insert your provided SVGs

* Hive SVG goes in the area graph title.
* Haxe SVG goes in the donut chart title.
* No emojis anywhere.

---

## 4. Afacad font for the area chart tooltip

### Load the font

Add this inside your `<style>` block:

```css
@import url('https://fonts.googleapis.com/css2?family=Afacad:wght@400;500;600&display=swap');
```

### Update the Chart.js tooltip configuration

Modify the **area chart** options:

```js
plugins: {
    legend: { display: false },
    tooltip: {
        enabled: true,
        backgroundColor: 'rgba(17, 17, 17, 0.9)',
        borderColor: '#FFD60A',
        borderWidth: 1,
        titleFont: {
            family: 'Afacad',
            size: 14,
            weight: '600'
        },
        bodyFont: {
            family: 'Afacad',
            size: 13,
            weight: '500'
        },
        padding: 10,
        cornerRadius: 10
    }
}
```

This affects only the area graph as requested.

---

## 5. Subtle hover animation for charts

### Area chart hover refinement

Inside the dataset:

```js
pointHoverRadius: 7,
pointHoverBorderWidth: 3
```

And add:

```js
hover: {
    mode: 'nearest',
    intersect: false
},
animation: {
    duration: 900,
    easing: 'easeOutQuart'
}
```

### Donut chart hover animation

Update the donut chart options:

```js
animation: {
    animateRotate: true,
    duration: 900,
    easing: 'easeOutQuart'
},
hoverOffset: 10
```

This gives a gentle expansion on hover without looking playful or loud.

---

## What was intentionally not changed

* No new colors introduced beyond your gold.
* No persistent shadows.
* No extra motion outside hover and initial render.
* No layout or data logic touched.

The result stays minimal, confident, and deliberate. The gold behaves like an accent, not a spotlight.


# Fixing the habbit dna
currently the items are not aligned and they look ugly too, can you help me change the entire code to provide dynamic, sleek, minimal ui 

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

// Split habits into 3 rows
const habitsPerRow = Math.ceil(habits.length / 3);
const rows = [
    habits.slice(0, habitsPerRow),
    habits.slice(habitsPerRow, habitsPerRow * 2),
    habits.slice(habitsPerRow * 2)
];

const container = dv.el('div', '', { 
    attr: { style: 'margin-bottom: 40px; background: var(--background-primary); padding: 0; overflow: hidden;' } 
});

let html = `
<style>
    .dna-container {
        display: flex;
        flex-direction: column;
        gap: 24px;
        max-width: 1200px;
        margin: 0 auto;
    }
    .dna-row {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(90px, 1fr));
        gap: 16px;
        justify-items: center;
    }
    .dna-strand {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        max-width: 90px;
    }
    .dna-label {
        font-family: 'Outfit', monospace;
        font-size: 11px;
        color: var(--text-muted);
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        white-space: nowrap;
        font-weight: 500;
    }
    .dna-sequence {
        display: flex;
        gap: 3px;
        background: var(--background-secondary);
        padding: 6px 8px;
        border-radius: 6px;
        border: 1px solid var(--background-modifier-border);
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .dna-bit {
        width: 10px;
        height: 20px;
        border-radius: 3px;
        background-color: var(--background-modifier-border);
        transition: all 0.2s ease;
    }
    .dna-bit.active {
        background-color: #FFD60A;
        box-shadow: 0 0 5px rgba(255, 214, 10, 0.5);
    }
    .dna-bit:hover {
        transform: scale(1.2);
    }
</style>
<h3 style="font-family: 'Outfit', sans-serif; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 2px; font-size: 12px; color: var(--text-muted);">Weekly DNA Fingerprint</h3>
<div class="dna-container">
`;

rows.forEach(row => {
    html += `<div class="dna-row">`;
    row.forEach(habit => {
        html += `<div class="dna-strand"><div class="dna-label">${habit.split(" ")[0]}</div><div class="dna-sequence">`;
        
        pages.forEach(p => {
            const isDone = p.file.tasks.some(t => t.text.includes(habit) && t.completed);
            html += `<div class="dna-bit ${isDone ? 'active' : ''}" title="${p.date.toFormat('EEE')}: ${habit}"></div>`;
        });
        
        html += `</div></div>`;
    });
    html += `</div>`;
});

html += `</div>`;
container.innerHTML = html;


I want you to use consistent padding for all rows and align all the boxes with each other

## Why it looks misaligned right now

Short, non-handwavy diagnosis before we fix it.

### Core layout problems

* You are splitting habits into **manual rows**. This guarantees misalignment because:

  * Each row has a different number of items.
  * Grid auto-fit recalculates widths per row.
* Each habit card has a **different label width**.
* The sequence container width is implicit, not fixed.
* Padding and gaps are defined in multiple places with different values.

Result: visually noisy, jagged edges, uneven rhythm.

The fix is not “tuning spacing”.
The fix is **changing the mental model** of the layout.

---

## New layout model (what we will do instead)

### Design principles

* One grid. Not three rows.
* Fixed-width habit cards.
* Fixed-width DNA sequence.
* Consistent vertical rhythm.
* Minimal glow, no visual clutter.
* Responsive without recalculating alignment.

### Visual outcome

* Every habit aligns perfectly.
* Rows auto-wrap cleanly.
* Boxes snap into a calm, modular system.
* Looks intentional, not improvised.

---

## Drop-in replacement code (fully rewritten)

You can replace your entire DataviewJS block with this.

```dataviewjs
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

const container = dv.el("div", "");

container.innerHTML = `
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600&display=swap');

.dna-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px 16px;
}

.dna-title {
  font-family: 'Outfit', sans-serif;
  font-size: 12px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 20px;
}

.dna-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 24px 20px;
  align-items: start;
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
  width: 100%;
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
  transition: transform 160ms ease, background-color 160ms ease;
}

.dna-bit.active {
  background: #FFD60A;
}

.dna-card:hover .dna-bit.active {
  transform: translateY(-2px);
}
</style>

<div class="dna-wrapper">
  <div class="dna-title">Weekly DNA Fingerprint</div>
  <div class="dna-grid">
    ${habits.map(habit => {
      const bits = pages.map(p => {
        const done = p.file.tasks.some(
          t => t.text.includes(habit) && t.completed
        );
        return `<div class="dna-bit ${done ? "active" : ""}"></div>`;
      }).join("");

      return `
        <div class="dna-card">
          <div class="dna-label">${habit}</div>
          <div class="dna-sequence">${bits}</div>
        </div>
      `;
    }).join("")}
  </div>
</div>
`;
```

---

## Why this version works

### Alignment is mathematically guaranteed

* One grid definition.
* Identical card width logic.
* Identical padding everywhere.
* No row-specific rules.

### Visual hierarchy is cleaner

* Labels are centered and consistent.
* DNA bars line up across the entire grid.
* No uneven shadows or accidental emphasis.

### Motion is restrained

* Only hover on the card.
* No jitter.
* No scale explosions.
* Gold is used as a signal, not decoration.

---

## If you want to go one level further later

Natural extensions that will fit this system cleanly:

* Week-over-week comparison toggle.
* Click a habit to open its daily breakdown.
* Animate bits left-to-right on load.
* Add a faint vertical rhythm grid in the background.

This structure will support all of that without collapsing.

Your instinct to call this “ugly” was correct.
It was not broken, it was under-structured.

## What we are adding

You want a **behavior-aware sort**, not cosmetic sorting.
The intent is clear and solid:

* Sort habits by **most achieved → least achieved**
* Toggle **ascending / descending**
* Keep the UI minimal and aligned with the current design system
* No layout breakage, no reflow chaos

This requires two things:

* Precompute a **completion score per habit**
* Re-render the grid when the sort mode changes

We will do this cleanly, without hacks.

---

## Sorting logic (concise explanation)

For each habit:

* Count how many days it was completed in the selected date range
* Store that as `score`
* Sort habits by `score`

  * Descending = most achieved first
  * Ascending = least achieved first

This is deterministic, fast, and visually meaningful.

---

## UI design for the controls

Top-right, subtle, not screaming “dashboard”:

* Two radio buttons
* Inline
* Muted by default
* Gold accent only when active

---

## Revised full DataviewJS code (drop-in replacement)

This replaces the previous version entirely.

```dataviewjs
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
```

---

## Why this revision stays clean

* No DOM hacks
* No layout shifts
* Sorting is data-driven, not visual
* Grid alignment is preserved
* UI controls are quiet and intentional

This now behaves like a **real analytical surface**, not a decorative widget.

If you want next-level polish later, the natural upgrades would be:

* Animated reordering (FLIP animation)
* Toggle between weekly and monthly windows
* Color intensity based on score density

But even without that, this is already production-grade Obsidian UI.

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

// Shorten names for the EQ labels (3-4 chars)
const shortNames = habits.map(h => h.substring(0, 3).toUpperCase());

// Calculate percentages
const data = habits.map(h => {
    const total = pages.length || 1;
    const completed = pages.filter(p => p.file.tasks.some(t => t.text.includes(h) && t.completed)).length;
    return Math.round((completed / total) * 10); // Scale 0-10 for 10 blocks
});

const container = dv.el('div', '', { 
    attr: { style: 'margin-bottom: 40px; background: var(--background-secondary); padding: 20px; border-radius: 12px; border: 1px solid var(--background-modifier-border);' } 
});

let html = `
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
    
    .synth-container {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        height: 180px;
        gap: 4px;
        padding-top: 20px;
        overflow-x: auto;
    }
    .synth-channel {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        min-width: 20px;
    }
    .synth-bar {
        display: flex;
        flex-direction: column-reverse;
        gap: 2px;
        margin-bottom: 8px;
    }
    .synth-led {
        width: 12px;
        height: 8px;
        background: var(--background-modifier-border);
        border-radius: 1px;
        opacity: 0.2;
        transition: all 0.3s ease;
    }
    .synth-led.active {
        opacity: 1;
        background: #FFD60A;
        box-shadow: 0 0 5px rgba(255, 214, 10, 0.6);
    }
    /* Make the top LEDs red/intense if 100% */
    .synth-led.active.peak {
        background: #FF5C5C;
        box-shadow: 0 0 8px rgba(255, 92, 92, 0.8);
    }
    .synth-label {
        font-family: 'Share Tech Mono', monospace;
        font-size: 9px;
        color: var(--text-muted);
        transform: rotate(-45deg);
        transform-origin: center;
        white-space: nowrap;
        margin-top: 5px;
    }
</style>
<h3 style="font-family: 'Outfit', sans-serif; margin-bottom: 0; text-transform: uppercase; letter-spacing: 2px; font-size: 12px; color: var(--text-muted);">Habit Frequency Response</h3>
<div class="synth-container">
`;

data.forEach((score, index) => {
    html += `<div class="synth-channel"><div class="synth-bar">`;
    
    // Create 10 LEDs
    for(let i=1; i<=10; i++) {
        const isActive = i <= score;
        const isPeak = i === 10; // Top block
        html += `<div class="synth-led ${isActive ? 'active' : ''} ${isActive && isPeak ? 'peak' : ''}"></div>`;
    }
    
    html += `</div><div class="synth-label" title="${habits[index]}">${shortNames[index]}</div></div>`;
});

html += `</div>`;
container.innerHTML = html;

i need to do the same for this as well, ALso can we make this more interactive with tooltips stating some important data point and making the shape a bit more thick currently it is so thin and also please ensure that the full name of the habbit is coming the fonts have to be afacad

<img width="1746" height="368" alt="image" src="https://github.com/user-attachments/assets/fa300411-d51f-427f-8d87-6040fd00f599" />
really good job but it has to be as wide as the page, and the entire habbit name has to come and like i told you no tooltip is coming yet

## What is actually going wrong (precise diagnosis)

You are very close. Two concrete issues are causing what you see:

### 1. Width is constrained by design, not Obsidian

* The container is capped by `max-width` and horizontal padding.
* The channel `min-width` is small, so content clusters in the center instead of breathing across the page.

### 2. Tooltip exists but never appears

This is the key bug.

* The tooltip is positioned **above** the bar.
* The parent containers (`synth-container` and sometimes Obsidian callouts) clip overflow.
* Result: tooltip renders but is clipped out of view.

This is a classic UI mistake. Nothing “mystical” is broken.

---

## Design corrections we will apply

### Layout

* Remove all max-width constraints.
* Let the chart stretch edge-to-edge.
* Distribute channels evenly across available width.
* Preserve scroll only if screen is extremely narrow.

### Labels

* Show **full habit names** under each bar.
* Wrap gracefully to two lines if needed.
* Afacad everywhere, no exceptions.

### Tooltips

* Move tooltip **inside the card**, not above it.
* Render tooltip **below the bar**, centered.
* Ensure no overflow clipping.
* Fade + lift animation, minimal.

---

## Fully corrected and refined code (drop-in replacement)

Replace your entire block with this.

```dataviewjs
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

// Compute stats
const stats = habits.map(habit => {
  const totalDays = pages.length || 1;
  const completedDays = pages.filter(p =>
    p.file.tasks.some(t => t.text.includes(habit) && t.completed)
  ).length;

  return {
    name: habit,
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

.synth-title {
  font-family: 'Afacad', sans-serif;
  font-size: 12px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 22px;
}

/* FULL-WIDTH DISTRIBUTION */
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
  position: relative;
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

/* FULL NAME LABEL */
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

/* TOOLTIP (NOW VISIBLE) */
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
  <div class="synth-title">Habit Frequency Response</div>

  <div class="synth-container">
    ${stats.map(stat => {
      const leds = Array.from({ length: 10 }, (_, i) => {
        const active = i < stat.level;
        const peak = i === 9 && active;
        return `<div class="synth-led ${active ? "active" : ""} ${peak ? "peak" : ""}"></div>`;
      }).join("");

      return `
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
      `;
    }).join("")}
  </div>
</div>
`;
```

---

## What is now fixed, explicitly

### Width

* Uses full available page width.
* No artificial centering.
* Channels distribute evenly.

### Labels

* Full habit names always visible.
* Clean wrapping.
* Afacad everywhere.

### Tooltips

* Now **actually visible**.
* Not clipped.
* Smooth fade and lift.
* Shows real data, not fluff.

---

## Why this version feels “right”

You now have:

* A spatially honest layout.
* Clear information density.
* No hidden elements.
* No accidental constraints.
* A visual system that scales with content.

This is no longer a “visualization”.
It is an **instrument**.

If you want the next refinement later, the correct next step would be:

* Sorting by frequency (like your DNA grid)
* Click-to-filter daily notes
* Month-level aggregation toggle

But for now, this version is structurally sound and aesthetically resolved.

amazing amazing work, now like we did we need two radio buttons, sort ascending and sort descending and a default view, can you make that happen
