
from util.blockchaininfo import get_latest_block_hash, Block

def match_delta(payment, delta):
  return payment.full_btc_amount == delta.value

def process_payment(payment, block):
  if block.hash is None or block.hash == payment.latest_block_hash:
    return

  payment.latest_block_hash = block.hash
  payment.save()

  deltas = block.find_deltas_with_address(payment.address.value)

  for delta in deltas:
    if match_delta(payment, delta):
      payment.close(block.hash, delta.txid)

class WithPaymentCheck:
  def check_payments(self):
    latest_block_hash = get_latest_block_hash()
    block = Block(latest_block_hash)

    for payment in self.filter(is_open=True):
      process_payment(payment, block)
