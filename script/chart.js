const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

const drawChart = function (label, data) {
    let ctx = document.getElementById('myChart').getContext('2d');

    let chart = new Chart(ctx, {
        type: 'line',

        data: {
            labels: label,
            datasets: [
                {
                    label: 'Temperatuur',
                    backgroundColor: 'white',
                    borderColor: 'red',
                    data: data,
                    fill: false
                }
            ]
        }
    })
};


document.addEventListener("DOMContentLoaded", function () {
    socket.emit('F2B_inlezen_temp', 0);
    // let geschiedenis = "";
    // let htmlGeschiedenis = document.querySelector(".js-geschiedenis");

    socket.on('B2F_geschiedenis', function (jsonObject) {
        let tijd = [];
        let waarde = [];

        // console.log(jsonObject);


        for (const element of jsonObject.geschiedenis) {
            tijd.push(element.meetdatum);
            waarde.push(element.meetwaarde);

        };
        console.log(tijd.slice(-5))
        // console.log(tijd[-9])

        drawChart(tijd.slice(-20), waarde.slice(-20));
    });


});