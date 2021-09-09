const SerialPort = require('serialport');
const GPS = require('gps');
const gps = new GPS;
const mqtt = require('mqtt');
const client = mqtt.connect("mqtt://broker.hivemq.com:1883");

let latitude = 0;
let longitude = 0;
let latlong;
let topic = "/gps/device/0";

client.on('connect', () => {
    console.log("MQTT Connected");
    client.subscribe(topic);
});

const serialPort = new SerialPort('/dev/ttyACM0', { // change path
    baudRate: 9600,
    parser: new SerialPort.parsers.Readline({
        delimiter: '\r\n'
    })
});

gps.on('data', data => {
    latitude = gps.state.lat;
    longitude = gps.state.lon
    latlong =
    {
        lat: latitude,
        long: longitude
    };
    client.publish(topic, JSON.stringify(latlong));
    console.log(topic, JSON.stringify(latlong));
});

serialPort.on('data', data => {
    gps.updatePartial(data);
});