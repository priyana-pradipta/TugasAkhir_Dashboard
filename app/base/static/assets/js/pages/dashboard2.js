/* global Chart:false */

$(document).ready(function(){
  $('table').DataTable({
    "paging": false,
    "lengthChange": false,
    "searching": false,
    "ordering": true,
    "info": true,
    "autoWidth": true,
    "responsive": true,
    "columnDefs": [{
        "targets": '_all',
        "defaultContent": ""
    }]
  });
});

$(function () {
  var ticksStyle = {
    fontColor: '#495057',
    fontStyle: 'bold'
  }
  var mode = 'index'
  var intersect = true


  var PluginHum =  {
    beforeInit: function(chart) {
      var data1 = chart.config.data;
      for (var i = 0; i < HumData.length; i++) {
        dataHum.labels.push(HumData[i][0]);
          dataHum.datasets[0].data.push(HumData[i][1]);
      }
    }
  };

  var PluginTemp =  {
        beforeInit: function(chart) {
          var data = chart.config.data;
          for (var i = 0; i < TempData.length; i++) {
            dataTemp.labels.push(TempData[i][0]);
              dataTemp.datasets[0].data.push(TempData[i][1]);
          }
        }
  };

  var PluginUp =  {
        beforeInit: function(chart) {
          var data1 = chart.config.data;
          for (var i = 0; i < UptimeData.length; i++) {
            dataUptime.labels.push(UptimeData[i][0]);
              dataUptime.datasets[0].data.push(UptimeData[i][1]);
          }
        }
  };
  
  var ctx = document.getElementById("hum-chart");
  var cty = document.getElementById("temp-chart");
  var ctz = document.getElementById("uptime-chart");

  // eslint-disable-next-line no-unused-vars
  var dataHum = {
      labels: [],
      datasets: [{
        type: 'line',
        data: [],
        backgroundColor: 'transparent',
        spanGaps: false,
        borderColor: '#007bff',
        pointBorderColor: '#007bff',
        pointBackgroundColor: '#007bff',
        fill: false,
        pointHoverBackgroundColor: '#007bff',
        pointHoverBorderColor    : '#007bff'
      }]
    };

  var dataTemp = {
      labels: [],
      datasets: [{
        type: 'line',
        data: [],
        backgroundColor: 'transparent',
        spanGaps: false,
        borderColor: '#007bff',
        pointBorderColor: '#007bff',
        pointBackgroundColor: '#007bff',
        fill: false,
        pointHoverBackgroundColor: '#007bff',
        pointHoverBorderColor    : '#007bff'
      }]
   };


  var dataUptime = {
    labels: [],
    datasets: [{
      type: 'line',
      data: [],
      backgroundColor: 'transparent',
      borderColor: '#007bff',
      pointBorderColor: '#007bff',
      pointBackgroundColor: '#007bff',
      fill: false
      // pointHoverBackgroundColor: '#007bff',
      // pointHoverBorderColor    : '#007bff'
    }]
  };

  var hum_chart = new Chart(ctx, {
    plugins: [PluginHum],
    data: dataHum,
    options: {
      maintainAspectRatio: false,
      responsive: true,
      tooltips: {
        mode: mode,
        intersect: intersect
      },
      hover: {
        mode: mode,
        intersect: intersect
      },
      legend: {
        display: false
      },
      scales: {
        yAxes: [{
          // display: false,
          gridLines: {
            display: true,
            lineWidth: '4px',
            color: 'rgba(0, 0, 0, .2)',
            zeroLineColor: 'transparent'
          },
          ticks: $.extend({
            beginAtZero: true,
            suggestedMax: 100
          }, ticksStyle),
          suggestedMax: 100
        }],
        xAxes: [{
          display: true,
          type: 'time',
          time: {
            parser: 'YYYY-MM-DD HH:mm:ss',
            // round: 'day'                                                                                                                                                                            
            tooltipFormat: 'YYYY-MM-DD HH:mm:ss',
            displayFormats: {
                millisecond: 'HH:mm:ss.SSS',
                second: 'MMM-DD HH:mm:ss',
                minute: 'MMM-DD HH:mm',
                hour: 'MMM-DD HH:mm',
                day: 'MMM-DD HH:mm',
                week: 'MMM-DD HH',
                month: 'MMM-DD HH'
            }
          }
        }]
      }
    }
  });

  var temp_chart = new Chart(cty, {
    plugins: [PluginTemp],
    data: dataTemp,
    options: {
      maintainAspectRatio: false,
      responsive: true,
      tooltips: {
        mode: mode,
        intersect: intersect
      },
      hover: {
        mode: mode,
        intersect: intersect
      },
      legend: {
        display: false
      },
      scales: {
        yAxes: [{
          // display: false,
          gridLines: {
            display: true,
            lineWidth: '4px',
            color: 'rgba(0, 0, 0, .2)',
            zeroLineColor: 'transparent'
          },
          ticks: $.extend({
            beginAtZero: true,
            suggestedMax: 100
          }, ticksStyle),
          suggestedMax: 100
        }],
        xAxes: [{
          display: true,
          type: 'time',
          time: {
            parser: 'YYYY-MM-DD HH:mm:ss',
            // round: 'day'                                                                                                                                                                            
            tooltipFormat: 'YYYY-MM-DD HH:mm:ss',
            displayFormats: {
                millisecond: 'HH:mm:ss.SSS',
                second: 'MMM-DD HH:mm:ss',
                minute: 'MMM-DD HH:mm',
                hour: 'MMM-DD HH:mm',
                day: 'MMM-DD HH:mm',
                week: 'MMM-DD HH',
                month: 'MMM-DD HH'
            }
          }
        }]
      }
    }
  });

  var uptime_chart = new Chart(ctz, {
    plugins: [PluginUp],
    data: dataUptime,
    options: {
      maintainAspectRatio: false,
      responsive: true,
      tooltips: {
        mode: mode,
        intersect: intersect
      },
      hover: {
        mode: mode,
        intersect: intersect
      },
      legend: {
        display: false
      },
      scales: {
        yAxes: [{
          // display: false,
          gridLines: {
            display: true,
            lineWidth: '4px',
            color: 'rgba(0, 0, 0, .2)',
            zeroLineColor: 'transparent'
          },
          ticks: $.extend({
            beginAtZero: true,
            suggestedMax: 100
          }, ticksStyle),
          suggestedMax: 100
        }],
        xAxes: [{
          display: true,
          type: 'time',
          time: {
            parser: 'YYYY-MM-DD HH:mm:ss',
            // round: 'day'                                                                                                                                                                            
            tooltipFormat: 'YYYY-MM-DD HH:mm:ss',
            displayFormats: {
                millisecond: 'HH:mm:ss.SSS',
                second: 'MMM-DD HH:mm:ss',
                minute: 'MMM-DD HH:mm',
                hour: 'MMM-DD HH:mm',
                day: 'MMM-DD HH:mm',
                week: 'MMM-DD HH',
                month: 'MMM-DD HH'
            }
          }
        }]
      }
    }
  });  
})


