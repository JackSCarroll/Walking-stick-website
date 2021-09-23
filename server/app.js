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
const jwt = require('jsonwebtoken');
require('dotenv').config();
const JWT_SECRET = 'hijshf7897^&*#jdfksh82hjdkash';

mongoose.connect(process.env.API_KEY, {
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

app.post('/api/login', async (req, res) => {
    const { email, password } = req.body
    const user = await User.findOne({ email }).lean()

    if(!user){
        return res.join({ status: 'error', error: 'Invalid username/password' });
    }

    if(await bcrypt.compare(password, user.password)){
            const token = jwt.sign({
                id: user._id, 
                email: email.email
            }, JWT_SECRET
        );
        return res.json({ status:'ok', data: ''})
    }
    res.json({ status: 'ok', data: token });
})

app.post('/api/register', async (req, res) => {
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
    io.sockets.emit("coords", latlong);
}

client.on('connect', () => {
    console.log("MQTT Connected");
    client.subscribe(topic);
});

client.on('message', (topic, message) => {
    latlong = message.toString();
    latlong = JSON.parse(latlong);
    //console.log(latlong.lat);
});