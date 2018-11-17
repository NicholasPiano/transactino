
import random

hexdigits = '0123456789ABCDEF'

def generate_challenge_content():
  return ''.join([random.choice(hexdigits) for i in range(512)])
