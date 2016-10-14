import sys

# True if we are running on Python 3.
PY3 = sys.version_info[0] == 3
PY32 = PY3 and sys.version_info[1] == 2
PY2 = not PY3

try:
    bytes = bytes
except NameError:
    bytes = str

try:
    set = set
except NameError:
    from sets import Set as set
    set = set

try:
    str = str
except NameError:
    str = str

try:
    long = int
except NameError:
    long = int

try:
    chr = chr
except NameError:
    chr = chr
