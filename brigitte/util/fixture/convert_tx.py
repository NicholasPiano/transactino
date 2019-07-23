
import json
from os.path import join
import subprocess

def get_transaction(txid):
  get_transaction_command = subprocess.run(
    [
      'curl',
      '-s',
      'http://localhost:8332/rest/tx/{}.json'.format(txid),
    ],
    stdout=subprocess.PIPE,
  )

  return json.loads(get_transaction_command.stdout.decode('utf-8'))

transactions = {}

with open('000000000000000000185bb785a144202e9715007fc150a95cd464755f3a3562.json') as block_file:
  block_json = json.loads(block_file.read())

  for transaction_json in block_json.get('tx'):
    for vin_json in transaction_json.get('vin'):
      if 'coinbase' not in vin_json:
        txid = vin_json.get('txid')
        past_transaction_json = get_transaction(txid)

        past_transaction = {
          'txid': past_transaction_json.get('txid'),
          'hash': past_transaction_json.get('hash'),
          'blockhash': past_transaction_json.get('blockhash'),
          'size': past_transaction_json.get('size'),
        }

        past_vins = []
        for past_vin_json in past_transaction_json.get('vin'):
          if 'coinbase' not in past_vin_json:
            past_vins.append({
              'txid': past_vin_json.get('txid'),
              'vout': past_vin_json.get('vout'),
            })

        past_transaction['vin'] = past_vins

        past_vouts = []
        for past_vout_json in past_transaction_json.get('vout'):
          past_vouts.append({
            'n': past_vout_json.get('n'),
            'scriptPubKey': {
              'addresses': past_vout_json.get('scriptPubKey').get('addresses'),
            },
            'value': past_vout_json.get('value'),
          })

        past_transaction['vout'] = past_vouts

        transactions[txid] = past_transaction

print(json.dumps(transactions))
