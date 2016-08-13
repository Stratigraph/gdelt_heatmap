"use strict";

// global map
var map;

// show the parts of the world where most events take place (sorry Antarctica...)
function initialize () {

  var mapOptions = {
    center: new google.maps.LatLng(0, 0),
    zoomControl: false,
    streetViewControl: false,
    navigationControl: false,
    mapTypeControl: false,
    scaleControl: false,
    draggable: false,
  };


  map = new google.maps.Map(document.getElementById('map'), mapOptions);

  // world boundaries, skipping far north and far south
  // for east and west, start at 0 and go as far as the map will take you
  var worldBounds = new google.maps.LatLngBounds(
    new google.maps.LatLng(-20, 0), 
    new google.maps.LatLng(50, 0)
  );

  map.fitBounds(worldBounds);

}

google.maps.event.addDomListener(window, 'load', initialize);