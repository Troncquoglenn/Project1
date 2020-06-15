const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

let htmlKnop, htmlBody, htmlKleur, htmlKleurWaarde, htmlKleurKnop, htmlSwitch, htmlUitschakelen;

let kleur, slider = false;

socket.on("B2F_knop", function(value){
  console.log(value);
  if (window.location.href === `http://${window.location.hostname}/standaardmodus.html`){
    if (value === "on") return htmlSwitch.checked = true;
    if (value === "off") return htmlSwitch.checked = false;


  };



});

const drawChart = function (label, data, keuze) {
  let ctx = document.getElementById('myChart').getContext('2d');

  let chart = new Chart(ctx, {
    type: 'line',

    data: {
      labels: label,
      datasets: [
        {
          label: keuze,
          backgroundColor: 'rgba(0,53,122,0.4)',
          borderColor: "#20529D",
          borderCapStyle: 'butt',
          borderDashOffset: 0.0,
          borderJoinStyle: 'mitter',
          pointBorderColor: "#20529D",
          poinBackgroundColor: "#fff",
          pointBorderWidth: 1,
          pointBorderWidth: 1,
          pointHoverRadius: 5,
          pointHoverBackGroundColor: "#20529D",
          poinHoverBorderColor: "#fff",
          pointHoverBorderWidth: 2,
          pointRadius: 1,
          pointHitRadius: 10,
          data: data,
          fill: true
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true

    }
  })
};

const showData = function (jsonObject) {
  let keuze;

  if (jsonObject.temperatuur) {
    keuze = "Temperatuur";
    htmlBody.innerHTML = `<div class="o-row o-container"><canvas id= "myChart"></div>`;

    let tijd = [];
    let waarde = [];


    for (const element of jsonObject.temperatuur) {
      tijd.push(element.meetdatum);
      waarde.push(element.meetwaarde);

    };
    drawChart(tijd.slice(-10), waarde.slice(-10), keuze);
  };
  if (jsonObject.licht) {
    keuze = "Lichtintensiteit";
    htmlBody.innerHTML = `<div class="o-row o-container"><canvas id= "myChart"></div>`;

    let tijd = [];
    let waarde = [];


    for (const element of jsonObject.licht) {
      tijd.push(element.meetdatum);
      waarde.push(element.meetwaarde);

    };
    drawChart(tijd.slice(-10), waarde.slice(-10), keuze);
  };
  if (jsonObject.beweging) {
    keuze = "Beweging";
    htmlBody.innerHTML = `<div class="o-row o-container"><canvas id= "myChart"></div>`;

    let tijd = [];
    let waarde = [];


    for (const element of jsonObject.beweging) {
      tijd.push(element.meetdatum);
      waarde.push(element.meetwaarde);

    };

    drawChart(tijd.slice(-10), waarde.slice(-10), keuze);
  };


};

const listenToSwitch = function () {
  htmlSwitch.addEventListener("input", function () {
    console.log(htmlSwitch.checked)

    if (htmlSwitch.checked === true) {
      if (window.location.href === `http://${window.location.hostname}/standaardmodus.html`) return socket.emit("F2B_modus", "standaardmodus");
      if (window.location.href === `http://${window.location.hostname}/bewegingsmodus.html`) return socket.emit("F2B_modus", "bewegingsmodus");
      if (window.location.href === `http://${window.location.hostname}/automodus.html`) return socket.emit("F2B_modus", "automodus");
      if (window.location.href === `http://${window.location.hostname}/temperatuurmodus.html`) return socket.emit("F2B_modus", "temperatuurmodus");

    }
    else {
      if (window.location.href === `http://${window.location.hostname}/standaardmodus.html`) return socket.emit("F2B_modus", "off");
      if (window.location.href === `http://${window.location.hostname}/bewegingsmodus.html`) return socket.emit("F2B_modus", "off");
      if (window.location.href === `http://${window.location.hostname}/automodus.html`) return socket.emit("F2B_modus", "off");
      if (window.location.href === `http://${window.location.hostname}/temperatuurmodus.html`) return socket.emit("F2B_modus", "off");

    };

  });

};


const listenToKleur = function () {
  htmlKleurKnop.addEventListener("click", function () {
    kleur = htmlKleur.value;
    console.log(kleur)
    socket.emit("F2B_kleur", kleur)

  })

};

const listenToKnop = function () {


  for (const knop of htmlKnop) {
    knop.addEventListener("click", function () {
      if (window.location.href === `http://${window.location.hostname}/index.html` || window.location.href === `http://${window.location.hostname}/`) {
        if (knop == htmlKnop[0]) return location.replace(`http://${window.location.hostname}/standaardmodus.html`);
        if (knop == htmlKnop[1]) return location.replace(`http://${window.location.hostname}/automodus.html`);
        if (knop == htmlKnop[2]) return location.replace(`http://${window.location.hostname}/bewegingsmodus.html`);

      }
      else {
        console.log("knoppen")
        if (knop == htmlKnop[0]) return (handleData(`http://192.168.0.170:5000/historiek/licht`, showData));
        if (knop == htmlKnop[1]) return (handleData(`http://192.168.0.170:5000/historiek/temperatuur`, showData));
        if (knop == htmlKnop[2]) return (handleData(`http://192.168.0.170:5000/historiek/beweging`, showData));
      }
    });

  };
};


const showSwitch = function (jsonObject) {
  
  let modus = jsonObject.data;
  
  if (window.location.href === `http://${window.location.hostname}/standaardmodus.html` && modus === "standaardmodus")  return htmlSwitch.checked = true, console.log(modus);
  if (window.location.href === `http://${window.location.hostname}/bewegingsmodus.html` && modus === "bewegingsmodus") return htmlSwitch.checked = true, console.log(modus);
  if (window.location.href === `http://${window.location.hostname}/automodus.html` && modus === "automodus") return htmlSwitch.checked = true, console.log(modus);
  if (window.location.href === `http://${window.location.hostname}/temperatuurmodus.html` && modus === "temperatuurmodus") return htmlSwitch.checked = true, console.log(modus);
};


document.addEventListener("DOMContentLoaded", function () {
  
  console.log("dom met succes geladen");

  htmlBody = document.querySelector(".js-body");
  htmlKnop = document.querySelectorAll(".js-btn");
  htmlKleur = document.querySelector(".js-kleur");
  htmlKleurKnop = document.querySelector(".js-btn-kleur");
  htmlSwitch = document.querySelector(".js-switch");
  htmlUitschakelen = document.querySelector(".js-uitschakelen");


  

  if (htmlKnop) {
    listenToKnop();
  };

  if (htmlSwitch) {
    handleData(`http://192.168.0.170:5000/switch`, showSwitch);

    console.log("switch gevonden");
    listenToSwitch();
  };

  if (htmlKleurKnop) {
    console.log("kleur knop gevonden");
    listenToKleur();
  }

  if (htmlUitschakelen) {
    htmlUitschakelen.addEventListener("click", function () {
      console.log("click");
      let bevestiging = confirm("Weet je zeker dat je de Raspberry Pi wilt uitschakelen?");
      if (bevestiging === true) return socket.emit("F2B_uitschakelen");
    })
  }





});