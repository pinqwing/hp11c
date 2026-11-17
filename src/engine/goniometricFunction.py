import math
from engine.const import AngularMode
from engine.calculatorFunction import CalculatorFunction
import cmath


class CF_convertToDegrees(CalculatorFunction):
    # radians to decimal degrees from radiansINDEPENDENT of angularMode
    "→DEG"
    @classmethod
    def __exec__(cls, this):
        radians = this.x 
        this.setX(AngularMode.degrees.fromRadians(radians))  # @UndefinedVariable


class CF_convertToRadians(CalculatorFunction):
    # convert decimal degrees to radians INDEPENDENT of angularMode
    "→RAD"
    @classmethod
    def __exec__(cls, this):
        degrees = this.x
        this.setX(AngularMode.degrees.toRadians(degrees))  # @UndefinedVariable
    


    
class GoniometricFunction(CalculatorFunction):
    @classmethod
    def __exec__(cls, this):
        radians = this.toRadians(this.x) 
        newX    = cls.fn(radians)
        this.setX(newX)
        
CF_cosinus      = GoniometricFunction.spawn("cosinus",      caption = "COS",    fn = math.cos)
CF_sinus        = GoniometricFunction.spawn("sinus",        caption = "SIN",    fn = math.sin)
CF_tangens      = GoniometricFunction.spawn("tangens",      caption = "TAN",    fn = math.tan)
        
CF_cosh         = GoniometricFunction.spawn("cosh",         caption = "COSH",   fn = math.cosh)
CF_sinh         = GoniometricFunction.spawn("sinh",         caption = "SINH",   fn = math.sinh)
CF_tanh         = GoniometricFunction.spawn("tanh",         caption = "TANH",   fn = math.tanh)
        
    
    
        
class GoniometricFunctionArc(GoniometricFunction):
    @classmethod
    def __exec__(cls, this):
        radians = cls.fn(this.x)
        this.setX(this.fromRadians(radians))
    
CF_arcCosinus   = GoniometricFunctionArc.spawn("arcCosinus",   caption = "COS^-1",  fn = math.acos)
CF_arcSinus     = GoniometricFunctionArc.spawn("arcSinus",     caption = "SIN^-1",  fn = math.asin)
CF_arcTangens   = GoniometricFunctionArc.spawn("arcTangens",   caption = "TAN^-1",  fn = math.atan)
    
CF_arcCosh      = GoniometricFunctionArc.spawn("arcCosinus",   caption = "COSH^-1", fn = math.acosh)
CF_arcSinh      = GoniometricFunctionArc.spawn("arcSinus",     caption = "SINH^-1", fn = math.asinh)
CF_arcTanh      = GoniometricFunctionArc.spawn("arcTangens",   caption = "TANH^-1", fn = math.atanh)
    
        
        
        
class CF_convertToPolar(CalculatorFunction):
    '→P'
    @classmethod
    def __exec__(cls, this):
        z = complex(this.x, this.y)        
        this.setX(abs(z))
        this.setY(this.fromRadians(cmath.phase(z)))
        
        
    
class CF_convertToCartesian(CalculatorFunction):
    '→R'
    @classmethod
    def __exec__(cls, this):
        z = this.x * cmath.exp(1j * this.toRadians(this.y)) 
        this.setX(z.real)
        this.setY(z.imag)
        
        
    
if __name__ == '__main__':
    import inspect, sys
    
    for name, cls in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if name.startswith("CF_"):
            print (f"""
    def test_{name}(self):
        expected = 0.00
        x, y     = 0, 0
        self.calculator.setY(y)
        self.calculator.setX(x)
        self.calculator.execute({name})
        self.assertAlmostEqual(expected, self.calculator.x, delta = 0.001)
            """)