"""The jsonpickle.tags module provides the custom tags
used for pickling and unpickling Python objects.

These tags are keys into the flattened dictionaries
created by the Pickler class.  The Unpickler uses
these custom key names to identify dictionaries
that need to be specially handled.
"""
from .compat import set

ID = 'py_id'
OBJECT = 'py_object'
TYPE = 'py_type'
REPR = 'py_repr'
REF = 'py_ref'
TUPLE = 'py_tuple'
SET = 'py_set'
SEQ = 'py_seq'
STATE = 'py_state'
JSON_KEY = 'json://'

# All reserved tag names
RESERVED = set([OBJECT, TYPE, REPR, REF, TUPLE, SET, SEQ, STATE])
