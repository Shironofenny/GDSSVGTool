# -*- coding: utf-8 -*-
from src.CompGeoTools import CompGeoTools

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
        # double iteration through all the polygons
        _nrPolygon = len(layer)
        for i in range(_nrPolygon):
            # Reconstructing ith polygon's edges
            for j in range(i, _nrPolygon):
                pass

    def mergeLayers(self):
        for layer in self.layers:
            self.mergeLayer(layer)

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
            
        _printLayers.sort(key = lambda l : self.layerMap.getLayerInfo(l)["printOrder"])
        self.layersToPrint = {_layerID : self.layers[_layerID] for _layerID in _printLayers}

    def getPrintLayers(self):
        return self.layersToPrint

    def getStreamLayers(self):
        return self.layersToPrint

    def printLayers(self, svgInterface):
        for _layerID in self.layersToPrint:
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
