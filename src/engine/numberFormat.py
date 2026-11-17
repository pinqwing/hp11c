import math 
from enum import Enum
from engine.const import Number
import string

class DisplayMode(Enum):
    default     =-1
    fixed       = 0
    scientific  = 1
    engineering = 2

DIGITS = string.digits + "+- "

class NumberFormat:
    
    def __init__(self, size = 11, decimalSeparator = '.', thousandGrouper = ' ', mode = DisplayMode.fixed, precision = 4):
        self.size       = size
        self.sepDec     = decimalSeparator
        self.sep1000    = thousandGrouper
        self.mode       = mode
        self.precision  = precision

        
    def toString(self, x: Number, precision = -1, mode = DisplayMode.default):
        x = Number(x)
        if precision < 0: precision = self.precision
            
        match mode:
            case DisplayMode.fixed:         result =  self._asFixed(x, precision)
            case DisplayMode.scientific:    result =  self._asScientific(x, precision)
            case DisplayMode.engineering:   result =  self._asEngeneeric(x, precision)
            case _:
                return self.toString(x, precision, self.mode if self.mode != DisplayMode.default 
                                                                        else DisplayMode.fixed)
                
        return result.replace(".", self.sepDec).replace("_", self.sep1000)
        

    def _asFixed(self, x: Number, precision):
        if abs(x) < 1E10: 
            number = f"{x: _.{precision}f}" 
            # lengte moeilijk te bepalen door interpunctie
            count = 0
            for i, c in enumerate(number):
                if c in DIGITS:
                    count += 1
                    if count >= self.size:
                        break 
            return number[:i+1]
            
        return self._asScientific(x, precision)


    def _asScientific(self, x: Number, precision):
        precision   = min(precision, self.size - 4)
        mantisse, exponent = f"{x: .{precision}e}".split('e')
        exponent    = f"{int(exponent): 03d}"
        return self._reformat(mantisse, exponent)


    def _asEngeneeric(self, x: Number, precision):
        s = f"{x:.{precision}e}"
        digits, exponent  = s.split("e")
        exponent    = int(exponent)
        dec         = exponent % 3
        exponent   -= dec
        precision  -= dec 
        exponent    = f"{int(exponent): 03d}"
        mantisse    = f"{float(digits) * (10**dec): .{max(0, precision)}f}"
        return self._reformat(mantisse, exponent)


    def _reformat(self, mantisse: str, exponent: str):
        visible     = sum([1 if c in DIGITS else 0 for c in mantisse])
        hidden      = len(mantisse) - visible
        width       = max(len(mantisse), self.size + hidden - len(exponent))
        return f"{mantisse:<{width}}{exponent}"     
    

class EnterExponent(NumberFormat):    

    def __init__(self, mantisse, *args, **kwargs):
        super().__init__(*args, **kwargs)
        width         = self.size -3
        self.mantisse = f"{mantisse:< {width}}"     
        
    def toString(self, exponent: int, *ignored, **alsoIgnored):
        exponent    = f"{int(exponent): 03d}"
        return self._reformat(str(self.mantisse), exponent)


if __name__ == '__main__':
    pi = math.pi
            
    def xprint(fmt, x):    
        r = fmt.toString(x)
        d = ""
        n = 0
        b = ["|"]*11
        p = [" "]*11
        for c in r:
            if c in DIGITS:
                p[n] = c
                n += 1
            else:
                b[n] = c
                
                
        d = '[' + ("".join([c[0] + c[1] for c in zip(p, b)]))[:-1] + ']'
            
        # print(x)
        print(d, " ...", f">{r}<", n)
        # print(f">{r}<")
        # print(f">12345678901<\n")
        
        
        
    def test(mode, x):
        fmt = NumberFormat(mode=mode, precision = 4, thousandGrouper='')
        print(f"\n*** {mode.name}")
        for i in range(1, 21, 4):
            xprint(fmt, (x / 10**i))

    
    t = 123456789
    for mode in DisplayMode:
        test(mode, t)
        
    
    print("\n***", "exponent")
    fmt = EnterExponent(123)
    xprint(fmt, 45)
    xprint(fmt, -45)
    fmt = EnterExponent(-123456)
    xprint(fmt, 45)
    xprint(fmt, -45)