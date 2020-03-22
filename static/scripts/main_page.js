// import * as map from "./map"

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
            xhr.timeout = 50000;
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


async function update() {
    let days = 360;
    let value = "init " + days;
    let url = 'get_data?user_input=' + value;
    let infected = ['USA', 'AUS', 'NGA', 'CHN'];
    for (let i = 0; i < days; i++) {


                await sendRequest(url, '', "GET").then((data) => {
                    displayData(document.getElementById("confirmed"), data);
                    displayData(document.getElementById("deaths"), data);
                    displayData(document.getElementById("recovered"), data);
                    integrate_plot(document.getElementById("plot"), data)
                    colorize(data.value["infected_countries_arr"])


                })
                url = 'get_data?user_input=' + days;
                // colorize(infected)



    }
}

function tmp() {

}

function displayData(element, data) {
    console.log(data);
    element.innerText = data.value[element.id];
}

function integrate_plot(element, data) {

    element.src = data.value[element.id];
    console.log(data[element.id]);

}


