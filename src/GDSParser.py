import gdsii.elements
from gdsii.library import Library
from gdsii.elements import *

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

    def read(self, filename = None):
        if (filename):
            with open(filename, 'rb') as gdsfile:
                self.stream = Library.load(gdsfile)

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

    def saveCompressedGDS(self, filename):
        Library.save(filename)

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
    def parse(self, resize = True):
        print("INFO   : Parsing...")
        if len(self.stream) > 1:
            print("WARNING: More than 1 structure has been found. Only the first library will be processed")
            print("         Please confirm that your gds is flattened.")
        _structure = self.stream[0]
        for _element in _structure:
            if (type(_element) is gdsii.elements.Text):
                # Ignore text layers
                pass
            elif (type(_element) is gdsii.elements.Boundary):
                print(_element.layer)
        print("INFO   : Parsing... Done!")