const mongoose = require('mongoose');

const UserSchema = new mongoose.Schema(
    {
        firstname: { type: String, required: true },
        lastname: { type: String, required: true },
        password: { type: String, required: true },
        email: { type: String, required: true, unique: true },
        phone: { type: String, required: true },
        serial: { type: String, required: true, unique: true}
    },
    { collection: 'users '}
);

const model = mongoose.model('UserSchema', UserSchema);
module.exports = model;
