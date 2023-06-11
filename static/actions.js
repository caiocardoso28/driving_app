var map;
var markers = [];
      function initMap() {
        var myLatLng = {lat: 40.7128, lng: -74.0060}; // Set this to the desired initial location

        map = new google.maps.Map(document.getElementById('map'), {
          zoom: 5,
          center: myLatLng
        });

        // This event listener calls addMarker() when the map is clicked.
        google.maps.event.addListener(map, 'click', function(event) {
          addMarker(event.latLng);
        });
      }

      // Adds a marker to the map and pushes to the array.
      function addMarker(location) {
        var marker = new google.maps.Marker({
          position: location,
          map: map
        });
        markers.push({lat: location.lat(), lng: location.lng()});
        // Send a POST request to your Flask app
        fetch('http://192.168.86.104:5000/markers', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            lat: location.lat(),
            lng: location.lng(),
          }),
        })
      }

      function calculateRoute() {
        fetch('http://192.168.86.104:5000/create_route', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            coordinates: markers,
          }),
        })
        .then(response => response.json())
        .then(data => {
          const polyline = new google.maps.Polyline({
            path: google.maps.geometry.encoding.decodePath(data.polyline),
            strokeColor: '#ff0000',
            strokeOpacity: 1.0,
            strokeWeight: 3,
          });
          polyline.setMap(map);
        })
        .catch((error) => {
          console.error('Error:', error);
        });
        markers = []
      }

      function getRoute() {
        var id = document.getElementById('routeId').value;
        fetch(`http://192.168.86.104:5000/get_route/${id}`)
        .then(response => response.json())
        .then(data => {
          const polyline = new google.maps.Polyline({
            path: google.maps.geometry.encoding.decodePath(data.polyline),
            strokeColor: '#672e2e',
            strokeOpacity: 1.0,
            strokeWeight: 3,
          });
          console.log(data.waypoints)
          let startLattitude = parseFloat(data.start.split(",")[0])
          let startLongitude = parseFloat(data.start.split(",")[1])
          var marker_start = new google.maps.Marker({
            position: {lat: startLattitude, lng: startLongitude},
            map: map
            });
          let endLattitude = parseFloat(data.end.split(",")[0])
          let endLongitude = parseFloat(data.end.split(",")[1])
          var marker_end = new google.maps.Marker({
            position: {lat: endLattitude, lng: endLongitude},
            map: map
            });
          for (let i= 0; i < data.waypoints.length; i++) {
            let lat_num = parseFloat(data.waypoints[i].split(",")[0])
            let lng_num = parseFloat(data.waypoints[i].split(",")[1])
            let loc = {lat: lat_num, lng: lng_num}

            var marker = new google.maps.Marker({
            position: loc,
            map: map
            });


          }
          polyline.setMap(map);
        })
        .catch((error) => {
          console.error('Error:', error);
        });
      }

