"use strict";


// world map initialize function comes from 
// http://stackoverflow.com/questions/9893680/google-maps-api-v3-show-the-whole-world
function initialize () {

  var mapOptions = {
    center: new google.maps.LatLng(0, 0),
    zoom: 1,
    minZoom: 1
  };

  var map = new google.maps.Map(document.getElementById('map'),mapOptions );

  var allowedBounds = new google.maps.LatLngBounds(
    new google.maps.LatLng(85, -180), // top left corner of map
    new google.maps.LatLng(-85, 180)  // bottom right corner
  );

  var k = 5.0; 
  var n = allowedBounds .getNorthEast().lat() - k;
  var e = allowedBounds .getNorthEast().lng() - k;
  var s = allowedBounds .getSouthWest().lat() + k;
  var w = allowedBounds .getSouthWest().lng() + k;
  var neNew = new google.maps.LatLng( n, e );
  var swNew = new google.maps.LatLng( s, w );
  boundsNew = new google.maps.LatLngBounds( swNew, neNew );
  map.fitBounds(boundsNew);

}

google.maps.event.addDomListener(window, 'load', initialize);