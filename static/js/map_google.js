"use strict";

// global map
var map;

// show the parts of the world where most events take place (sorry Antarctica...)
function initialize () {

  var mapOptions = {
    center: new google.maps.LatLng(0, 0),
    // zoomControl: false,
    streetViewControl: false,
    navigationControl: false,
    mapTypeControl: false,
    scaleControl: false,
    styles: MAPSTYLES,
    // draggable: false,
  };


  map = new google.maps.Map(document.getElementById('map'), mapOptions);

  // world boundaries, skipping far north and far south
  // for east and west, start at 0 and go as far as the map will take you
  var worldBounds = new google.maps.LatLngBounds(
    new google.maps.LatLng(-20, 0), 
    new google.maps.LatLng(50, 0)
  );

  map.fitBounds(worldBounds);

  // from google maps lecture demo 'bears.js'
  // Define global infoWindow
  // If you do this inside the loop where you retrieve the json,
  // the windows do not automatically close when a new marker is clicked
  // and you end up with a bunch of windows opened at the same time.
  // What this does is create one infowindow and we replace the content
  // inside for each marker.
  var infoWindow = new google.maps.InfoWindow({
      width: 150
  });


$.get('events.json', function (events) {
  // iterate over keys of js object
  for(var ltlngString in events) {
    var marker, html

    var ltlng = events[ltlngString]
    var fgCount = ltlng.fgEvts.length;
    var apCount = ltlng.apEvts.length;

    var apColor = 'red'
    var fgColor = 'blue'
    var markerScale = 0.5


    if (apCount) {
      makeMarker(apColor, ltlng.apEvts)
    }

    if (fgCount) {
      makeMarker(fgColor, ltlng.fgEvts)
    }


    function makeMarker(markerColor, evts) {
      // from http://stackoverflow.com/questions/11162740/where-i-can-find-the-little-red-dot-image-used-in-google-map
      var circle = {
        path: google.maps.SymbolPath.CIRCLE,      
        fillColor: markerColor,
        fillOpacity: 0.4,
        scale: markerScale * evts.length,
        strokeColor: 'white',
        strokeWeight: 1
      };
           // Define the marker
          marker = new google.maps.Marker({
              position: new google.maps.LatLng(ltlng.lat, ltlng.lng),
              map: map,
              // title: evt.titles[0],
              icon: circle
          });

          // Define the content of the infoWindow
          var links = ''
          for (var i=0; i < evts.length; i++) {
            links += '<p><a target="blank" href="';
            links += evts[i].url;
            links += '">';
            links += evts[i].title;
            links += '</a></p>';
          }
          html = (
              '<div class="window-content">' +
                links + 
              '</div>');

          // Inside the loop we call bindInfoWindow passing it the marker,
          // map, infoWindow and contentString
          bindInfoWindow(marker, map, infoWindow, html);
      }
    }

  });

    // from google maps lecture demo 'bears.js'
  // This function is outside the for loop.
  // When a marker is clicked it closes any currently open infowindows
  // Sets the content for the new marker with the content passed through
  // then it open the infoWindow with the new content on the marker that's clicked
  function bindInfoWindow(marker, map, infoWindow, html) {
      google.maps.event.addListener(marker, 'click', function () {
          infoWindow.close();
          infoWindow.setContent(html);
          infoWindow.open(map, marker);
      });
  }


}

// get events and draw on map



google.maps.event.addDomListener(window, 'load', initialize);
