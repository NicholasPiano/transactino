
const api = require('./util/api');
const http = require('http');
const WebSocket = require('ws');
const uuidv4 = require('uuid/v4');

const uuid = () => uuidv4().replace(/-/g, '');

const HTTPPort = 8080;
const HTTPHostname = 'localhost';
const HTTPServer = http.createServer();
HTTPServer.listen(HTTPPort, HTTPHostname, () => {
  console.log(`HTTP server running at http://${HTTPHostname}:${HTTPPort}/`);
});

const websocketPort = 8081;
const websocketServer = new WebSocket.Server({ port: websocketPort });
console.log(`Websocket server running at ws://${HTTPHostname}:${websocketPort}/`);

let clients = {};

HTTPServer.on('request', (request, response) => {
  if (request.method === 'POST') {
    let body = [];
    request.on('data', chunk => body.push(chunk));
    request.on('end', () => {
      body = Buffer.concat(body).toString();
      const { id, ip, channel, transactino } = JSON.parse(body);
      const { [channel]: client } = clients;
      client.send(JSON.stringify(transactino), () => response.end());
    });
  } else {
    response.statusCode = 404;
    response.end();
  }
});

const transactinoURL = 'http://localhost:8000';

websocketServer.on('connection', (client, clientRequest) => {
  client.ip = clientRequest.connection.remoteAddress;
  client.channel = uuid();
  clients[client.channel] = client;

  client.on('message', message => {
    const data = JSON.stringify({
      id: uuid(),
      ip: client.ip,
      channel: client.channel,
      transactino: message,
    });
    const options = {
      path: '/api/',
      method: 'POST',
      headers: {
        'Cookie': `csrftoken=${client.token}`,
        'X-CSRFToken': client.token,
        'Content-Type': 'application/json',
        'Content-Length': data.length,
      },
    };
    const request = http.request(transactinoURL, options, response => {
      let body = [];
      response.on('data', chunk => body.push(chunk));
      response.on('end', () => {
        const bodyString = Buffer.concat(body).toString();
        const { transactino } = JSON.parse(bodyString);
        client.send(JSON.stringify(transactino));
      });
    });

    request.write(data);
    request.end();
  });

  const request = http.get(transactinoURL, { path: '/api/' }, response => {
    let body = [];
    response.on('data', chunk => body.push(chunk));
    response.on('end', () => {
      const bodyString = Buffer.concat(body).toString();
      const { token } = JSON.parse(bodyString);
      client.token = token;
    });
  });

  request.end();

  client.on('close', () => {
    console.log('CLOSE');
  });
});
