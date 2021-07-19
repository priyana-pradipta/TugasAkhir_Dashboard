
    $(document).ready(function(){
        $('table').DataTable({
          "responsive": true,
          "autoWidth": true,
          "columnDefs": [{
              "targets": '_all',
              "defaultContent": ""
          }]
        });
    });
  
    jQuery( "#datetime_range" ).submit(function( event ) {
        timezone = jstz.determine();
        jQuery(".timezone").val(timezone.name());
    });

    $(window).resize(function() {
      if(this.resizeTO) clearTimeout(this.resizeTO);
      this.resizeTO = setTimeout(function() {
          $(this).trigger('resizeEnd');
      }, 500);
    });
    
    function drawChartTemp() {
  
      var data = new google.visualization.DataTable();
      data.addColumn('datetime', 'Waktu');
      data.addColumn('number', 'Temperatur');
      data.addRows(TempData);
    
      var options = {
        height: 563,
        interpolateNulls: true,
        hAxis: {
          title: "Waktu",
          format: 'dd-MMM-yyyy HH:mm' },
        vAxis: {
          title: 'Derajat (Celcius)'
        },
        title: 'Temperatur',
        curveType: 'function'  //none kalau mau flat
      };
    
      options.theme = 'material';
      var chart = new google.visualization.LineChart(document.getElementById('chart_temps'));
    
      chart.draw(data, options);
    
      }

    $(window).on('resizeEnd', function drawChartTemp() {
  
    var data = new google.visualization.DataTable();
    data.addColumn('datetime', 'Waktu');
    data.addColumn('number', 'Temperatur');
    data.addRows(TempData);
  
    var options = {
      height: 563,
      interpolateNulls: true,
      hAxis: {
        title: "Waktu",
        format: 'dd-MMM-yyyy HH:mm' },
      vAxis: {
        title: 'Derajat (Celcius)'
      },
      title: 'Temperatur',
      curveType: 'function'  //none kalau mau flat
    };
  
    options.theme = 'material';
    var chart = new google.visualization.LineChart(document.getElementById('chart_temps'));
  
    chart.draw(data, options);
  
    })
  
    function drawChartHum() {

      var data = new google.visualization.DataTable();
      data.addColumn('datetime', 'Waktu');
      data.addColumn('number', 'Kelembapan');
      data.addRows(HumData);
    
      var options = {
        height: 563,
        interpolateNulls: true,
        hAxis: {
          title: "Waktu",
          format: 'dd-MMM-yyyy HH:mm' },
        vAxis: {
          title: 'Persentase'
        },
        title: 'Kelembapan',
        curveType: 'function'  //none kalau misal pengen flat
      };
    
      options.theme = 'material';
      var chart = new google.visualization.LineChart(document.getElementById('chart_hums'));
    
      chart.draw(data, options);
    
      }

    $(window).on('resizeEnd', function drawChartHum() {

    var data = new google.visualization.DataTable();
    data.addColumn('datetime', 'Waktu');
    data.addColumn('number', 'Kelembapan');
    data.addRows(HumData);
  
    var options = {
      height: 563,
      interpolateNulls: true,
      hAxis: {
        title: "Waktu",
        format: 'dd-MMM-yyyy HH:mm' },
      vAxis: {
        title: 'Persentase'
      },
      title: 'Kelembapan',
      curveType: 'function'  //none kalau misal pengen flat
    };
  
    options.theme = 'material';
    var chart = new google.visualization.LineChart(document.getElementById('chart_hums'));
  
    chart.draw(data, options);
  
    })
  