// ==========================================================================
//  Intake vs adoption bar chart
// ==========================================================================
function renderReport1Chart() {
  const chartData = JSON.parse(document.getElementById("species-data").textContent);
  Chart.defaults.font.family = getComputedStyle(document.body).fontFamily; // same font as the site

  const chart = new Chart(document.getElementById("speciesChart"), {
    type: "bar",
    data: {
      labels: chartData.labels,
      datasets: [
        {label: "Taken in", data: chartData.intake, borderRadius: 6 },
        {label: "Adopted", data: chartData.adopted, borderRadius: 6 },
      ],
    },
    // Chart customizations 
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { ticks: {}, grid: { display: false } },
        y: { ticks: { precision: 0 }, grid: {}, beginAtZero: true, suggestedMax: 5 },
      },
      plugins: { legend: { labels: {} } },
    },
  });

  // Colors following from custom.css light/dark mode.
  function applyChartTheme() {
    const c = themeColors();
    chart.data.datasets[0].backgroundColor = c.primary;
    chart.data.datasets[1].backgroundColor = c.strong;
    chart.options.scales.x.ticks.color = c.text;
    chart.options.scales.y.ticks.color = c.text;
    chart.options.scales.y.grid.color = c.grid;
    chart.options.plugins.legend.labels.color = c.text;
    chart.update("none");
  }
  applyChartTheme();
  document.addEventListener("themechange", applyChartTheme);
}