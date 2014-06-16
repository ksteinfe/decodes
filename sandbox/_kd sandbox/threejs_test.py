import decodes
from decodes.core import *

out = decodes.make_out(decodes.Outies.ThreeJS,"myscene","C:\\")
out.put(Point(2,2,4))
out.draw()

# {
# "metadata":{"version":4.3, "type":"Object","generator":"ObjectExporter"},
# "geometries": [{ "uuid": "Some number", "x":  , "y":  , "z":  }],
# "materials":[{}],
# "object":{ , , ,"children":[{},{}]}
# }
