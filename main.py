from src import SVGInterface
from src import GDSParser
from src import LayerMap

layerMap = LayerMap("json/CM018GII.json")

gdsParser = GDSParser()
gdsParser.read("gds/opt_1xinv.gds")
gdsParser.setResizeFactor(5)
gdsParser.parse()

gdsParser.loadLayerMap(layerMap)