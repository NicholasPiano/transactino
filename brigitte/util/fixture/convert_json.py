
import json

with open('fixture/block.json', 'r+') as block_json_file:
  block_json = json.loads(block_json_file.read())

  block = {
    'previousblockhash': block_json.get('previousblockhash'),
    'height': block_json.get('height'),
  }

  transactions = []
  for transaction_json in block_json.get('tx'):
    transaction = {
      'txid': transaction_json.get('txid'),
      'hash': transaction_json.get('hash'),
      'size': transaction_json.get('size'),
    }

    vins = []
    for vin_json in transaction_json.get('vin'):
      if 'coinbase' not in vin_json:
        vins.append({
          'txid': vin_json.get('txid'),
          'vout': vin_json.get('vout'),
        })

    transaction['vin'] = vins

    vouts = []
    for vout_json in transaction_json.get('vout'):
      vouts.append({
        'n': vout_json.get('n'),
        'scriptPubKey': {
          'addresses': vout_json.get('scriptPubKey').get('addresses'),
        },
        'value': vout_json.get('value'),
      })

    transaction['vout'] = vouts
    transactions.append(transaction)

  block['tx'] = transactions

  print(json.dumps(block))
