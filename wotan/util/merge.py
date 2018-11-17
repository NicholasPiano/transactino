
def merge(*args):
  original, to_merge = args[0], args[1:]

  # merge only the first to_merge
  if to_merge:
    first, rest = to_merge[0], to_merge[1:]

    if first is None:
      return merge(original, *rest)

    if isinstance(original, dict) and isinstance(first, dict):
      for key, value in first.items():
        original.update({key: merge(original.get(key), value)})

      return merge(original, *rest)

    if isinstance(original, list) and isinstance(first, list):
      original.extend(first)
      return merge(original, *rest)

    return merge(first, *rest)

  return original
