from src import SVGInterface
from src import GDSParser
from src import LayerMap

layerMap = LayerMap("json/CM018GII.json")

gdsParser = GDSParser()
gdsParser.read("gds/opt_1xinv.gds")
gdsParser.setResizeFactor(5)
gdsParser.loadLayerMap(layerMap)
gdsParser.parse()

svgInterface = SVGInterface("output/test.svg", (1200,1200))
svgInterface.drawLayer(gdsParser.layers["13"])
svgInterface.save()