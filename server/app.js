const SerialPort = require('serialport');
const GPS = require('gps');
const gps = new GPS;
const express = require('express');
const app = express();

let latitude = 0;
let longitude = 0;

app.listen(3000, () => {
    console.log("Server listening on 3000");
});

app.use('/', express.static('../client'));

const serialPort = new SerialPort('/dev/ttyACM0', { // change path
    baudRate: 9600,
    parser: new SerialPort.parsers.Readline({
        delimiter: '\r\n'
    })
});

gps.on('data', data => {
    latitude = gps.state.lat;
    longitude = gps.state.lon
    console.log(latitude);
    console.log(longitude);
});

serialPort.on('data', data => {
    gps.updatePartial(data);
});
