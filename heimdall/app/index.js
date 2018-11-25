
const { wotan: { ip, port } } = require('../env.json');
const { startWotan } = require('./models/wotan');

const start = async () => {
  // 1. attempt to contact the initial wotan server and do not return until you do. This means not accepting requests or opening websockets.
  const wotan = await startWotan(ip, port);
  if (!wotan.connected) return;

  // 2. Start the http server

  // 3. Start the websocket server

};

module.exports = {
  start,
};
