from src import SVGInterface
from src import GDSParser
from src import LayerMap
from src import LayerProcessor
from src import CompGeoTools

layerMap = LayerMap("json/CM018GII.json")

gdsParser = GDSParser()
gdsParser.read("gds/opt_1xinv.gds")
gdsParser.setResizeFactor(5)
gdsParser.loadLayerMap(layerMap)
gdsParser.parse()

layerProcessor = LayerProcessor(layerMap = layerMap, layers = gdsParser.layers)
layerProcessor.processLayers()

layer = layerProcessor.layers['16']

square = layer[0]
print(square)

tools = CompGeoTools()
result = tools.computePolarity(tools.makeEdge(square[0], square[1]), tools.makeEdge(square[0], square[2]))
tools.setPolarity(result)
testPoint = (160,1133)
print(tools.cross2D(tools.makeEdge(square[0], square[1]), tools.makeEdge(square[0], testPoint)))
print(tools.cross2D(tools.makeEdge(square[1], square[2]), tools.makeEdge(square[1], testPoint)))
print(tools.cross2D(tools.makeEdge(square[2], square[3]), tools.makeEdge(square[2], testPoint)))
print(tools.cross2D(tools.makeEdge(square[3], square[4]), tools.makeEdge(square[3], testPoint)))
print(result)

#svgInterface = SVGInterface("output/all.svg", (1200,1200))
#layerProcessor.printLayers(svgInterface = svgInterface)
#svgInterface.save()