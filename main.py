<<<<<<< HEAD
from src import SVGInterface
from src import GDSParser
from src import LayerMap
=======
from src.SVGInterface import SVGInterface
from src.GDSParser import GDSParser
from src.LayerMap import LayerMap
from src.LayerProcessor import LayerProcessor
>>>>>>> f52bd238b8f9ef09370033271cf57826dedb9fc3

layerMap = LayerMap("json/CM018GII.json")

gdsParser = GDSParser()
gdsParser.read("gds/opt_1xinv.gds")
gdsParser.setResizeFactor(5)
gdsParser.loadLayerMap(layerMap)
gdsParser.parse()

layerProcessor = LayerProcessor(layerMap = layerMap, layers = gdsParser.layers)
layerProcessor.processLayers()

svgInterface = SVGInterface("output/all.svg", (1200,1200))
layerProcessor.printLayers(svgInterface = svgInterface)
svgInterface.save()