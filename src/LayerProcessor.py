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
        self.layerPaths = {}
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
    def mergeLayer(self, layer, path):
        # Convert all polygons into shapely.geometry.Polygon
        _sPolygons = []
        for _polygon in layer:
            _sPolygon = Polygon(shell = _polygon).buffer(0)
            _sPolygons.append(_sPolygon)
        try:
            _outPolygons = unary_union(_sPolygons)
        except ValueError as ve:
            print("ERROR  : Cannot merge this layer")
            print("         " + str(ve))
            return

        # Return value within layer
        if isinstance(_outPolygons, Polygon):
            path.append(self.polygonToPath(_outPolygons))
        else:
            for _polygon in _outPolygons.geoms:
                path.append(self.polygonToPath(_polygon))

    def mergeLayers(self):
        for key in self.layers.keys():
            print("INFO   : Processing layer number " + key)
            # Initialize paths for each layer
            self.layerPaths[key] = []
            self.mergeLayer(self.layers[key], self.layerPaths[key])

    '''
    polygonToPath:
        Convert a polygon information into an W3 compatible path information.
        It also rounds the points into its neariest integer
    '''
    def polygonToPath(self, polygon = None):
        if polygon is None:
            return ''
        else:
            # Define the output string for the path definition
            _retVal = ''
            # Assemble the all coords list
            _paths = []
            _paths.append(list(polygon.exterior.coords))
            for _interiorPath in polygon.interiors:
                _paths.append(list(_interiorPath.coords))
            # Process each path
            for _path in _paths:
                _prevPoint = None
                for _point in _path:
                    _xNow = int(_point[0])
                    _yNow = int(_point[1])
                    if _prevPoint is None:
                        _retVal = _retVal + 'M' + str(_xNow) + ',' + str(_yNow) + ' '
                    else:
                        if _xNow == _prevPoint[0]:
                            _retVal = _retVal + 'V' + str(_yNow) + ' '
                        else:
                            _retVal = _retVal + 'H' + str(_xNow) + ' '
                    _prevPoint = (_xNow, _yNow)
            return _retVal

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
    
        self.layersToPrint = {_layerID : self.layerPaths[_layerID] for _layerID in _printLayers}

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
