from engine.calculatorFunction import CalculatorFunction
import random 
import math
from engine.const import Number, ShiftMode



class ArithmeticFunction(CalculatorFunction):
    argCount = -1
    fn = lambda *args: 0.0

    @classmethod
    def __exec__(cls, this):
        assert cls.argCount >= 0, f"undefined argCount in class {cls}"
        args   = tuple(reversed(list(this)[:cls.argCount]))
        newX   = cls.fn(*args)
        if cls.argCount <= 1:
            this.setX(newX)
        else:
            this.joinXY(newX)
        

    @classmethod
    def check(cls):
        super().check()
        if cls.fn is ArithmeticFunction.fn:
            print(f"class '{cls}' doesn't have its function defined")
        

class GenerativeFunction(ArithmeticFunction):    
    argCount = 0
    
class UnaryFunction(ArithmeticFunction):    
    argCount = 1
    
class BinaryFunction(ArithmeticFunction):   
    argCount = 2


decimalHours = lambda x: sum([f * h for f, h in zip((1./0.6, 1.0), math.modf(x))]) 
minuteHours  = lambda x: sum([f * h for f, h in zip((0.6, 1.0), math.modf(x))])

ffactorial = lambda x: math.gamma(x + 1.)

CF_randomNumber          = GenerativeFunction.spawn("CF_randomNr",  caption = "RAN #",  fn = random.random)
CF_pi                    = GenerativeFunction.spawn("CF_pi",        caption = "π",      fn = lambda: math.pi)

CF_absoluteValue         = UnaryFunction.spawn("CF_absoluteValue",  caption = "ABS",    fn = abs)
CF_changeSign            = UnaryFunction.spawn("CF_changeSign",     caption = "CHS",    fn = lambda x: -x)
CF_convertToDecimalHours = UnaryFunction.spawn('CF_convertToDecHrs',caption = "→H",     fn = decimalHours)
CF_convertToMinuteHours  = UnaryFunction.spawn('CF_convertToMinHrs',caption = "→H.MS",  fn = minuteHours)
CF_exponentOf10          = UnaryFunction.spawn('CF_exponentOf10',   caption = '10^x',   fn = lambda x: math.pow(10, x))
CF_fraction              = UnaryFunction.spawn('CF_fraction',       caption = 'FRAC',   fn = lambda x: math.modf(x)[0])
CF_integer               = UnaryFunction.spawn('CF_integer',        caption = 'INT',    fn = Number.__trunc__)
CF_reciprokeValue        = UnaryFunction.spawn('CF_reciprokeValue', caption = '1/x',    fn = lambda x: 1/x)
CF_logarithmNatural      = UnaryFunction.spawn('CF_logarithmBaseE', caption = 'LN',     fn = math.log)
CF_logarithmBase10       = UnaryFunction.spawn('CF_logarithmBase10',caption = 'LOG',    fn = math.log10)
CF_factorial             = UnaryFunction.spawn('CF_factorial',      caption = 'x!',     fn = ffactorial)
CF_square                = UnaryFunction.spawn('CF_square',         caption = 'x²',     fn = lambda x: x*x)
CF_sqareRoot             = UnaryFunction.spawn('CF_sqareRoot',      caption = '√x',     fn = math.sqrt)
CF_exponent              = UnaryFunction.spawn('CF_exponent',       caption = 'e^-1',   fn = math.exp)

CF_operatorPlus          = BinaryFunction.spawn('CF_operatorPlus',  caption = '+',      fn = Number.__add__)
CF_operatorMin           = BinaryFunction.spawn('CF_operatorMin',   caption = '-',      fn = Number.__sub__)
CF_operatorMul           = BinaryFunction.spawn('CF_operatorMul',   caption = '×',      fn = Number.__mul__)
CF_operatorDiv           = BinaryFunction.spawn('CF_operatorDiv',   caption = '÷',      fn = Number.__truediv__)
CF_operatorPower         = BinaryFunction.spawn('CF_operatorPower', caption = 'y^x',    fn = lambda y, x: x.__pow__(y))
CF_percentage            = BinaryFunction.spawn('CF_percentage',    caption = '%',      fn = lambda y, x: x * y / 100.)
CF_deltaPercent          = BinaryFunction.spawn('CF_deltaPercent',  caption = 'Δ%',     fn = lambda y, x: 100 * (x - y) / y)


class MemoryOperator(CalculatorFunction):
    
    @classmethod
    def execute(cls, this):
        this.setMemoryOperator(cls.operator)
        return ShiftMode.none
    

CF_memOpPlus            = BinaryFunction.spawn('CF_memOpPlus',  operator = '+')
CF_memOpMin             = BinaryFunction.spawn('CF_memOpMin',   operator = '-')
CF_memOpMul             = BinaryFunction.spawn('CF_memOpMul',   operator = '×')
CF_memOpDiv             = BinaryFunction.spawn('CF_memOpDiv',   operator = '÷')

CalculatorFunction.registerSubclasses()

