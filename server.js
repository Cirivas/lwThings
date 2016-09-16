var express = require('express')
var cors	= require('cors')
var zerorpc	= require('zerorpc')
var path 	= require('path')
var bodyParser = require('body-parser')
var app		= express()
var router 	= express.Router()
var client = new zerorpc.Client()

//ZeroRPC python-nodejs 
client.connect("tcp://10.0.0.4:4242")

app.disable('x-powered-by')
app.use(cors())

app.use(bodyParser.urlencoded({ extended: true}))
app.use(bodyParser.json())

router.post('/pet', function(req, res){
	console.log("Node: Lematizacion de " + req.body.text)
	setTimeout(client.invoke("lemma",req.body.text, function(err, resp, more){
		if(err) console.log("Error")
		console.log("Lema: " + resp)
		res.send(resp)
	}), 7000)
})

//Send index file
router.get('/', function(req, res){
	res.sendFile(path.join(__dirname+'/index.html'))
})

//Serve videos
router.get('/vids/:video', function(req, res){
	res.sendFile(path.join(__dirname+'/vids/'+req.params.video))
})

app.use(router)
app.listen(8080, function(){
	console.log("Example app")
})