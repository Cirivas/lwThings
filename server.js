var express = require('express')
var cors	= require('cors')
var zerorpc	= require('zerorpc')
var path 	= require('path')
var bodyParser = require('body-parser')
var mongoose	= require('mongoose')
var app		= express()
var router 	= express.Router()
var client = new zerorpc.Client({heartbeatInterval: 15000})

//Model
var WordModel = require('./model/word')

//ZeroRPC python-nodejs 
client.connect("tcp://127.0.0.1:4242")

app.disable('x-powered-by')
app.use(cors())

app.use(bodyParser.urlencoded({ extended: true}))
app.use(bodyParser.json())

router.post('/pet', function(req, res){
	console.log("Node: Lematizacion de " + req.body.text)
	client.invoke("lemma",req.body.text, function(err, resp, more){
		if(err) console.log(err)
		console.log("Texto nuevo: " + resp)
		res.send(resp)
	})
})

//Send index file
router.get('/', function(req, res){
	res.sendFile(path.join(__dirname+'/public/index.html'))
})

//Serve videos
router.get('/vids/:video', function(req, res){
	res.sendFile(path.join(__dirname+'/public/vids/'+req.params.video))
})

router.get('/test/:word/:type', function(req, res){
	var word = new WordModel({word:req.params.word, type: req.params.type})
	word.save(function(er, word){
		if(er) res.send('Duplicado')
		else res.send(word)
	})
})

router.get('/test', function(req, res){
	WordModel.find(function(err, words){
		res.send(words)
	})
})
//Mongodb 
// Connection to DB
mongoose.connect('mongodb://localhost:27017/words', function(err, res) {
  if(err) throw err;
  console.log('Connected to Database');
});

app.use(router)
app.use(express.static('public'))
app.listen(8080, function(){
	console.log("Example app")
})
