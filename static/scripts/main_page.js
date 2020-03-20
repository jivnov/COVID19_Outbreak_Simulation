/**
 * Sends request and executes callback when request is received.
 * @param {string} url - endpoint
 * @param {dict} data - data to send. Leave empty if send a POST request
 * @param {string} method - request method
 * @returns new Promise
 */
function sendRequest(url, data, method) {
    return new Promise(function (resolve, reject) {
            var xhr = new XMLHttpRequest();
            xhr.open(method, url, true);
            xhr.timeout = 5000;
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.onreadystatechange = function () {
                if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                    if (method == "GET") {
                        result = JSON.parse(xhr.responseText)
                        resolve(result)
                    } else {
                        resolve();
                    }
                } else if (xhr.readyState == XMLHttpRequest.DONE) {
                    var response = JSON.parse(xhr.responseText);
                    alert(response.message)
                }
            };
            xhr.ontimeout = () => {
                reject("That took too long")
            }
            //TODO implement triming
            xhr.send(JSON.stringify(data))
        }
    )
}


function update() {
    let value = 60;
    let url = 'get_data?user_input=' + value;
    sendRequest(url, '', "GET").then((data) => {
        displayData(document.getElementById("confirmed"), data);
        displayData(document.getElementById("deaths"), data);
        displayData(document.getElementById("recovered"), data);
        integrate_plot(document.getElementById("plot"), data)
        // setTimeout(update, 1000)

    })
}

function displayData(element, data) {
    console.log(data);
    element.innerText = data.value[element.id];
}

function integrate_plot(element, data) {

    element.src = data.value[element.id];
    console.log(data[element.id]);

}




var mapConfig = {
  'layers': [{
    'type': 'cartodb',
    'options': {
      'cartocss_version': '2.1.1',
      'cartocss': '#layer { polygon-fill: #F00; }',
      'sql': 'select * from european_countries_e where area > 0'
    }
  }]
};

var cartoDBSource = new CartoDB({
  account: 'documentation',
  config: mapConfig
});

var map = new Map({
  layers: [
    new TileLayer({
      source: new OSM()
    }),
    new TileLayer({
      source: cartoDBSource
    })
  ],
  target: 'map',
  view: new View({
    center: [0, 0],
    zoom: 2
  })
});

function setArea(n) {
  mapConfig.layers[0].options.sql =
      'select * from european_countries_e where area > ' + n;
  cartoDBSource.setConfig(mapConfig);
}


document.getElementById('country-area').addEventListener('change', function() {
  setArea(this.value);
});
