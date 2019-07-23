
def pluck(d, *args):
  return (
    d[arg]
    for arg in args
    if arg in d
  )
