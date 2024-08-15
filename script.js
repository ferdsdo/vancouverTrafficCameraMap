// 20:25:34 -> photo on website
// 20:35:35 -> time when photo appears
// website seems to update after 10 mins after the photo
// photos update every 5 mins on the half 
/* cool spots :
Boulevards and W 41st Ave
Anderson St and Lamey's Mill Rd
https://trafficcams.vancouver.ca/boundaryVanness.htm
*/
const map = new maplibregl.Map({
    container: 'map',
    style: {
        'id': 'raster',
        'version': 8,
        'name': 'Raster tiles',
        'center': [0, 0],
        'zoom': 0,
        'sources': {
            'raster-tiles': {
                'type': 'raster',
                'tiles': ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'],
                'tileSize': 256,
                'minzoom': 0,
                'maxzoom': 19
            }
        },
        'layers': [
            {
                'id': 'background',
                'type': 'background',
                'paint': {
                    'background-color': '#e0dfdf'
                }
            },
            {
                'id': 'simple-tiles',
                'type': 'raster',
                'source': 'raster-tiles'
            }
        ]
    },
    center: [-123.12051391364608, 49.28290750560059], // downtown Vancouver
    zoom: 13,
    // pitch: 40, // 3D view
    // bearing: 20,
    // antialias: true    
});

map.on('load', async () => {
    image = await map.loadImage('./cameraIcon.png')
    map.addImage('camera', image.data)
    const dataUrl = 'https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/web-cam-url-links/exports/geojson?lang=en'
    fetch(dataUrl).then(response => {
        return response.json()
    }).then(data => {
        map.addSource('FeatureCollection', {
            'type': 'geojson',
            'data': data
        })
        map.addLayer({
        'id':'FeatureCollection',
        'type': 'symbol',
        'source': 'FeatureCollection',
        'layout': {
            'icon-image': 'camera',
            'icon-size': 0.05,
            }
        })
    }) 
    // When a click event occurs on a feature in the places layer, open a popup at the
    // location of the feature, with description HTML from its properties.
    map.on('click', 'FeatureCollection', (e) => {
        const coordinates = e.features[0].geometry.coordinates.slice();
        const description = e.features[0].properties.url;
        const name = e.features[0].properties.name;
        const coords = e.features[0]._geometry.coordinates;

        // Ensure that if the map is zoomed out such that multiple
        // copies of the feature are visible, the popup appears
        // over the copy being pointed to.
        while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
            coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
        }

        new maplibregl.Popup()
            .setLngLat(coordinates)
            .setHTML(`<a href="${description}" target="_blank">${name}</a><br><a href="https://www.google.com/maps/search/?api=1&query=${coords[1]}%2C${coords[0]}" target="_blank">Google Maps Link</a>`)
            .addTo(map);
    });

    // Change the cursor to a pointer when the mouse is over the FeatureCollection layer.
    map.on('mouseenter', 'FeatureCollection', () => {
        map.getCanvas().style.cursor = 'pointer';
    });

    // Change it back to a pointer when it leaves.
    map.on('mouseleave', 'FeatureCollection', () => {
        map.getCanvas().style.cursor = '';
    });
});

// Geolocate user control
map.addControl(
    new maplibregl.GeolocateControl({
        positionOptions: {
            enableHighAccuracy: true
        },
        trackUserLocation: true
    })
);
function updateTime() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    const timeString = `${hours}:${minutes}:${seconds}`;
    document.getElementById('clock').textContent = timeString;

}

setInterval(updateTime, 1000);
updateTime();