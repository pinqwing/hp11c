import inspect
import re
from engine.const import AngularMode, ShiftMode


class fancytype(type):
    
    def __str__(cls):  # @NoSelf
        # class to string behaviour
        try:
            return cls.__className__()
        except AttributeError:            
            return cls.__name__            

    
    def __className__(cls): # @NoSelf
        return f"{cls.__name__}"            
        

    def spawn(cls, name, **kwargs):  # @NoSelf
        # quickly create simple subclass
        kwargs.update(dict(className = name))
        return type(f"{cls} -> {name}", (cls,), kwargs)




class CalculatorFunction(metaclass = fancytype):
    _subclasses_ = {}
    numeric      = False
     
    @classmethod
    def registerSubclasses(cls):
        module = inspect.getmodule(inspect.stack()[1].frame)
        for _, member in inspect.getmembers(module, inspect.isclass):
            if issubclass(member, cls):
                cls._subclasses_[member.getCaption().upper()] = member
        
        
    @classmethod
    def getCaption(cls):
        caption = cls.caption if hasattr(cls, "caption") else cls.__doc__
        if caption is None: caption = ""
        
        return str(re.sub(r"\^(.+)", r"<sup>\1</sup>", str(caption)))


    @classmethod
    def retVal(cls):
        return ShiftMode.plain

        
    @classmethod
    def execute(cls, this):
        cls.__exec__(this)
        return cls.retVal()
    
    
    @classmethod
    def __exec__(cls, this): ...


    @classmethod
    def find(cls, caption):
        return cls._subclasses_.get(caption.upper())
            
            
    @classmethod
    def check(cls):
        if not cls.getCaption():
            print(f"class '{cls}' doesn't have its caption defined ")


class XF_NOP(CalculatorFunction): # No Operation: null pattern
    caption = ""
    @classmethod
    def __exec__(cls, this): pass
    
    
# ---------------------------------------------------------------------------------------------------------------------

class CF_enter(CalculatorFunction):
    caption = "ENTER"

    @classmethod
    def __exec__(cls, this):
        this.enter()
        

class NumberKey(CalculatorFunction): 
    numeric = True
    
    @classmethod
    def __exec__(cls, this):
        value = cls.value if hasattr(cls, "value") else cls.caption 
        this.addToInput(value)

    
CF_number_0     = NumberKey.spawn("CF_number_0",        caption = "0")
CF_number_1     = NumberKey.spawn("CF_number_1",        caption = "1")
CF_number_2     = NumberKey.spawn("CF_number_2",        caption = "2")
CF_number_3     = NumberKey.spawn("CF_number_3",        caption = "3")
CF_number_4     = NumberKey.spawn("CF_number_4",        caption = "4")
CF_number_5     = NumberKey.spawn("CF_number_5",        caption = "5")
CF_number_6     = NumberKey.spawn("CF_number_6",        caption = "6")
CF_number_7     = NumberKey.spawn("CF_number_7",        caption = "7")
CF_number_8     = NumberKey.spawn("CF_number_8",        caption = "8")
CF_number_9     = NumberKey.spawn("CF_number_9",        caption = "9")
CF_decimalPoint = NumberKey.spawn("CF_decimalPoint",    caption = ".")
CF_backarrow    = NumberKey.spawn("CF_backarrow",       caption = "←", value = chr(8))
    

class UserKey(CalculatorFunction): pass
CF_userKeyA = UserKey.spawn("CF_userKeyA", caption = "A")
CF_userKeyB = UserKey.spawn("CF_userKeyB", caption = "B")
CF_userKeyC = UserKey.spawn("CF_userKeyC", caption = "C")
CF_userKeyD = UserKey.spawn("CF_userKeyD", caption = "D")
CF_userKeyE = UserKey.spawn("CF_userKeyE", caption = "E")
    

class ShiftKey(CalculatorFunction): 
    @classmethod
    def retVal(cls):
        return cls.mode
    
        
CF_shiftF               = ShiftKey.spawn("CF_shiftF",           caption = "f",      mode = ShiftMode.fMode)
CF_shiftG               = ShiftKey.spawn("CF_shiftG",           caption = "g",      mode = ShiftMode.gMode)
CF_hyperbolic           = ShiftKey.spawn("CF_hyperbolic",       caption = "HYP",    mode = ShiftMode.hyperbole)
CF_hyperbolicInv        = ShiftKey.spawn("CF_hyperbolicInv",    caption = "HYP^-1", mode = ShiftMode.hyper_inv)
CF_storeValue           = ShiftKey.spawn("CF_storeValue",       caption = "STO",    mode = ShiftMode.store)
CF_recallValue          = ShiftKey.spawn("CF_recallValue",      caption = "RCL",    mode = ShiftMode.recall)
CF_enterExponent        = ShiftKey.spawn("CF_enterExponent",    caption = "EEX",    mode = ShiftMode.exponent)



class SetAngularMode(CalculatorFunction):
    @classmethod
    def __exec__(cls, this): this.setAngularMode(cls.mode)
    
CF_angleModeDegrees     = SetAngularMode.spawn("CF_angleModeDegrees", caption = "DEG", mode = AngularMode.degrees)
CF_angleModeRadians     = SetAngularMode.spawn("CF_angleModeRadians", caption = "RAD", mode = AngularMode.radians)
CF_angleModeGrades      = SetAngularMode.spawn("CF_angleModeGrades",  caption = "GRD", mode = AngularMode.grades)
    
_lastX      = lambda this: this.lastX()
_clearX     = lambda this: this.setX(0)
_clearReg   = lambda this: this.clearReg()
_clearStat  = lambda this: this.clearSigma()

CF_switchOn             = CalculatorFunction.spawn("CF_switchOn",           caption = "ON")
CF_lastX                = CalculatorFunction.spawn("CF_lastX",              caption = "LSTx", __exec__ = _lastX)
CF_clearX_Register      = CalculatorFunction.spawn("CF_clearX_Register",    caption = "CLx",  __exec__ = _clearX)
CF_clearRegisters       = CalculatorFunction.spawn("CF_clearRegisters",     caption = "REG",  __exec__ = _clearReg)
CF_clearStatistics      = CalculatorFunction.spawn("CF_clearStatistics",    caption = "Σ",    __exec__ = _clearStat)
CF_notationModeEng      = CalculatorFunction.spawn("CF_notationModeEng",    caption = "ENG")
CF_notationModeFix      = CalculatorFunction.spawn("CF_notationModeFix",    caption = "FIX")
CF_notationModeSci      = CalculatorFunction.spawn("CF_notationModeSci",    caption = "SCI")
CF_showMantissa         = CalculatorFunction.spawn("CF_showMantissa",       caption = "PREFIX")
CF_round                = CalculatorFunction.spawn("CF_round",              caption = "RND")




        
CalculatorFunction.registerSubclasses()

if __name__ == '__main__':
    import inspect, sys
    
    for name, cls in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if name.startswith("CF_"):
            print (f"""
    def test_{name}(self):
        clc = self.calculator()
        clc.execute(FN_NOP)
            """)