var express = require('express');
var cors	= require('cors');
var app		= express();

app.disable('x-powered-by');
app.use(cors());

app.post('/pet', function(req, res){
	console.log("Peticion");
	res.jsonp({text: 'Hola mundo'});
});

app.listen(8080, function(){
	console.log("Example app");
});