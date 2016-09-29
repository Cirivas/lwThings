# SignIt

## Nodejs
```
curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### Zmq

Existe un problema con la librería ZMQ, hay que instalarla manualmente.

https://github.com/JustinTulloss/zeromq.node

El resto de las dependencias se instala sin problemas utilizando ```npm install``` en la carpeta base (donde está package.json)

## Freeling
download: https://github.com/TALP-UPC/FreeLing/releases

### Requirements
```
sudo apt-get install libboost-regex-dev libicu-dev zlib1g-dev
sudo apt-get install libboost-system-dev libboost-program-options-dev libboost-thread-dev+
```
info: https://talp-upc.gitbooks.io/freeling-user-manual/content/installation.html

Part of the Speech (PoS) tags: https://talp-upc.gitbooks.io/freeling-user-manual/content/tagsets/tagset-es.html

## Python

Versión utilizada: 2.7 (utilizando pip)

### Paquetes adicionales:
zerorpc: ```pip install zerorpc```


## MongoDB

Versión instalada: 2.6.10
```
sudo apt-get install mongodb-server
```
## Servicios corriendo

Guía node.js + nginx + pm2

https://www.digitalocean.com/community/tutorials/how-to-set-up-a-node-js-application-for-production-on-ubuntu-14-04


### Nginx

Configuración básica para hacer el paso a node.js:

```
server {
    listen 80;

    server_name http://signit.brazilsouth.cloudapp.azure.com/; ##Puede omitirse

    location / {
            proxy_pass http://10.0.0.4:8080; ##Ip local, puerto servido por node
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
}
```
Reiniciar servicio: ```sudo service nginx restart```

### Pm2

Para servir node, se utiliza pm2

```sudo npm install pm2 -g```

Uso: ```pm2 start|stop|restart server.js```

### Python como servicio

Para mantener el script de python corriendo, se configuró un servicio (válido para Ubuntu 15 y superior) utilizando systemd:

Archivo /etc/systemd/system/pyserv.service
```
[Unit]
Description=Python for SignIt
After=multi-user.target

[Service]
Type=simple
User=desarrollador
WorkingDirectory=/home/desarrollador/lwThings
ExecStart=/usr/bin/python2 /home/desarrollador/lwThings/server.py
Restart=on-failure
StandardOutput=syslog
StandardError=syslog

[Install]
WantedBy=multi-user.target
```

Ejecutar los siguientes para cuando se haga alguna modificación al service o se quiera reiniciar:

```
sudo systemctl daemon-reload
sudo systemctl enable pyserv.service
sudo systemctl start|stop|restart pyserv.service
```

El comando ```enable``` solo es necesario ejecutarlo una vez.

## Links de Interés:

- Diccionario de Señas A-H: http://portales.mineduc.cl/usuarios/edu.especial/File/2012/DiccionarioSeNasAH.pdf
- Diccionario de Señas I-Z: http://portales.mineduc.cl/usuarios/edu.especial/File/2012/DiccionarioSenasIZ.pdf
- Diccionario de Señas Videos http://diccionariodesenas.umce.cl/
- Introducción pequeña a LSCh https://issuu.com/fundacionamoma/docs/introducci__n_a_la_lengua_de_se__as
- Introducción a la gramática LS España http://blog.showleap.com/tag/gramatica/
