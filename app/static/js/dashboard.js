// static/dashboard.js
let intervalId;

const fetchDataPeriodically = () => {
  if (intervalId) clearInterval(intervalId);
  fetchAndUpdateData();
  intervalId = setInterval(fetchAndUpdateData, 5000);
};

const pageVisibilityHandler = () => {
  if (document.visibilityState === 'visible') {
    fetchDataPeriodically();
  } else {
    clearInterval(intervalId);
  }
}

const fetchAndUpdateData = async () => {
  try {
    const response = await fetch('/data');
    // Add check for JSON response
    const contentType = response.headers.get("content-type");
    if (!response.ok || !contentType || !contentType.includes("application/json")) {
      throw new Error('Failed to fetch data');
    }
    const data = await response.json();

    if (!data) { // If data is empty, do not proceed.
      throw new Error('Data is not valid or empty');
    }

    // Guard clauses for the updateChart and updateTable methods, check if they both exist and are a function
    if (typeof updateChart === 'function') {
      updateChart(data);
    }
    if (typeof updateTable === 'function') {
      updateTable(data);
    }
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}

// Amended the 'DOMContentLoaded' event target to 'window'
window.addEventListener('DOMContentLoaded', fetchDataPeriodically);
document.addEventListener('visibilitychange', pageVisibilityHandler);
document.addEventListener('pagehide', () => {
  if (intervalId) clearInterval(intervalId);
});

// Do not execute chart related code if google.charts not defined
if (typeof google !== "undefined" && typeof google.charts !== "undefined") {
  google.charts.load('current', {'packages':['corechart']});
  google.charts.setOnLoadCallback(drawVisualization);
}
      function drawVisualization() {
        // Some raw data (not necessarily accurate)
        var data = google.visualization.arrayToDataTable([
          ['Month', 'China', 'United States', 'France', 'India', 'Canada', 'Average'],
          ['2020/05',  165,      938,         522,             998,           450,      614.6],
          ['2021/06',  135,      1300,        599,             1268,          288,      682],
          ['2022/07',  157,      1167,        587,             807,           397,      623],
          ['2023/08',  139,      1110,        615,             968,           215,      609.4],
        ]);

        var options = {
          title : 'CO2 Emissions by Country',
          vAxis: {title: 'CO2 Emissions'},
          hAxis: {title: 'Year/Month'},
          seriesType: 'bars',
          series: {5: {type: 'line'}}
        };

        var chart = new google.visualization.ComboChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
      
      // Pie Chart
      var data = [{
        type: "pie",
        values: [2, 3, 4, 4, 9],
        labels: ["China", "France", "India", "Canada", "United States"],
        textinfo: "label+percent",
        textposition: "outside",
        automargin: true
      }]
      
      var layout = {
        height: 400,
        width: 400,
        margin: {"t": 0, "b": 0, "l": 0, "r": 0, "u": 0},
        showlegend: false
        }
      
      Plotly.newPlot('myDiv', data, layout)