
from util.is_valid_datetime import is_valid_datetime
from util.is_valid_uuid import is_valid_uuid
from util.is_valid_ip_address import is_valid_ip_address

from .constants import constants

class Type():
  description = None
  schema = None

  def __init__(self, description=None, schema=None):
    self.description = description or self.description
    self.schema = schema or self.schema

  def __eq__(self, other):
    return self.code == other.code

  def validate(self, value):
    return False

  def render(self):
    rendered = {
      constants.TYPE: self.type,
      constants.DESCRIPTION: self.description,
    }

    if self.schema is not None:
      rendered.update({
        constants.SCHEMA: self.schema.respond().render(top=False),
      })

    return rendered

class Boolean(Type):
  code = '001'
  description = 'A true or false value'
  type = '__boolean'

  def validate(self, value):
    return isinstance(value, bool)

class Integer(Type):
  code = '002'
  description = 'A whole number value'
  type = '__integer'

  def validate(self, value):
    return isinstance(value, int)

class PositiveInteger(Type):
  code = '003'
  description = 'A whole number value greater than zero'
  type = '__positiveinteger'

  def validate(self, value):
    return isinstance(value, int) and value >= 0

class Float(Type):
  code = '004'
  description = 'A floating point number value'
  type = '__float'

  def validate(self, value):
    return value == 0 or isinstance(value, float)

class String(Type):
  code = '005'
  description = 'A string of characters'
  type = '__string'

  def validate(self, value):
    return isinstance(value, str)

class Structure(Type):
  code = '006'
  description = 'A JSON object'
  type = '__structure'

  def validate(self, value):
    return isinstance(value, dict)

class Array(Type):
  code = '007'
  description = 'A JSON array'
  type = '__array'

  def validate(self, value):
    return isinstance(value, list)

class UUID(Type):
  code = '008'
  description = 'A valid UUID'
  type = '__uuid'

  def validate(self, value):
    return is_valid_uuid(value)

class IpAddress(Type):
  code = '0081'
  description = 'A valid IPv4 address'
  type = '__ip'

  def validate(self, value):
    return is_valid_ip_address(value)

class Time(Type):
  code = '009'
  description = (
    'A valid timestamp - either an integer timestamp'
    ' or a string that formats to a valid datetime.'
  )
  type = '__datetime'

  def validate(self, value):
    if not (isinstance(value, int) or isinstance(value, str)):
      return False

    return is_valid_datetime(value)

class Model(Type):
  pass

class Ref(Type):
  code = '011'
  description = 'A string composed of a model name and uuid separated by a point'
  type = '__ref'

  def validate(self, value):
    if isinstance(value, str):
      split_value = value.split('.')
      if len(split_value) == 2:
        [model_name, uuid_value] = split_value
        return is_valid_uuid(uuid_value)
    return False

class Enum(Type):
  def __init__(self, *options):
    self.options = options

class Immutable(Type):
  pass

class Any(Type):
  code = '014'
  description = 'Any value'
  type = '__any'

  def validate(self, value):
    return True

class Null(Type):
  code = '015'
  description = 'Null value'
  type = '__null'

  def validate(self, value):
    return value == constants.NULL

class types:
  BOOLEAN = Boolean
  MODEL = Model
  STRUCTURE = Structure
  ARRAY = Array
  INTEGER = Integer
  POSITIVE_INTEGER = PositiveInteger
  FLOAT = Float
  STRING = String
  UUID = UUID
  IP_ADDRESS = IpAddress
  TIME = Time
  REF = Ref
  ENUM = Enum
  IMMUTABLE = Immutable
  ANY = Any
  NULL = Null

def map_type(type_to_map):
  type_map = {
    'CharField': types.STRING(),
    'DateTimeField': types.TIME(),
    'BooleanField': types.BOOLEAN(),
    'UUIDField': types.UUID(),
    'TextField': types.STRING(),
    'PositiveIntegerField': types.POSITIVE_INTEGER(),
    'FloatField': types.FLOAT(),
    'BigIntegerField': types.INTEGER(),
  }

  return type_map.get(type_to_map)
