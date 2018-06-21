from src.SVGInterface import SVGInterface
from src.GDSParser import GDSParser
from src.LayerMap import LayerMap

layerMap = LayerMap("json/CM018GII.json")

gdsParser = GDSParser()
gdsParser.read("gds/opt_1xinv.gds")
gdsParser.setResizeFactor(5)
gdsParser.parse()

gdsParser.loadLayerMap(layerMap)