const express = require('express');
const app = express();
const mqtt = require('mqtt');
const client = mqtt.connect("mqtt://broker.hivemq.com:1883");
const socket = require('socket.io');
const bodyParser = require('body-parser');
const server = app.listen(3000)
const mongoose = require('mongoose');
const User = require('./models/user')
const bcrypt = require('bcryptjs');

mongoose.connect('mongodb+srv://antos:walkingStick@users.aiokz.mongodb.net/Users?retryWrites=true&w=majority', {
    useNewUrlParser: true,
    useUnifiedTopology: true,
});

let io = socket(server);
let topic = "/gps/device/0";
let latlong;

var options = {
    index: "login.html"
}

app.use('/', express.static('../client', options));
app.use(bodyParser.json());

app.post('/api/register', async (req, res) => {
    console.log(req.body);
    const { firstname, lastname, password: plainTextPassword, email, phone, serial } = req.body
    const password = await bcrypt.hash(plainTextPassword, 10);

    try {
        const response = await User.create({
            firstname,
            lastname, 
            password,
            email,
            phone,
            serial
        });
        console.log(response);

    } catch(error) {
        if(error.code === 11000) {
            return res.json({ status: 'error', error: 'Username already in use' });
        }
        throw error
    }
    res.json({ status: "ok" });
})

io.sockets.on('connection', newConnection)
function newConnection(socket) {
    console.log('new connection: ' + socket.id);
}

client.on('connect', () => {
    console.log("MQTT Connected");
    client.subscribe(topic);
});

client.on('message', (topic, message) => {
    latlong = message.toString();
    latlong = JSON.parse(latlong);
    console.log(latlong.lat);
    io.sockets.emit("coords", latlong);
});