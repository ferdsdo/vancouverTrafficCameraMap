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
    toggleSidebar('right')
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
});

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
    // Update Sidebar content
    setPanelContent(e.features[0])
});

// Change the cursor to a pointer when the mouse is over the FeatureCollection layer.
map.on('mouseenter', 'FeatureCollection', () => {
    map.getCanvas().style.cursor = 'pointer';
});

// Change it back to a pointer when it leaves.
map.on('mouseleave', 'FeatureCollection', () => {
    map.getCanvas().style.cursor = '';
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

function toggleSidebar(id) {
    const elem = document.getElementById(id);
    const classes = elem.className.split(' ');
    const collapsed = classes.indexOf('collapsed') !== -1;

    const padding = {};

    if (collapsed) {
        // Remove the 'collapsed' class from the class list of the element, this sets it back to the expanded state.
        classes.splice(classes.indexOf('collapsed'), 1);

        padding[id] = 400; // In px, matches the width of the sidebars set in .sidebar CSS class
        map.easeTo({
            padding,
            duration: 1000 // In ms, CSS transition duration property for the sidebar matches this value
        });
    } else {
        padding[id] = 0;
        // Add the 'collapsed' class to the class list of the element
        classes.push('collapsed');

        map.easeTo({
            padding,
            duration: 1000
        });
    }

    // Update the class list on the element
    elem.className = classes.join(' ');
}

function setPanelContent(feature) {
    const tbody = document.querySelector("#tbody")
            tbody.innerHTML = "";
            // document.getElementById('jsonTable').innerHTML = ''
            document.getElementById('right-text').innerHTML = ''
            clickedGeoJson = sortGeoJSONFeatureProperties(feature) // make it so sidebar properties are sorted
            for (let key in clickedGeoJson.properties) {
                if (clickedGeoJson.properties.hasOwnProperty(key)) {

                    if(['geo_point_2d'].includes(key)) {
                        feature = JSON.parse(clickedGeoJson.properties[key])

                        const row = document.createElement('tr')

                        // Property name cell (not editable)
                        const propertyNameCell = document.createElement('td')
                        propertyNameCell.textContent = 'Link'
                        row.appendChild(propertyNameCell);
    
                        // Property value cell (editable input)
                        const propertyValueCell = document.createElement('td');
                        const propertyLinkCell = document.createElement('a');
                        propertyLinkCell.href = `https://www.google.com/maps/search/?api=1&query=${feature['lat']}%2C${feature['lon']}`;
                        propertyLinkCell.textContent = 'Google Maps Link';
                        propertyLinkCell.target = '_blank'; // Opens the link in a new tab
                        propertyValueCell.appendChild(propertyLinkCell)

                        row.appendChild(propertyValueCell);
                        tbody.appendChild(row);
                    } else if(['url'].includes(key)) {
                        feature = clickedGeoJson.properties[key]
                        const row = document.createElement('tr')

                        // Property name cell (not editable)
                        const propertyNameCell = document.createElement('td')
                        propertyNameCell.textContent = 'Link'
                        row.appendChild(propertyNameCell);
    
                        // Property value cell (editable input)
                        const propertyValueCell = document.createElement('td');
                        const propertyLinkCell = document.createElement('a');
                        propertyLinkCell.href = feature;
                        propertyLinkCell.textContent = 'City Map Url';
                        propertyLinkCell.target = '_blank'; // Opens the link in a new tab
                        propertyValueCell.appendChild(propertyLinkCell)

                        row.appendChild(propertyValueCell);
                        tbody.appendChild(row);
                    } else if(!['geo_local_area','mapid'].includes(key)){ // list of properties to hide
                        const row = document.createElement('tr')

                        // Property name cell (not editable)
                        const propertyNameCell = document.createElement('td')
                        propertyNameCell.textContent = key
                        row.appendChild(propertyNameCell);
    
                        // Property value cell (editable input)
                        const propertyValueCell = document.createElement('td');
                        propertyValueCell.textContent = clickedGeoJson.properties[key]
                        row.appendChild(propertyValueCell);
    
                        tbody.appendChild(row);
                    }
                }
            }
}


/**
 * Sorts the geojson object properties 
 * @param {geoJSON} feature 
 * @returns sorted geojson object
 */
function sortGeoJSONFeatureProperties(feature) {
    // Check if the input is a valid GeoJSON feature with properties
    if (feature && feature.type === 'Feature' && feature.properties) {
        // Sort the properties object by keys
        feature.properties = sortObjectByKeys(feature.properties);
    }
    return feature;
}

// Helper function to sort the keys of an object recursively
function sortObjectByKeys(obj) {
    const sortedKeys = Object.keys(obj).sort();
    const sortedObj = {};

    sortedKeys.forEach(key => {
        if (typeof obj[key] === 'object' && obj[key] !== null && !Array.isArray(obj[key])) {
            sortedObj[key] = sortObjectByKeys(obj[key]);  // Recursively sort nested objects
        } else {
            sortedObj[key] = obj[key];
        }
    });

    return sortedObj;
}

// Create a custom control class
class CustomTableControl {
    onAdd(map) {
        // Create a container element for the control
        this._container = document.createElement('div');
        this._container.className = 'maplibregl-ctrl maplibregl-ctrl-group';
        this._container.style.backgroundColor = 'white';
        this._container.style.width = '30px';
        this._container.style.height = '30px';
        this._container.style.cursor = 'pointer';
        this._container.innerHTML = 'Table'; // Button text

        // Add click event listener
        this._container.addEventListener('click', () => {
            toggleSidebar('right'); // Function to be called
        });

        return this._container;
    }

    onRemove() {
        // Remove the container when the control is removed from the map
        this._container.parentNode.removeChild(this._container);
        this._map = undefined;
    }
}

var customTableControl = new CustomTableControl();
map.addControl(customTableControl, 'top-right');

setInterval(updateTime, 1000);
updateTime();