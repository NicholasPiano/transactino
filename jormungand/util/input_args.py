
from constants import method_constants

def get_default_arg(arg_input):
  default_input = '{}: '.format(arg_input)

  return input(default_input)

boolean_map = {
  'T': True,
  'F': False,
}

def get_boolean_arg(arg_input):
  boolean_input = '{} (T/F): '.format(arg_input)
  arg_string = input(boolean_input)
  while arg_string and arg_string not in boolean_map:
    arg_string = input(boolean_input)

  return arg_string

type_map = {
  str: get_default_arg,
  bool: get_boolean_arg,
  int: get_default_arg,
  float: get_default_arg,
}

def input_args(config):
  args = {}
  for arg_name, arg_config in config.items():
    arg_input = arg_config.get(method_constants.INPUT)
    arg_type = arg_config.get(method_constants.TYPE)
    arg_method = type_map.get(arg_type)
    arg_string = arg_method(arg_input)

    if arg_string:
      args.update({
        arg_name: arg_type(arg_string),
      })

  return args
