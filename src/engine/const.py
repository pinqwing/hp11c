from enum import Enum
import math


Number  = float


class AngularMode(Enum):
    radians     = "rad",    1.0
    degrees     = "deg",    180/math.pi
    grades      = "grad",   200 / math.pi
    
    def getCaption(self):
        return self.value[0]
    
    def toRadians(self, angle):
        return angle / self.value[1] 
    
    def fromRadians(self, angle):
        return angle * self.value[1] 
    
    @classmethod
    def degreesForAll(cls, degrees):
        rad = cls.degrees.toRadians(degrees)
        return rad, degrees, cls.grades.fromRadians(rad)

    
    
class ShiftMode(Enum):
    none        = -1
    plain       = 0
    fMode       = 1     
    gMode       = 2
    hyperbole   = 4     # HYP   [function]
    hyper_inv   = 5     # HYP-1 [function]
    decimals    = 6     # FIX/SCI.ENG [#]
    exponent    = 7
    store       = 10
    recall      = 20
    
    
    def index(self):
        match self:
            case ShiftMode.fMode: return 0    
            case ShiftMode.plain: return 1    
            case ShiftMode.gMode: return 2    
        return -99999

