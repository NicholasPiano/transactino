
import json
import subprocess
from os.path import join
import requests

from django.conf import settings

from util.force_array import force_array

class blockchaininfo_constants:
  URL = 'https://blockchain.info/'
  BEST_BLOCK_HASH = 'bestblockhash'
  LATEST_BLOCK = 'latestblock'
  HASH = 'hash'
  RAW_BLOCK = 'rawblock'
  PREV_BLOCK = 'prev_block'
  PREV_OUT = 'prev_out'
  VALUE = 'value'
  INDEX = 'n'
  ADDRESS = 'addr'
  SIZE = 'size'
  WEIGHT = 'weight'
  INPUTS = 'inputs'
  OUT = 'out'
  HEIGHT = 'height'
  TRANSACTION = 'tx'

if settings.DEBUG:
  fixture_path = join(settings.DJANGO_PATH, 'util', 'fixture')
  block_hash = '000000000000000000185bb785a144202e9715007fc150a95cd464755f3a3562'

def get_latest_block_hash():
  if settings.DEBUG:
    return block_hash

  get_response = requests.get(join(blockchaininfo_constants.URL, blockchaininfo_constants.LATEST_BLOCK))

  json_response = None
  try:
    json_response = json.loads(get_response.text)
  except:
    return None

  return json_response.get(blockchaininfo_constants.HASH)

get_block_hashes = {}
if settings.DEBUG:
  with open(join(fixture_path, '{}.json'.format(block_hash))) as block_file:
    get_block_hashes = {
      block_hash: json.loads(block_file.read())
    }

def get_block(hash):
  if hash is None:
    return None

  if hash in get_block_hashes:
    return get_block_hashes.get(hash)

  if len(get_block_hashes) > 100:
    del get_block_hashes[list(get_block_hashes.keys())[0]]

  get_response = requests.get(
    join(
      blockchaininfo_constants.URL,
      blockchaininfo_constants.RAW_BLOCK,
      hash,
    ),
  )

  json_response = None
  try:
    json_response = json.loads(get_response.text)
  except:
    return None

  get_block_hashes[hash] = json_response

  return json_response

def get_previous_hash(hash):
  block_json = get_block(hash)

  if block_json is None:
    return None

  return block_json.get(blockchaininfo_constants.PREV_BLOCK)

if settings.DEBUG:
  with open(join(fixture_path, 'tx.json')) as transaction_file:
    transactions = json.loads(transaction_file.read())

class Delta():
  def __init__(self, vin_json=None, vout_json=None, out_txid=None):
    if vin_json is not None:
      self.incoming(vin_json)

    if vout_json is not None:
      self.out_txid = out_txid
      self.outgoing(vout_json)

  def incoming(self, vin_json):
    prev_out = vin_json.get(blockchaininfo_constants.PREV_OUT)
    self.value = int(prev_out.get(blockchaininfo_constants.VALUE))

  def outgoing(self, vout_json):
    self.index = int(vout_json.get(blockchaininfo_constants.INDEX))
    self.value = int(vout_json.get(blockchaininfo_constants.VALUE))
    self.addresses = force_array(vout_json.get(blockchaininfo_constants.ADDRESS))

class Transaction():
  def __init__(self, transaction_json):
    self.txid = transaction_json.get(blockchaininfo_constants.HASH)
    self.size = transaction_json.get(blockchaininfo_constants.SIZE)
    self.weight = transaction_json.get(blockchaininfo_constants.WEIGHT)

    self.create_deltas(transaction_json)

  def create_deltas(self, transaction_json):
    self.incoming_deltas = [
      Delta(vin_json=vin_json)
      for vin_json
      in transaction_json.get(blockchaininfo_constants.INPUTS)
      if blockchaininfo_constants.PREV_OUT in vin_json
    ]
    self.outgoing_deltas = [
      Delta(vout_json=vout_json, out_txid=self.txid)
      for vout_json
      in transaction_json.get(blockchaininfo_constants.OUT)
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
  def __init__(self, hash):
    self.hash = hash
    block_json = get_block(hash)

    self.has_failed = False
    if block_json is None:
      self.has_failed = True

    if block_json is not None:
      self.parent = block_json.get(blockchaininfo_constants.PREV_BLOCK)
      self.height = block_json.get(blockchaininfo_constants.HEIGHT)

      self.create_transactions(block_json.get(blockchaininfo_constants.TRANSACTION))

  def create_transactions(self, transactions_json):
    self.transactions = [
      Transaction(transaction_json)
      for transaction_json
      in transactions_json
    ]

  def find_deltas_with_address(self, address):
    deltas = []
    for transaction in self.transactions:
      deltas.extend(transaction.find_deltas_with_address(address))

    return deltas
