mapboxgl.accessToken = config.MY_KEY;
let infected = ['USA', 'AUS', 'NGA', 'CHN'];
var map = new mapboxgl.Map({
    container: 'map', //this is the id of the container you want your map in
    style: 'mapbox://styles/mapbox/dark-v10', // this controls the style of the map. Want to see more? Try changing 'light' to 'simple'.
    minZoom: 2 // We want our map to start out pretty zoomed in to start.
});

map.on('load', function () { //On map load, we want to do some stuff
    map.addLayer({ //here we are adding a layer containing the tileset we just uploaded
        'id': 'countries',//this is the name of our layer, which we will need later
        'source': {
            'type': 'vector',
            'url': 'mapbox://byfrost-articles.74qv0xp0' // <--- Add the Map ID you copied here
        },
        'source-layer': 'ne_10m_admin_0_countries-76t9ly', // <--- Add the source layer name you copied here
        'type': 'fill',
        'paint': {
            'fill-color': '#340300', //this is the color you want your tileset to have (I used a nice purple color)
            'fill-outline-color': '#F2F2F2' //this helps us distinguish individual countries a bit better by giving them an outline
        }
    });



    map.setFilter('countries', ['in', 'ADM0_A3_IS']); // This line lets us filter by country codes.

    map.on('click', 'countries', function (mapElement) {
        const countryCode = mapElement.features[0].properties.ADM0_A3_IS; // Grab the country code from the map properties.
        // map.setFilter('countries', ['in', 'ADM0_A3_IS'].concat([countryCode]));
        fetch(`https://restcountries.eu/rest/v2/alpha/${countryCode}`) // Using tempalate tags to create the API request
            .then((data) => data.json()) //fetch returns an object with a .json() method, which returns a promise
            .then((country) => { //country contains the data from the API request
                // Let's build our HTML in a template tag
                const html = ` 
        <img src='${country.flag}' /> 
        <ul>
          <li><h3>${country.name}</h3></li>
          <li><strong>Currencies:</strong> ${country.currencies.map((c) => c.code).join(', ')}</li>
          <li><strong>Capital:</strong> ${country.capital}</li>
          <li><strong>Population:</strong> ${country.population}</li>
          <li><strong>Demonym:</strong> ${country.demonym}</li>
        </ul>
      `; // Now we have a good looking popup HTML segment.
                new mapboxgl.Popup() //Create a new popup
                    .setLngLat(mapElement.lngLat) // Set where we want it to appear (where we clicked)
                    .setHTML(html) // Add the HTML we just made to the popup
                    .addTo(map); // Add the popup to the map
            });
    });
});

function colorize(codes) {
    map.setFilter('countries', ['in', 'ADM0_A3_IS'].concat(codes));
}
