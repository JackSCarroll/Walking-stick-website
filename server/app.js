const express = require('express');
const app = express();
const mqtt = require('mqtt');
const client = mqtt.connect("mqtt://broker.hivemq.com:1883");
const socket = require('socket.io');
const server = app.listen(3000)

let io = socket(server);
let topic = "/gps/device/0";
let latlong;

io.sockets.on('connection', newConnection)

function newConnection(socket) {
    console.log('new connection: ' + socket.id);
}

app.use('/', express.static('../client'));

client.on('connect', () => {
    console.log("MQTT Connected");
    client.subscribe(topic);
});

client.on('message', (topic, message) => {
    sleep(5000);
    latlong = message.toString();
    latlong = JSON.parse(latlong);
    //console.log(latlong.lat);
    io.sockets.emit("coords", latlong);
});

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}