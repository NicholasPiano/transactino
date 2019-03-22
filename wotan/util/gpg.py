
import re
import os
import uuid
from os.path import join, exists
from subprocess import Popen, PIPE
from binascii import hexlify

class gpg_constants:
  LONG_KEY_ID = 'long_key_id'
  STATUS = 'status'

class status_constants:
  UNCHANGED = 'unchanged'
  IMPORTED = 'imported'

class command_constants:
  IMPORT = '--import'
  OUTPUT = '--output'
  ENCRYPT = '--encrypt'
  DECRYPT = '--decrypt'
  RECIPIENT = '--recipient'
  ARMOR = '--armor'

class Imported:
  def __init__(self, long_key_id=None, status=None):
    self.long_key_id = long_key_id
    self.status = status
    self.is_valid = long_key_id is not None and status is not None

class GPG:
  def __init__(self, binary=None, path=None):
    self.binary = binary
    self.home_path = path

    self.key_path = join(path, 'keys')
    if not exists(self.key_path):
      os.mkdir(self.key_path)

    self.encrypt_path = join(path, 'encrypt')
    if not exists(self.encrypt_path):
      os.mkdir(self.encrypt_path)

    self.encrypted_path = join(path, 'encrypted')
    if not exists(self.encrypted_path):
      os.mkdir(self.encrypted_path)

    self.decrypt_path = join(path, 'decrypt')
    if not exists(self.decrypt_path):
      os.mkdir(self.decrypt_path)

    self.decrypted_path = join(path, 'decrypted')
    if not exists(self.decrypted_path):
      os.mkdir(self.decrypted_path)

    self.pubring_path = join(path, 'pubring.gpg')
    self.secring_path = join(path, 'secring.gpg')

  def _run_command(self, *args):
    command = [
      self.binary,
      '--homedir', self.home_path,
      '--keyring', self.pubring_path,
      '--secret-keyring', self.secring_path,
      '--trust-model', 'always',
      *args,
    ]

    p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()

    return err.decode('utf-8')

  def import_key(self, key_data):

    unique_id = uuid.uuid4().hex
    asc_file_name = '{}.asc'.format(unique_id)
    asc_file_path = join(self.key_path, asc_file_name)

    with open(asc_file_path, 'w+') as asc_file:
      asc_file.write(key_data)

    output = self._run_command(command_constants.IMPORT, asc_file_path)

    long_key_id_pattern = r'key (?P<long_key_id>[0-9A-Z]+):'
    long_key_id_search = re.search(long_key_id_pattern, output)
    long_key_id = (
      long_key_id_search.groupdict().get(gpg_constants.LONG_KEY_ID)
      if long_key_id_search is not None
      else None
    )

    status_pattern = r'(?P<status>(imported|unchanged)): 1'
    status_search = re.search(status_pattern, output)
    status = (
      status_search.groupdict().get(gpg_constants.STATUS)
      if status_search is not None
      else None
    )

    os.remove(asc_file_path)

    return Imported(long_key_id=long_key_id, status=status)

  def encrypt_to_public_with_long_key_id(self, content=None, long_key_id=None):
    encrypt_id = uuid.uuid4().hex
    encrypt_path = join(self.encrypt_path, encrypt_id)
    with open(encrypt_path, 'w+') as encrypt_file:
      encrypt_file.write(content)

    encrypted_path = join(self.encrypted_path, '{}.gpg'.format(encrypt_id))

    output = self._run_command(
      command_constants.OUTPUT, encrypted_path,
      command_constants.ENCRYPT,
      command_constants.RECIPIENT, long_key_id,
      command_constants.ARMOR,
      encrypt_path,
    )

    encrypted_message = None
    with open(encrypted_path, 'rb') as encrypted_file:
      encrypted_message = encrypted_file.read().decode()

    return encrypted_message

  def decrypt_from_private(self, content):
    decrypt_id = uuid.uuid4().hex
    decrypt_path = join(self.decrypt_path, decrypt_id)
    with open(decrypt_path, 'w+') as decrypt_file:
      decrypt_file.write(content)

    decrypted_path = join(self.decrypted_path, '{}.gpg'.format(decrypt_id))

    output = self._run_command(
      command_constants.OUTPUT, decrypted_path,
      command_constants.DECRYPT,
      decrypt_path,
    )

    error_state = (
      'no valid OpenPGP data found' in output
    )

    if error_state:
      return None

    decrypted_message = None
    with open(decrypted_path, 'r') as decrypted_file:
      decrypted_message = decrypted_file.read()

    return decrypted_message
