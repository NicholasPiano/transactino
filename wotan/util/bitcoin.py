
import json
import subprocess
from os.path import join

from django.conf import settings

if settings.DEBUG:
  fixture_path = join(settings.DJANGO_PATH, 'util', 'fixture')
  block_hash = '000000000000000000185bb785a144202e9715007fc150a95cd464755f3a3562'

def get_info():
  if settings.DEBUG:
    return {
      'bestblockhash': block_hash,
    }

  get_info_command = subprocess.run(
    [
      'bitcoin-cli',
      'getblockchaininfo',
    ],
    stdout=subprocess.PIPE,
  )

  return json.loads(get_info_command.stdout.decode('utf-8'))

get_block_hashes = {}
if settings.DEBUG:
  with open(join(fixture_path, '{}.json'.format(block_hash))) as block_file:
    get_block_hashes = {
      block_hash: json.loads(block_file.read())
    }

def get_block(hash):
  if hash in get_block_hashes:
    return get_block_hashes.get(hash)

  if len(get_block_hashes) > 100:
    del get_block_hashes[list(get_block_hashes.keys())[0]]

  get_block_command = subprocess.run(
    [
      'curl',
      '-s',
      'http://localhost:8332/rest/block/{}.json'.format(hash),
    ],
    stdout=subprocess.PIPE,
  )

  data = json.loads(get_block_command.stdout.decode('utf-8'))

  get_block_hashes[hash] = data

  return data

def get_previous_hash(hash):
  return get_block(hash).get('previousblockhash')

def get_latest_block_hash():
  return get_info().get('bestblockhash')

if settings.DEBUG:
  with open(join(fixture_path, 'tx.json')) as transaction_file:
    transactions = json.loads(transaction_file.read())

def get_transaction(txid):
  if settings.DEBUG:
    return transactions.get(txid)

  get_transaction_command = subprocess.run(
    [
      'curl',
      '-s',
      'http://localhost:8332/rest/tx/{}.json'.format(txid),
    ],
    stdout=subprocess.PIPE,
  )

  return json.loads(get_transaction_command.stdout.decode('utf-8'))

class Delta():
  def __init__(self, vin_json=None, vout_json=None, minimal=False, out_txid=None):
    self.minimal = minimal
    if vin_json is not None:
      self.incoming(vin_json)

    if vout_json is not None:
      self.out_txid = out_txid
      self.outgoing(vout_json)

  def incoming(self, vin_json):
    self.txid = vin_json.get('txid')
    self.index = vin_json.get('vout')

    if not self.minimal:
      past_transaction_json = get_transaction(self.txid)
      past_vout = past_transaction_json.get('vout')[self.index]
      self.value = int(past_vout.get('value') * 10e8)

  def outgoing(self, vout_json):
    self.index = vout_json.get('n')
    self.value = int(vout_json.get('value') * 10e8)
    self.addresses = vout_json.get('scriptPubKey').get('addresses')

class Transaction():
  def __init__(self, transaction_json, minimal=False):
    self.txid = transaction_json.get('txid')
    self.hash = transaction_json.get('hash')
    self.size = transaction_json.get('size')
    self.minimal = minimal

    self.create_deltas(transaction_json)

  def create_deltas(self, transaction_json):
    self.incoming_deltas = [
      Delta(vin_json=vin_json, minimal=self.minimal)
      for vin_json
      in transaction_json.get('vin')
      if 'coinbase' not in vin_json
    ]
    self.outgoing_deltas = [
      Delta(vout_json=vout_json, out_txid=self.txid)
      for vout_json
      in transaction_json.get('vout')
    ]

  def get_fee(self):
    total_incoming = sum([
      delta.value
      for delta
      in self.incoming_deltas
    ])

    total_outgoing = sum([
      delta.value
      for delta
      in self.outgoing_deltas
    ])

    if total_incoming:
      fee = total_incoming - total_outgoing
      density = fee / self.size if fee else 0

      return fee, density

    return 0, 0

  def find_deltas_with_address(self, address):
    return [
      delta
      for delta
      in self.outgoing_deltas
      if (
        delta.addresses is not None
        and address in delta.addresses
      )
    ]

class Block():
  def __init__(self, hash, minimal=False):
    self.hash = hash
    block_json = get_block(hash)

    self.minimal = minimal
    self.parent = block_json.get('previousblockhash')
    self.height = block_json.get('height')
    self.hash = block_json.get('hash')

    self.create_transactions(block_json.get('tx'))

  def create_transactions(self, transactions_json):
    self.transactions = [
      Transaction(transaction_json, minimal=self.minimal)
      for transaction_json
      in transactions_json
    ]

  def find_deltas_with_address(self, address):
    deltas = []
    for transaction in self.transactions:
      deltas.extend(transaction.find_deltas_with_address(address))

    return deltas
