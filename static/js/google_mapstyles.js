// adapted from https://snazzymaps.com/style/118/travel-countries

"use strict";

var landColor = "#F7F7FF"
var waterColor = "#CCCCCF"

var MAPSTYLES = 
  [{
    "featureType": "administrative",
    "elementType": "all",
    "stylers": [{
      "visibility": "off"
    }]
  }, {
    "featureType": "administrative.country",
    "elementType": "geometry.stroke",
    "stylers": [{
      "visibility": "on"
    }, {
      "color": landColor
    }, {
      "weight": 0.8
    }]
  }, {
    "featureType": "water",
    "elementType": "all",
    "stylers": [{
      "color": landColor
    }]
  }, {
    "featureType": "landscape",
    "elementType": "all",
    "stylers": [{
      "color": waterColor
    }]
  }, {
    "featureType": "poi",
    "elementType": "all",
    "stylers": [{
      "color": waterColor
    }]
  }, {
    "featureType": "road",
    "elementType": "all",
    "stylers": [{
      "visibility": "off"
    }]
  }, {
    "featureType": "transit",
    "elementType": "all",
    "stylers": [{
      "visibility": "off"
    }]
  }, {
    "featureType": "all",
    "elementType": "labels",
    "stylers": [{
      "visibility": "off"
    }]
  }
]
