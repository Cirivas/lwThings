var mongoose = require('mongoose')
var Schema   = mongoose.Schema
var ObjectId = Schema.Types.ObjectId

var wordSchema = new Schema({
	word:	{ type: String, unique: true, required: true },
	type:	{ type: String, required: true }
})

module.exports = mongoose.model('Word', wordSchema)