
const http = require('http');
const WebSocket = require('ws');

const { uuid } = require('./util/uuid');

const app = require('./app');
const api = require('./util/api');

app.start();

// 1. Start up
//  a. Connect to initial Wotan
//  b. Activate http server
//  c. Activate socket server
// 2. Running
//  a. Handle messages from client
//  b. Make requests to wotan
//  c.

// Lists
// 1. Wotan list
// 2. Client list -> map to wotan

// Process for finding wotan for client
// 1. Ask all known wotans Question 1: do they know the IP?
// 2. If Answer 1 returns affirmative from anyone, set that wotan as mapping for client
// 3. If Answer 1 is no, ask Question 2: do any of the peers you know of know the IP? This question should be recursive, permeating all wotans until an answer is found.
// 4. Finally, a wotan is chosen: the first to know the IP or the first contacted.
// 5. The only way this could work is if

// const HTTPPort = 8080;
// const HTTPHostname = 'localhost';
// const HTTPServer = http.createServer();
// HTTPServer.listen(HTTPPort, HTTPHostname, () => {
//   console.log(`HTTP server running at http://${HTTPHostname}:${HTTPPort}/`);
// });
//
// const websocketPort = 8081;
// const websocketServer = new WebSocket.Server({ port: websocketPort });
// console.log(`Websocket server running at ws://${HTTPHostname}:${websocketPort}/`);
//
// let clients = {};
//
// HTTPServer.on('request', (request, response) => {
//   if (request.method === 'POST') {
//     let body = [];
//     request.on('data', chunk => body.push(chunk));
//     request.on('end', () => {
//       body = Buffer.concat(body).toString();
//       const { id, ip, channel, transactino } = JSON.parse(body);
//       const { [channel]: client } = clients;
//       client.send(JSON.stringify(transactino), () => response.end());
//     });
//   } else {
//     response.statusCode = 404;
//     response.end();
//   }
// });
//
// const transactinoURL = 'http://localhost:8000';
//
// websocketServer.on('connection', (client, clientRequest) => {
//   client.ip = clientRequest.connection.remoteAddress;
//   client.channel = uuid();
//   clients[client.channel] = client;
//
//   client.on('message', message => {
//     const data = JSON.stringify({
//       id: uuid(),
//       ip: client.ip,
//       channel: client.channel,
//       transactino: message,
//     });
//     const options = {
//       path: '/api/',
//       method: 'POST',
//       headers: {
//         'Cookie': `csrftoken=${client.token}`,
//         'X-CSRFToken': client.token,
//         'Content-Type': 'application/json',
//         'Content-Length': data.length,
//       },
//     };
//     const request = http.request(transactinoURL, options, response => {
//       let body = [];
//       response.on('data', chunk => body.push(chunk));
//       response.on('end', () => {
//         const bodyString = Buffer.concat(body).toString();
//         const { transactino } = JSON.parse(bodyString);
//         client.send(JSON.stringify(transactino));
//       });
//     });
//
//     request.write(data);
//     request.end();
//   });
//
//   const request = http.get(transactinoURL, { path: '/api/' }, response => {
//     let body = [];
//     response.on('data', chunk => body.push(chunk));
//     response.on('end', () => {
//       const bodyString = Buffer.concat(body).toString();
//       const { token } = JSON.parse(bodyString);
//       client.token = token;
//     });
//   });
//
//   request.end();
//
//   client.on('close', () => {
//     console.log('CLOSE');
//   });
// });
