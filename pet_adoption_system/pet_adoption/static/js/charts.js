// ==========================================================================
//  Helper functions
// ==========================================================================

// ==========================================================================
// Report 1: Intake vs Adoption Bar chart
// ==========================================================================
function renderReport1_Bar({canvasId, dataId}) {
    const chartData = JSON.parse(document.getElementById(dataId).textContent);
    Chart.defaults.font.family = getComputedStyle(document.body).fontFamily; // same font as the site
    const c = themeColors();

    const chart = new Chart(document.getElementById(canvasId), {
        type: "bar",
        data: {
            labels: chartData.labels,
            datasets: [
                {label: "Taken in", data: chartData.intake, borderRadius: 6, backgroundColor: c.bar_1},
                {label: "Adopted", data: chartData.adopted, borderRadius: 6, backgroundColor: c.bar_2},
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { ticks: { color: c.text }, grid: { display: false } },
                y: { ticks: { precision: 0, color: c.text }, grid: { color: c.grid }, beginAtZero: true, suggestedMax: 5 },
            },
            plugins: { colors: { enabled: false }, legend: { labels: { color: c.text } } },
        },
    });

    function applyChartTheme() {
        const c = themeColors();
        chart.data.datasets[0].backgroundColor = c.bar_1;
        chart.data.datasets[1].backgroundColor = c.bar_2;
        chart.options.scales.x.ticks.color = c.text;
        chart.options.scales.y.ticks.color = c.text;
        chart.options.scales.y.grid.color = c.grid;
        chart.options.plugins.legend.labels.color = c.text;
        chart.update("resize");
    }

    document.addEventListener("themechange", applyChartTheme);
}

// ==========================================================================
// Report 1: Intake and Adoption Donut charts 
// ==========================================================================
// Color constants (I got too lazy to put in custom.css again):
const DONUT_COLORS_LIGHT = ["#14706a", "#e3a14a", "#0f3d3a", "#5b8fc7", "#6dbdb3", "#d9826b"];
const DONUT_COLORS_DARK  = ["#5cc4bb", "#f0b45e", "#14706a", "#7aa8dc", "#a8dcd6", "#e6967f"];


// Helper: Donut maker 
function makeDonut(canvasId, dataId) {
    const chartData = JSON.parse(document.getElementById(dataId).textContent);
    const chart = new Chart(document.getElementById(canvasId), {
        type: "doughnut",
        data: {
            labels: chartData.labels,
            datasets: [{
                data: chartData.data,
                borderWidth: 0,
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: "bottom", labels: {} } },
        },
    });

    function applyChartTheme() {
        const c = themeColors();
        const isDark = document.documentElement.dataset.bsTheme === "dark";
        const palette = isDark ? DONUT_COLORS_DARK : DONUT_COLORS_LIGHT;

        const ds = chart.data.datasets[0];
        ds.backgroundColor = chartData.labels.map((_, i) => palette[i % palette.length]);
        ds.borderColor = getComputedStyle(document.documentElement).getPropertyValue("--bs-body-bg").trim();
        chart.options.plugins.legend.labels.color = c.text;
        chart.update("none");
    }

    applyChartTheme();
    document.addEventListener("themechange", applyChartTheme);
}

// Render the two donuts: 
function renderReport1_Donuts(donuts) {
    // (Canvas ID, data ID), set from HTML template
    donuts.forEach((d) => {
        makeDonut(d.canvasId, d.dataId);
    });
}