import sys

# https://stackoverflow.com/a/34482761/1040915, with some changes
def progressbar(it, prefix="Computing: ", size=60, file=sys.stdout, count=None):
  """
  `count` lets you define how many items to expect without having to rely on `len`
  (e.g. if you want to use a generator which will still have a known size)
  """
  if count is None:
    count = len(it)
  def show(j):
    x = int(size*j/count)
    file.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), j, count))
    file.flush()
  show(0)
  for i, item in enumerate(it):
    yield item
    show(i+1)
  file.write("\n")
  file.flush()
