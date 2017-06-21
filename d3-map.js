var periods = ["1986-2005", "2020-2039", "2040-2059", "2080-2099"];

// add any regions you'd like to this array to color them blue
// var highlight_regions = ['USA.9.317', 'IND.10.121.371'];
var highlight_regions = [];
var highlight_color = d3.rgb('#0000ff')

var excludes = ['CA-', 'ATA'];

var loaded_csv_data = {}
    baseWidth = 360,
    baseHeight = 173
    postData = {};

var grey = d3.rgb("#C3C3C3");

// define color scheme
var bins = [];
var color_palette = [];

var load_dataset = function(filepath, callback) {

  if (loaded_csv_data.hasOwnProperty(filepath)) {
    callback(loaded_csv_data[filepath])
  }

  loaded_csv_data[filepath] = {}

  d3.csv(filepath, function(error, data) {
    data.forEach(function(value, index) {

      loaded_csv_data[filepath][value['hierid']] = {
        '0.05': parseInt(value['0.05']),
        '0.5': parseInt(value['0.5']),
        '0.95': parseInt(value['0.95']),
        'index': index,
        'hierid': value['hierid']
      };
    });
    
    callback(loaded_csv_data[filepath])
  });
}


var div = d3.select("body").append("div")   
  .attr("class", "tooltip")               
  .style("opacity", 0)
  .attr("id", "tooltip");

var
  // regionalTopo = './topo/globalRegions.json'; // This is just the map json
    // regionalTopo = './topo/nyt_small_simplified.json'; // This is just the map json
  regionalTopo = './topo/new_shapefile.topo.json'; // This is just the map json

var svg = d3.select($('div.acf-map-generator__map-preview')[0])
  .append('svg')
  .attr("id", "globalmap")
  .attr("width", baseWidth)
  .attr("height", baseHeight);

var zoom = d3.zoom()
    .scaleExtent([1, 100])
    // .translateExtent([[-100, -100], [baseWidth, baseHeight]])
    .on("zoom", zoomed);

var g = svg.append("g");

d3.json(regionalTopo, function(error, map) {
  if (error) throw error;
  var projection = d3.geoEquirectangular()
    .scale(baseWidth / 2 / Math.PI)
    .translate([0, 0]),
    path = d3.geoPath().projection(projection);

  svg
    .attr('width', baseWidth)
    .attr('height', baseHeight)
    .attr('viewBox', baseWidth / -2 + ' ' + baseHeight / -2 + ' ' + baseWidth + ' ' + baseHeight);

  g
    .attr("class", "regions")
    .selectAll("path")
    .data(topojson.feature(map, map.objects.cil3).features)
    .enter().append("path")
    .attr("fill", function(d) { 
        if (excludes.indexOf(d.properties.hierid.substring(0, 3)) > -1) {
            return "#fff";
        } else {
            return "#bdbdbd";
        }
      })
    .attr("d", path);


  // var legend = svg.append("g")
  //   .attr("transform", "translate (-170,-40)")
  //   .attr("class", "legend")
  //   .attr("id", "legend");

  setTimeout(refreshMap, 0.01);

});


svg
    .call(zoom);


function zoomed() {
  g.attr("transform", d3.event.transform);
}


var refreshMap = function() {

  var
    globalPercentileSelect = document.getElementById("global-dataset-percentile-list"),
    global_combo_variable = document.getElementById("combobox-variable"),
    global_combo_relative = document.getElementById("combobox-relative");
    global_combo_scenario = document.getElementById("global-scenario");
    global_slider_period = document.getElementById("period-slider");

  // Get selected dataset
  var selectedGlobalPercentile = globalPercentileSelect.value,
      selected_variable = global_combo_variable.value,
      selected_relative = global_combo_relative.value,
      selected_scenario = global_combo_scenario.value,
      selected_period = periods[global_slider_period.value];

  var filepath_unit,
    unit_name;

  if (selected_variable == 'tasmin-under-32F') {
    filepath_unit = 'days-under-32F';
    unit_name = ['Count of', 'days'];
  } else if (selected_variable == 'tasmax-over-95F') {
    filepath_unit = 'days-over-95F';
    unit_name = ['Count of', 'days'];
  } else {
    filepath_unit = 'degF';
    unit_name = ['Temperature', 'bins'];
  }

  var selectedGlobalDataset = (
        "./csv/global_hierid_"
        + selected_variable
        + "_" + selected_scenario
        + "_" + selected_period
        + "_" + selected_relative
        + "_" + filepath_unit
        + "_percentiles.csv");

  var formatFile = (
        "./color_palettes/"
        + selected_variable
        + "_" + selected_relative
        + ".json"
        // Prevent caching to allow file update
        + '?' + Math.floor(Math.random() * 1000));

  d3.json(formatFile, function(err, format) {
    if (err) throw err;

    // Map csv to something we like to use
    load_dataset(selectedGlobalDataset, function(preppedGlobalDataset) {

      // This is where we want to work
      bins = []

      format.bins.forEach(function(d, i) {bins.push(Number(d))});

      if (format.color_palette !== undefined) {

        // just use the color palette given if defined
        color_palette = format.color_palette;

      } else if (format.diverging === true) { 

          // build a diverging color scheme using two colors in "color_scheme"

          // this is the array we use in our color function
          color_palette = [];

          // first half
          var
            color_scheme = d3.scaleLinear().domain([1,bins.length/2-1])
              .interpolate(d3.interpolateLab)
              .range([d3.rgb(format.color_scheme[0]), grey]);

          for (var i = 0; i < (bins.length/2-1); i++) {
            color_palette.push(color_scheme(i));
          }

          // second half
          color_scheme = d3.scaleLinear().domain([bins.length/2, bins.length-1])
              .interpolate(d3.interpolateLab)
              .range([grey, d3.rgb(format.color_scheme[1])]);

          for (var i = bins.length/2; i < (bins.length-1); i++) {
            color_palette.push(color_scheme(i));
          }


      } else {

        if (format.color_scheme[0] === null) {
          format.color_scheme[0] = grey;
        }

        if (format.color_scheme[1] === null) {
          format.color_scheme[1] = grey;
        }

        // build an interpolated color scheme between colors in "color_scheme"
        var
          color_scheme = d3.scaleLinear().domain([1,bins.length])
            .interpolate(d3.interpolateLab)
            .range([d3.rgb(format.color_scheme[0]), d3.rgb(format.color_scheme[1])]);

        color_palette = [];

        for (var i = 0; i < bins.length-1; i++) {
          color_palette.push(color_scheme(i));
        }

      }

      
      var 
        color = d3.scaleThreshold()
          .domain(bins.slice(1, bins.length-1))
          .range(color_palette);


      svg
        .selectAll("path")
        .attr("fill", function(d) {
          if ( preppedGlobalDataset[d.properties.hierid] !== 'undefined' && preppedGlobalDataset[d.properties.hierid] !== undefined ) {
            // console.log( 'Found Region:', d.properties.hierid,  preppedGlobalDataset[d.properties.hierid]  );
            // If USA regions, ignore

            if (excludes.indexOf(d.properties.hierid.substring(0, 3)) > -1) {
                return "#fff";
            // } else if ( d.properties.hierid.substring(0, 3) === 'USA' ) {
            //   return '#bdbdbd';
            } else if (highlight_regions.indexOf(d.properties.hierid) > -1) {
              return highlight_color;
            } else {

              // console.log(preppedGlobalDataset[d.properties.hierid][selectedGlobalPercentile]);
              return color( preppedGlobalDataset[d.properties.hierid][selectedGlobalPercentile]  );

            }

          } else {
            // console.log( 'Missing Region: ', d.properties.hierid  );
            return '#bdbdbd';
          }
        })
        // .on('mouseover', function(d) {
        //   console.log('Region: ', d.properties);
        // });

        // ################################################
        // OnHover tooltip -- diagnostic tool
        // Should be deleted before going live
        // 
        // from http://bl.ocks.org/KoGor/5685876
        // ################################################
        
        //Adding mouseevents
        .on("mouseover", function(d) {
          if (excludes.indexOf(d.properties.hierid.substring(0, 3)) > -1) { return ;}
          div.transition().duration(100)
            .style("opacity", 1)
          div.text(preppedGlobalDataset[d.properties.hierid]['hierid'] + " : " + preppedGlobalDataset[d.properties.hierid][selectedGlobalPercentile])
            .style("left", (d3.event.pageX) + "px")
            .style("top", (d3.event.pageY -30) + "px");
        })
        .on("mouseout", function() {
          div.transition().duration(100)
          .style("opacity", 0);
        });

        // ################################################
        // End hover tooltip
        // ################################################
      

      // ################################################
      // MIKE DELGADO'S CODE
      // 
      // legend -- diagnostic tool
      // Should be deleted before going live
      // 
      // from http://bl.ocks.org/KoGor/5685876
      // ################################################
       
      //Adding legend for our Choropleth


      var boxmargin = 4,
        lineheight = 6;
        keyheight = 5,
        keywidth = 10,
        boxwidth = 1.5 * keywidth;

      var titleheight = unit_name.length*lineheight + boxmargin;

      var margin = { "left": 10, "top": 10 };

      var ranges = color.range().length;

      // make legend 
      // var legend = svg.select(document.getElementById("legend"));
          
      try {document.getElementById("legend").remove();} catch(err) {};
      // document.getElementById("legend-title").remove();
      // document.getElementById("legend-box").remove();
      // document.getElementById("legend-items").remove();
      var legend = svg.append("g")
          .attr("transform", "translate (-170,-40)")
          .attr("class", "legend")
          .attr("id", "legend");

      legend.selectAll("text")
          .data(unit_name)
          .enter().append("text")
          .attr("text-anchor", "middle")
          .attr("class", "legend-title")
          .attr("id", "legend-title")
          .attr("x",  keywidth + boxmargin)
          .attr("y", function(d, i) { return (i+1)*lineheight-2; })
          .text(function(d) { return d; })

      // make legend box 
      var lb = legend.append("rect")
          .attr("transform", "translate (0,"+titleheight+")")
          .attr("class", "legend-box")
          .attr("id", "legend-box")
          .attr("width", boxwidth)
          .attr("height", ranges*lineheight+2*boxmargin+lineheight-keyheight);

      // make quantized key legend items
      var li = legend.append("g")
          .attr("transform", "translate (8,"+(titleheight)+")")
          .attr("class", "legend-items")
          .attr("id", "legend-items");

      li.selectAll("rect")
          .data(color.range().map(function(thisColor) {
            var d = color.invertExtent(thisColor);
            if (d[0] == null) d[0] = color.domain()[0] - 1;
            if (d[1] == null) d[1] = color.domain()[1] + 1;
            return d;
          }))
          .enter().append("rect")
          .attr("y", function(d, i) { return i*lineheight+lineheight-keyheight; })
          .attr("width", keywidth)
          .attr("height", keyheight)
          .style("fill", function(d) { return color(d[0]); });
          
      li.selectAll("text")
          .data(color.domain())
          .enter().append("text")
          .attr("class", "legend-entry")
          .attr("x", keywidth + boxmargin)
          .attr("y", function(d, i) { return (i+1)*lineheight-2 + (lineheight*0.5); })
          .text(function(d) { return String(d); });

      // ################################################
      // End legend
      // ################################################

    });
  });
}; // End refreshMap

// Map generation
var globalPercentileSelect = document.getElementById("global-dataset-percentile-list");
globalPercentileSelect.onchange = function() {setTimeout(refreshMap, 0.01)};

var mapGenButton = document.getElementById("generate-map");
mapGenButton.onclick = function() {setTimeout(refreshMap, 0.01)};

var global_combo_variable = document.getElementById("combobox-variable");
global_combo_variable.onchange = function() {setTimeout(refreshMap, 0.01)};

var global_combo_relative = document.getElementById("combobox-relative");
global_combo_relative.onchange = function() {setTimeout(refreshMap, 0.01)};

var global_scenario = document.getElementById("global-scenario");
global_scenario.onchange = function() {setTimeout(refreshMap, 0.01)};

var global_slider_period = document.getElementById("period-slider");
var period_value = document.getElementById("period-value");
global_slider_period.onchange = function() {
  period_value.innerHTML = periods[global_slider_period.value].replace("_", " to ");
  setTimeout(refreshMap, 0.01)
};

function rgb2hex(rgb){
 rgb = rgb.match(/^rgba?[\s+]?\([\s+]?(\d+)[\s+]?,[\s+]?(\d+)[\s+]?,[\s+]?(\d+)[\s+]?/i);
 return (rgb && rgb.length === 4) ? "#" +
  ("0" + parseInt(rgb[1],10).toString(16)).slice(-2) +
  ("0" + parseInt(rgb[2],10).toString(16)).slice(-2) +
  ("0" + parseInt(rgb[3],10).toString(16)).slice(-2) : '';
}

var downloadPalette = document.getElementById('download-palette');
downloadPalette.onclick = function() {
  var body = JSON.stringify({
    bins: bins,
    color_palette: color_palette.map(rgb2hex)
  }, space=1);
  var link=document.createElement('a');
  document.body.appendChild(link);
  link.href=("data:application/octet-stream," + body);
  link.click();
}

