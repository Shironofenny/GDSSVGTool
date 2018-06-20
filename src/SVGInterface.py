import svgwrite

class SVGInterface(object):

    def __init__(self, filename = None, size = None):
        self.openFile(filename, size)

    def openFile(self, filename = None, size = None):
        if (filename):
            if (None != size and isinstance(size, tuple)):
                self.svgFile = svgwrite.Drawing(filename=filename, size=size)
            else:
                self.svgFile = svgwrite.Drawing(filename=filename)

    def save(self):
        svgwrite

    