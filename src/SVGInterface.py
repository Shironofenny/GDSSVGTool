import svgwrite
from svgwrite.shapes import Rect, Polygon
from svgwrite.path import Path

class SVGInterface(object):

    def __init__(self, filename = None, size = None):
        self.svgFile = None
        self.openFile(filename, size)

    def openFile(self, filename = None, size = None):
        if (filename):
            if (None != size and isinstance(size, tuple)):
                self.svgFile = svgwrite.Drawing(filename=filename, size=size)
            else:
                self.svgFile = svgwrite.Drawing(filename=filename)
            self.svgFile.fill(rule='nonzero')

    def drawLayer(self, paths, fillColor = 'black', fillOpacity = 0.5, strokeColor = 'black', strokeWidth = 1, strokeOpacity = 1.0):
        for path in paths:
            _polygon = self.svgFile.add(Path(path))
            _polygon.fill(fillColor, opacity = fillOpacity)
            _polygon.stroke(strokeColor, width = strokeWidth, opacity = strokeOpacity)

    def save(self):
        self.svgFile.save()