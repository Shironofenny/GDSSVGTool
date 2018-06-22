from enum import Enum

class CompGeoTools(object):

    # Handle case 0 gracefully!
    class Polarity(Enum):
        POS = 1
        NUL = 0
        NEG = -1

    class Position(Enum):
        IN = 1
        ON = 0
        OUT = -1

    def __init__(self):
        self.polarity = CompGeoTools.Polarity.POS
        pass

    '''
    makeEdge
    I : point1, starting point
    I : point2, ending point
    O : edge, a point tuple. A point is a coordinate tuple, so basically edge is a tuple of two tuples
    '''
    def makeEdge(self, point1, point2):
        return (point1, point2)

    '''
    setPolarity
    I : polarity, set which cross product polarity means a point is in a polygon
    '''
    def setPolarity(self, polarity):
        self.polarity = polarity

    '''
    computePolarity
    I : e1, e2, two edges. e1 = P0->P1, e2 = P0->P2, P0, P1, P2 are 3 consecutive points in the polygon path
    O : N/A
    use two edges P0->P1 and P0->P2 to tell which polarity means a point is in a polygon
    '''
    def computePolarity(self, e1, e2):
        _value = self.cross2D(e1, e2)
        if _value is 0:
            print("ERROR  : Polarity cannot be null!")
            return False
        elif _value > 0:
            return CompGeoTools.Polarity.POS
        else:
            return CompGeoTools.Polarity.NEG

    '''
    corss2D
    I : e1, e2, two edges (vectors).
    O : The value of the cross product of the two edges that is perpendicular to the plane of interest
    Calculate the z direction projection of the cross product of e1 and e2, assuming e1 and e2 are confined within x-y plane
    '''
    def cross2D(self, e1, e2):
        x1 = e1[1][0] - e1[0][0]
        y1 = e1[1][1] - e1[0][1]
        x2 = e2[1][0] - e2[0][0]
        y2 = e2[1][1] - e2[0][1]
        return x1*y2 - x2*y1

    '''
    isInPolygon
    I : polygon, the path for the polygon
    I : point, the point for test
    O : 
    '''
    def isInPolygon(self, polygon, point):
        pass