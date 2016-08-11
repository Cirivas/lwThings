var express = require('express');
var cors	= require('cors');
var zerorpc	= require("zerorpc");
var bodyParser = require('body-parser');
var app		= express();
var router = express.Router();

var client = new zerorpc.Client();
client.connect("tcp://127.0.0.1:4242");

app.disable('x-powered-by');
app.use(cors());

app.use(bodyParser.urlencoded({ extended: false}));
app.use(bodyParser.json());



router.post('/pet/:text', function(req, res){
	console.log("Lamatizacion de " + req.params.text);
	client.invoke("lemma",req.params.text, function(err, resp, more){
		if(err) console.log("Error");
		res.send(resp);
	});
});

app.use(router);
app.listen(8080, function(){
	console.log("Example app");
});