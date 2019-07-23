
def force_array(collection):
  if isinstance(collection, list):
    return collection

  return [collection]
