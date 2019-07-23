
import string
import random

def random_string(length):
  return ''.join([random.choice(string.hexdigits) for _ in range(length)])

def random_key():
  return random_string(8)
