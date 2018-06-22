import gdsii.elements
from gdsii.library import Library
from gdsii.elements import Text, Boundary

class GDSParser(object):

    def __init__(self, filename = None):
        self.stream = None
        self.streamout = None
        self.read(filename = filename)
        # Scale factor of the gds
        self.resizeFactor = 1
        # The coordinate range this gds file occupies
        # Bottom left = blcorner
        # Top right = trcorner
        # They are both initialized to be zero
        self.blcorner = (0,0)
        self.trcorner = (0,0)
        # This gds has not been parsed yet
        self.isParsed = False
        # The layer map
        self.layerMap = None
        # The dictionary for all layers
        self.layers = None
        # Flag for if a valid layer map is available
        self.isLayerMapValid = False

    def read(self, filename = None):
        if (filename):
            with open(filename, 'rb') as gdsfile:
                self.stream = Library.load(gdsfile)

    def loadLayerMap(self, layerMap):
        self.layerMap = layerMap
        _keys = layerMap.getMap()["layers"].keys()
        self.layers = {x : [] for x in _keys}
        self.isLayerMapValid = True

    '''
    Setting the resize factor.
    I : resizeFactor, the division factor to resize the gds file
    O : N/A
    Just an alternative way to call resizing before parsing
    The resize process will not happen unless you call parse()
    You can also pass the resize factor there so it is kind of redundant
    '''
    def setResizeFactor(self, resizeFactor):
        self.resizeFactor = resizeFactor

    '''
    '''
    def iteratePoints(self, path, resize = False):
        # Initialize output path variable
        _path = []
        for point in path:
            if resize:
                if (point[0] % resize is 0 and point[1] % resize is 0):
                    pass
                else:
                    print("WARNING: Point not divisible by " + str(resize) + " found at ( " + str(point[0]) + ", " + str(point[1]) + ")")
                _point = (int(point[0] / resize), int(point[1] / resize))
            else:
                _point = (point[0], point[1])
            
            # Update canvas corner information
            if (_point[0] < self.blcorner[0]):
                self.blcorner = (_point[0], self.blcorner[1])
            if (_point[0] > self.trcorner[0]):
                self.trcorner = (_point[0], self.trcorner[1])
            if (_point[1] < self.blcorner[1]):
                self.blcorner = (self.blcorner[0], _point[1])
            if (_point[1] > self.trcorner[1]):
                self.trcorner = (self.trcorner[0], _point[1])
            
            # Pushing point into path
            _path.append(_point)
        
        return _path

    '''
    '''
    def saveGDS(self, filename):
        self.streamout.save(filename)

    '''
    Parsing method.
    I : resize, if set to be True, it will resize the gds using pre-defined resize factor
        If set to be an integer, it will resize using this integer, and update the resize factor
        Should return error, if set to anything else
    O : N/A
    During the parsing process, self.isParsed will be set, and the following functions will produce
    meaningful results:
        self.getCanvasSize()
        self.
    '''
    def parse(self, resize = True, layerMap = None):
        print("INFO   : Parsing GDSII stream...")

        # Processing resizing information
        _resize = resize
        if (_resize is 1 or (resize is True and self.resizeFactor is 1)):
            print("INFO   : Resize factor not set, or set to be 1. Output will preserve the scale of the initial gds file")
            _resize = False
        else:
            _resize = self.resizeFactor
        # From now on, _resize should be used as resize factor

        # Processing layer map information
        if layerMap:
            self.loadLayerMap(layerMap)
        
        if not self.isLayerMapValid:
            print("ERROR  : No valid layer map found. Aborting parsing process")
            return
        # self.layerMap should be ready from now, and self.layers should be initialized to empty lists

        # Sort polygons on each layer into self.layers
        if len(self.stream) > 1:
            print("WARNING: More than 1 structure has been found. Only the first library will be processed")
            print("         Please confirm that your gds is flattened.")
        _structure = self.stream[0]
        for _element in _structure:
            if (type(_element) is Text):
                # Ignore text layers
                pass
            elif (type(_element) is Boundary):
                # Sort _elements to different layers
                try:
                    _path = self.iteratePoints(_element.xy, _resize)
                    self.layers[str(_element.layer)].append(_path)
                except KeyError as ke:
                    print("Error  : Layer number " + str(ke) + " cannot be found in layer map.")
                    print("       : Please check your layer map file.")
        
        print("INFO   : Reporting GDS Size")
        print("         Bottom left corner " + str(self.blcorner))
        print("         Top right corner " + str(self.trcorner))

        print("INFO   : Done parsing GDSII stream!")