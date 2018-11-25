
const uuidv4 = require('uuid/v4');

module.exports = {
  uuid: () => uuidv4().replace(/-/g, ''),
};
