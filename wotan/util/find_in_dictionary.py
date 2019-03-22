
def find_in_dictionary(dictionary, path_list=[]):
  if not isinstance(dictionary, dict):
    return None

  if not path_list:
    return dictionary

  first_path, rest = path_list[0], path_list[1:]

  if first_path not in dictionary:
    return None

  child_element = dictionary[first_path]

  if rest:
    return find_in_dictionary(child_element, path_list=rest)

  return child_element
