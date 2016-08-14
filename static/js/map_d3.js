"use strict";

// javascript from https://www.toptal.com/javascript/a-map-to-perfection-using-d3-js-to-make-beautiful-web-maps
var width = 900;
var height = 600;

var projection = d3.geo.mercator();

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);
var path = d3.geo.path()
    .projection(projection);
var g = svg.append("g");

d3.json("https://gist.githubusercontent.com/d3noob/5193723/raw/6e1434b2c2de24aedde9bcfe35f6a267bd2c04f5/world-110m2.json", function(error, topology) {
    g.selectAll("path")
      .data(topojson.object(topology, topology.objects.countries)
          .geometries)
    .enter()
      .append("path")
      .attr("d", path)
});