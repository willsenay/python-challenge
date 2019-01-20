// Store our API endpoint inside queryUrl
var queryUrl = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson";

// Perform a GET request to the query URL
d3.json(queryUrl, function(data) {
  // Once we get a response, send the data.features object to the createFeatures function
  createFeatures(data.features);
});

function markerSize(mag) {
  return mag * 4;
};

function createFeatures(earthquakeData) {
  
  // Define a function we want to run once for each feature in the features array
  // Give each feature a popup describing the place and time of the earthquake
  function onEachFeature(feature, layer) {
    layer.bindPopup("<h3>" + feature.properties.place +
    "</h3><hr><p>" + new Date(feature.properties.time) + "</p>");
  }
  
  
  // Create a GeoJSON layer containing the features array on the earthquakeData object
  // Run the onEachFeature function once for each piece of data in the array
  var earthquakes = L.geoJSON(earthquakeData, {
    onEachFeature: onEachFeature,
    pointToLayer: function (geoJsonPoint, latlng) {
      
      // marker style details
      var geojsonMarkerOptions = {
        radius: markerSize(geoJsonPoint.properties.mag),
        fillColor: markerColor(geoJsonPoint.properties.mag),
        color: "#000",
        weight: 1,
        opacity: 1,
        fillOpacity: 0.8
      };
      
      return L.circleMarker(latlng, geojsonMarkerOptions);
    }
  });

  // Sending our earthquakes layer to the createMap function
  createMap(earthquakes);
}

function markerColor(mag) {
  if (mag > 5) {
    return '#f06b6b'
  } else if (mag > 4) {
    return '#f0a76b'
  } else if (mag > 3) {
    return '#f3ba4d'
  } else if (mag > 2) {
    return '#f3db4d'
  } else if (mag > 1) {
    return '#e1f34d'
  } else {
    return '#b7f34d'
  }
}

function createMap(earthquakes) {

  // Define streetmap and darkmap layers
  var streetmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.streets",
    accessToken: API_KEY
  });

  var darkmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.dark",
    accessToken: API_KEY
  });

  // Define a baseMaps object to hold our base layers
  var baseMaps = {
    "Street Map": streetmap,
    "Dark Map": darkmap
  };

  // Create overlay object to hold our overlay layer
  var overlayMaps = {
    Earthquakes: earthquakes
  };

  // Create our map, giving it the streetmap and earthquakes layers to display on load
  var myMap = L.map("map", {
    center: [
      37.09, -95.71
    ],
    zoom: 5,
    layers: [streetmap, earthquakes]
  });

  // Create a layer control
  // Pass in our baseMaps and overlayMaps
  // Add the layer control to the map
  L.control.layers(baseMaps, overlayMaps, {
    collapsed: false
  }).addTo(myMap);

  // legend
  var info = L.control({
    position: "bottomright"
  });

  info.onAdd = function() {
    
    var div = L.DomUtil.create('div', 'info legend');
    var limits = [0, 1, 2, 3, 4, 5];
    var colors = ['#b7f34d', '#e1f34d', '#f3db4d', '#f3ba4d', '#f0a76b', '#f06b6b'];
    var labels = [];
      
    div.innerHTML += "<h4 style='margin:4px'>Magnitude</h4>"

    limits.forEach(function(limit, index) {
      labels.push("<li style= 'background-color:  " + colors[index] + "' ></li>");
    });

    for (var i = 0; i < limits.length; i++) {
      i > 4 ? div.innerHTML += "<ul> " + limits[i] + "+&nbsp;" + "\t" + labels[i] + "</ul>" :
      div.innerHTML += "<ul>" + limits[i] + "-" + limits[i+1] + "\t" + labels[i] + "</ul>";
    }

    return div;
  };

  info.addTo(map);
};
