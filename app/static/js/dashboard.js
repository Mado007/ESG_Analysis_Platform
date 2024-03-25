async function fetchAndUpdateData() {
  try {
    const response = await fetch('/data');
    const data = await response.json();
    updateChart(data);
    updateTable(data);
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}

function updateChart(data) {
  // Implementation remains the same; consider using modern chart libraries or vanilla JS to update the chart
}

function updateTable(data) {
  // Similar approach; dynamically update your HTML table based on fetched data
}

document.addEventListener('DOMContentLoaded', () => {
  fetchAndUpdateData();
  setInterval(fetchAndUpdateData, 5000);
});
google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawVisualization);

      function drawVisualization() {
        // Some raw data (not necessarily accurate)
        var data = google.visualization.arrayToDataTable([
          ['Month', 'Bolivia', 'Ecuador', 'Madagascar', 'Papua New Guinea', 'Rwanda', 'Average'],
          ['2020/05',  165,      938,         522,             998,           450,      614.6],
          ['2021/06',  135,      1120,        599,             1268,          288,      682],
          ['2022/07',  157,      1167,        587,             807,           397,      623],
          ['2023/08',  139,      1110,        615,             968,           215,      609.4],
        ]);

        var options = {
          title : 'Monthly Coffee Production by Country',
          vAxis: {title: 'Cups'},
          hAxis: {title: 'Month'},
          seriesType: 'bars',
          series: {5: {type: 'line'}}
        };

        var chart = new google.visualization.ComboChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }