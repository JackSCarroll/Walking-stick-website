const SerialPort = require('serialport');
const GPS = require('gps');
const gps = new GPS;
const mqtt = require('mqtt');
const client = mqtt.connect("mqtt://broker.hivemq.com:1883");

let latitude = 0;
let longitude = 0;
let latsub = -37.5;
let longsub = 145;
let latlong;
let topic = "/gps/device/0";

client.on('connect', () => {
    console.log("MQTT Connected");
    client.subscribe(topic);

    //Delete below when done.
    latlong =
    {
        lat: latsub,
        long: longsub
    };
    setInterval(function() {
        client.publish(topic, JSON.stringify(latlong));
        console.log(topic, JSON.stringify(latlong));
    }), 1000
    
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