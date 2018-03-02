
// plot 4 
function plot4(plot04_data) {

    var data = [];
    for (i = 0; i < plot04_data.length; i++) { 
        data.push(plot04_data[i]);
    }
      console.log(data)
      var layout = {
            barmode: 'stack',
            title: 'Stacked Bar Chart: Percentage of Drafted Recruits (All States)',
            xaxis: {title: 'Star'},
            yaxis: {title: 'Percentage(%)'},
            legend: {"orientation": "h"}
    };
      Plotly.newPlot("plot4", data, layout);
}

var url = "/plot4";
function initPlot4() {
    Plotly.d3.json(url, function (error, data) { 
        var plot04_data = data;
        plot4(plot04_data);
    });
    
}

initPlot4();


// plot 3 
function plot3(plot03_data) {

      console.log(plot03_data);
      data = plot03_data
      var layout = {
 
        title: 'Pie Chart: Percentage of Drafted Recruits from all Players (about 8% Drafted)',

      };
      Plotly.newPlot("plot3", data, layout);
}

var url3 = "/plot3";
function initPlot3() {
    Plotly.d3.json(url3, function (error, data) { 
        var plot03_data = data;
        plot3(plot03_data);
    });
    
    
}

initPlot3();

// plot 2 
function plot2(plot02_data) {

    console.log(plot02_data);

    var mapbox = 'https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoia2pnMzEwIiwiYSI6ImNpdGRjbWhxdjAwNG0yb3A5b21jOXluZTUifQ.T6YbdDixkOBWH_k9GbS8JQ'

        var myMap = L.map('map', {
            center: [39.8283, -98.5795],
            zoom: 4
        });


        L.tileLayer(mapbox).addTo(myMap);

        var heatArray = plot02_data;
        console.log(heatArray)

        var heat = L.heatLayer(heatArray, {
            radius:10,
            blur: 2.5
        }).addTo(myMap)
}

var url = "/plot2";
function initPlot2() {
    Plotly.d3.json(url, function (error, data) { 
        var plot02_data = data;
        plot2(plot02_data);
    });
    
    
}

initPlot2();


// plot 1 
function plot1(plot01_data) {

    var data = [];
    for (i = 0; i < plot01_data.length; i++) { 
        data.push(plot01_data[i]);
    }
      console.log(data)
      var layout = {
          barmode: 'stack',
          title: 'Star (1 to 5) Stacked Bar Chart - Recruits Origin',
          xaxis: {title: 'Number of Players'},
          yaxis: {title: 'State of Origin'},
          legend: {"orientation": "v"}

        };
      Plotly.newPlot("plot1", data, layout);
}

var url = "/plot1";
function initPlot1() {
    Plotly.d3.json(url, function (error, data) { 
        var plot01_data = data;
        plot1(plot01_data);
    });
    
    
}

initPlot1();
