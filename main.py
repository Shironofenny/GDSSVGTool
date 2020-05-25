from src import SVGInterface
from src import GDSParser
from src import LayerMap
from src import LayerProcessor

layerMap = LayerMap("json/CM018GII.json")

gdsParser = GDSParser()
gdsParser.read("gds/inv1.gds")
gdsParser.setResizeFactor(5)
gdsParser.loadLayerMap(layerMap)
gdsParser.parse()

layerProcessor = LayerProcessor(layerMap = layerMap, layers = gdsParser.layers)
#layerProcessor.mergeLayer(layerProcessor.layers["2"])
layerProcessor.processLayers()

svgInterface = SVGInterface("output/inv1.svg")
layerProcessor.printLayers(svgInterface = svgInterface)
svgInterface.save()