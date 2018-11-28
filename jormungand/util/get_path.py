
def get_path(dictionary, path_list):
  value = dictionary
  for item in path_list:
    if not isinstance(value, dict):
      return None

    value = value.get(item)

  return value
