
let wotans = {

};

function Wotan (ip, port) {
  this.connect = async function () {

  }
}

const getWotan = (ip, port) => {
  const key = `${ip}:${port}`;
  const { [key]: wotan } = wotans;

  if (wotan) {
    return wotan;
  }

  const newWotan = new Wotan(ip, port);
  wotans[key] = newWotan;

  return newWotan;
}

const startWotan = async (ip, port) => {
  const wotan = getWotan(ip, port);

  await wotan.connect();

  return wotan;
}

module.exports = {
  wotans,
  Wotan,
  startWotan,
};
