from src import SVGInterface
from src import GDSParser
from src import LayerMap
from src import LayerProcessor

layerMap = LayerMap("json/CM018GII.json")

gdsParser = GDSParser()
gdsParser.read("gds/assem_OTP_AMP_NVC_flat.gds")
gdsParser.setResizeFactor(5)
gdsParser.loadLayerMap(layerMap)
gdsParser.parse()

layerProcessor = LayerProcessor(layerMap = layerMap, layers = gdsParser.layers)
layerProcessor.mergeLayer(layerProcessor.layers["2"])
#layerProcessor.processLayers()

#svgInterface = SVGInterface("output/assem_flatv2.svg", (166000,148000))
#layerProcessor.printLayers(svgInterface = svgInterface)
#svgInterface.save()