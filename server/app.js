const express = require('express');
const app = express();
const mqtt = require('mqtt');
const client = mqtt.connect("mqtt://broker.hivemq.com:1883");

let topic = "/gps/device/0";

app.listen(3000, () => {
    console.log("Server listening on 3000");
});

app.use('/', express.static('../client'));

client.on('connect', () => {
    console.log("MQTT Connected");
    client.subscribe(topic);
});

client.on('message', (topic, message) => {
    console.log("Topic: " + topic);
    console.log("Message: " + message);
})
