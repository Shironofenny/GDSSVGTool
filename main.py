from src import SVGInterface
from src import GDSParser
from src import LayerMap

gdsParser = GDSParser()
gdsParser.read("gds/opt_1xinv.gds")
gdsParser.setResizeFactor(5)
gdsParser.parse()

layerMap = LayerMap("json/CM018GII.json")