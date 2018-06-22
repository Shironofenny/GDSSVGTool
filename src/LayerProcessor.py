# -*- coding: utf-8 -*-
from src.CompGeoTools import CompGeoTools
from shapely.geometry import Polygon
from shapely.ops import unary_union

class LayerProcessor(object):

    def __init__(self, layerMap = None, layers = None):
        self.layerMap = layerMap 
        self.layers = layers
        # State variable that will only be true if both layer map and layers are present
        self.isReady = False
        # Processed layer information
        self.layersToPrint = []
        self.layersToStream = []

    def loadLayerMap(self, layerMap):
        self.layerMap = layerMap
        if self.layerMap and self.layers:
            self.isReady = True
        else:
            self.isReady = False

    def loadLayers(self, layers):
        self.layers = layers
        if self.layerMap and self.layers:
            self.isReady = True
        else:
            self.isReady = False

    '''
    mergeLayer
    IO: layer, a list of paths (each path is a list of points) presenting a list of polygons
        value will be returned within layer, as a list of the maximum possible union of the polygons
    This method should not belong to this class, however, it seems importing scope has some bugs in
    Windows OS. Leaving it here avoids a lot of those kind of bs.
    '''
    def mergeLayer(self, layer):
        # Convert all polygons into shapely.geometry.Polygon
        _sPolygons = []
        for _polygon in layer:
            _sPolygon = Polygon(shell = _polygon)
            _sPolygons.append(_sPolygon)
            try:
                _outPolygons = unary_union(_sPolygons)
            except ValueError as ve:
                print("ERROR  : Adding polygon " + _polygon + " creates problems")
                print("         " + str(ve))
        _outPolygons = unary_union(_sPolygons)
        layer.clear()
        # Return value within layer
        if isinstance(_outPolygons, Polygon):
            _coords = list(_outPolygons.exterior.coords)
            _coordsInt = []
            for _point in _coords:
                _pointInt = (int(_point[0]), int(_point[1]))
                _coordsInt.append(_pointInt)
            layer.append(list(_coordsInt))
        else:
            for _polygon in _outPolygons.geoms:
                _coords = list(_polygon.exterior.coords)
                _coordsInt = []
                for _point in _coords:
                    _pointInt = (int(_point[0]), int(_point[1]))
                    _coordsInt.append(_pointInt)
                layer.append(list(_coordsInt))

    def mergeLayers(self):
        for key in self.layers.keys():
            print("INFO   : Processing layer number " + key)
            self.mergeLayer(self.layers[key])

    def processLayers(self):
        # Merge each layer
        self.mergeLayers()

        # Seperate those that we want to print
        _printLayers = []
        for _layerID in self.layers.keys():
            _layerName = self.layerMap.getLayerInfo(_layerID)["name"]
            _layerAction = self.layerMap.getLayerInfo(_layerID)["action"]
            if _layerAction == "Ignore":
                print("INFO   : Layer " + str(_layerID) + " (" + _layerName + ") is specified to be ignored")
            elif _layerAction == "Print":
                print("INFO   : Layer " + str(_layerID) + " (" + _layerName + ") is specified to be printed")
                _printLayers.append(_layerID)
            else:
                print("WARNING: Layer " + str(_layerID) + " (" + _layerName + ") does not have defined action")
                print("         Action " + _layerAction + " is not defined")
    
        self.layersToPrint = {_layerID : self.layers[_layerID] for _layerID in _printLayers}

    def getPrintLayers(self):
        return self.layersToPrint

    def getStreamLayers(self):
        return self.layersToPrint

    def printLayers(self, svgInterface):
        # Dictionary only preserves order after python 3.6, so we use an
        # alternative ordering method (less efficient for sure) that gives
        # extra backward compatibility
        _layerOrder = list(self.layersToPrint.keys())
        _layerOrder.sort(key = lambda l : self.layerMap.getLayerInfo(l)["printOrder"])
        for _layerID in _layerOrder:
            _paths = self.layersToPrint[_layerID]
            _colorData = self.layerMap.getLayerInfo(_layerID)["color"]
            _fillColor = _colorData["fill"]
            _fillOpacity = _colorData["fillOpacity"]
            _strokeColor = _colorData["stroke"]
            _strokeWidth = _colorData["strokeWidth"]
            _strokeOpacity = _colorData["strokeOpacity"]
            svgInterface.drawLayer(paths = _paths,
                                   fillColor = _fillColor,
                                   fillOpacity = _fillOpacity,
                                   strokeColor = _strokeColor,
                                   strokeWidth = _strokeWidth,
                                   strokeOpacity = _strokeOpacity)
        return
