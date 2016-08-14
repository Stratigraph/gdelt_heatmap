"use strict";

var g

// javascript from https://www.toptal.com/javascript/a-map-to-perfection-using-d3-js-to-make-beautiful-web-maps
function make_map1() {
  var width = 900;
  var height = 600;

  var projection = d3.geo.mercator();

  var svg = d3.select("body").append("svg")
      .attr("width", width)
      .attr("height", height);
  var path = d3.geo.path()
      .projection(projection);
  g = svg.append("g");

  d3.json("https://gist.githubusercontent.com/d3noob/5193723/raw/6e1434b2c2de24aedde9bcfe35f6a267bd2c04f5/world-110m2.json", function(error, topology) {

    // this part adapted from https://bost.ocks.org/mike/bubble-map/

    // svg.append("path")
    //   .datum(topojson.feature(us, us.objects.nation))
    //   .attr("class", "land")
    //   .attr("d", path);

    // svg.append("path")
    //   .datum(topojson.mesh(us, us.objects.states, function(a, b) { return a !== b; }))
    //   .attr("class", "border border--state")
    //   .attr("d", path);


      g.selectAll("path")
        .data(topojson.object(topology, topology.objects.countries)
            .geometries)
      .enter()
        .append("path")
        .attr("d", path)
  });

  // documentation: https://github.com/d3/d3-geo/blob/master/README.md#geoCircle
  // d3.geoCircle().center([0,0]).radius(100);

  // our GeoJSON feature collection; eventually will get this from ajax
  var evts = { "type": "FeatureCollection",
    "features": [
      { "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [49.25, -123.133]},
        "properties": {"titles": ["Earls asks ranchers for forgiveness for 'dumb decision'"],
                      "urls": ["http://forums.canadiancontent.net/news/145556-earls-asks-ranchers-forgiveness-dumb.html+"],
                      "count": 1}
        }
      ]
    }



  // adapted from https://bost.ocks.org/mike/bubble-map/
  g.attr("class", "bubble")
    .selectAll("circle")
      .data(evts)
    .enter().append("circle")
      // translate function here taken from https://bost.ocks.org/mike/map/
      .attr("transform", function(evt) { return "translate(" + projection(evt.geometry.coordinates) + ")";; })
      .attr("r", function(evt) { return radius(evt.properties.count) * 1000; });


  // adapted from https://bost.ocks.org/mike/map/
//   svg.append("path")
//     .datum(topojson.feature(uk, uk.objects.places))
//     .attr("d", path)
//     .attr("class", "place");

// svg.selectAll(".place-label")
//     .data(topojson.feature(uk, uk.objects.places).features)
//   .enter().append("text")
//     .attr("class", "place-label")
//     .attr("transform", function(d) { return "translate(" + projection(d.geometry.coordinates) + ")"; })
//     .attr("dy", ".35em")
//     .text(function(d) { return d.properties.name; });

}

$(document).ready(make_map1);

// javascript from http://jsbin.com/nutawiboci/1/edit?html,js,output
function make_map2() {

      //basic map config with custom fills, mercator projection
      var map = new Datamap({
        scope: 'world',
        element: document.getElementById('container1'),
        projection: 'mercator',
        height: 500,
        fills: {
          defaultFill: '#f0af0a',
          lt50: 'rgba(0,244,244,0.9)',
          gt50: 'red'
        },
        
        data: {
          USA: {fillKey: 'lt50' },
          RUS: {fillKey: 'lt50' },
          CAN: {fillKey: 'lt50' },
          BRA: {fillKey: 'gt50' },
          ARG: {fillKey: 'gt50'},
          COL: {fillKey: 'gt50' },
          AUS: {fillKey: 'gt50' },
          ZAF: {fillKey: 'gt50' },
          MAD: {fillKey: 'gt50' }       
        }
      })

  map.bubbles([
   {name: 'Hot', latitude: 21.32, longitude: 5.32, radius: 10, fillKey: 'gt50'},
   {name: 'Chilly', latitude: -25.32, longitude: 120.32, radius: 18, fillKey: 'lt50'},
   {name: 'Hot again', latitude: 21.32, longitude: -84.32, radius: 8, fillKey: 'gt50'},

  ], {
   popupTemplate: function(geo, data) {
     return "<div class='hoverinfo'>It is " + data.name + "</div>";
   }
  });
}