
from util.blockchaininfo import get_latest_block_hash, Block

def match_delta(payment, delta):
  return payment.full_btc_amount == delta.value

def process_payment(payment, block):
  if block.hash is None:
    return

  deltas = block.find_deltas_with_address(payment.address.value)

  for delta in deltas:
    if match_delta(payment, delta):
      payment.close(block.hash, delta.out_txid, delta.index)
      return

class WithPaymentCheck:
  def check_payments(self):
    latest_block_hash = get_latest_block_hash()
    block = Block(latest_block_hash)

    for payment in self.filter(is_open=True):
      process_payment(payment, block)
