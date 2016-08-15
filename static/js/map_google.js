"use strict";

// global map
var map;

// global markers array
var markers = [];

// global events data
var events;

function initialize () {

  drawMap();
  getData();

}

function drawMap() {

  // show the parts of the world where most events take place (sorry Antarctica...)
  var mapOptions = {
    center: new google.maps.LatLng(0, 0),
    streetViewControl: false,
    navigationControl: false,
    mapTypeControl: false,
    scaleControl: false,
    styles: MAPSTYLES,
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


// response function on ajax call to get event data
function getData() {

  $.get('events.json', function(response) {

  // set global variable
  events = response.events;

  // get min and max timestamp and apply to slider
  var minTimestamp = response.min;
  var maxTimestamp = response.max;

  // set slider to min timestamp
  setSlider(minTimestamp, maxTimestamp);

  });
}

function plotEvents(timestamp) {

  // clear all the previous markers
  for (var i=0; i < markers.length; i++) {
    markers[i].setMap(null)
  }

  // reset the markers array
  markers = []

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


  // iterate over keys of js object
  // events is global variable set in ajax callback processEvents
  var todays_events = events[timestamp]
  for(var ltlngString in todays_events) {

    var marker, html

    var ltlng = todays_events[ltlngString]

    var apColor = 'red'
    var fgColor = 'blue'
    var markerScale = 8

    makeMarkers(apColor, ltlng.apEvts)
    makeMarkers(fgColor, ltlng.fgEvts)
  }

  // a function to make a marker for event data from a latlng
  function makeMarkers(markerColor, evts) {
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

      // add to global array so it can be erased later
      markers.push(marker);

      // Define the content of the infoWindow
      var links = ''
      for (var i=0; i < evts.length; i++) {

        // console.log("making marker for... ");
        // console.log(evts[i]);

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



function setSlider(minTimestamp, maxTimestamp) {

  var secondsInDay = 60 * 60 * 24

  // get the data and make the slider
  // https://jqueryui.com/slider/#steps

  $( function() {
    $( "#slider" ).slider({
      // numbers are too big for jquery slider -- must divide
      value: maxTimestamp/secondsInDay,
      min: minTimestamp/secondsInDay,
      max: maxTimestamp/secondsInDay,
      // step: 3600,
      slide: function(event, ui) {
        // parseint to account for rounding error
        sliderUpdate(parseInt(ui.value * secondsInDay));
      }
    });
    sliderUpdate(maxTimestamp);
  } );

}

function sliderUpdate(tstamp) {
  // things to do when the slider updates (or initializes)
  // update the map
  plotEvents(tstamp);

  // update the display
  $('#date').html(getDateString(tstamp));
}

function getDateString(tstamp) {
  // get a date string from the timestamp
  // adapted from http://stackoverflow.com/questions/847185/convert-a-unix-timestamp-to-time-in-javascript

  var a = new Date(tstamp * 1000);
  var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  var year = a.getFullYear();
  var month = months[a.getMonth()];
  var date = a.getDate();
  var dateString = date + ' ' + month + ' ' + year;
  return dateString;
}



google.maps.event.addDomListener(window, 'load', initialize);
