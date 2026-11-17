from collections import deque
from engine.const import Number, ShiftMode
import string


class Stack(deque): 
    
    def __init__(self):
        super().__init__(maxlen = 4)
        self.clearStack()
        self._lastX = self.x


    def __str__(self):
        return str(list(self))

        
    def clearStack(self):
        self.clear()
        self.extend([0.0] *4)
        

    def enter(self, newX = None):
        self._lastX = super().pop()
        self.insert(0, self.x if newX is None else Number(newX))

    
    def lastX(self):
        super().pop()
        self.insert(0, self._lastX)


    def getX(self):
        return self[0]
    
    
    def setX(self, value):
        self._lastX = self.x
        self[0]     = Number(value)
        
        
    def setY(self, value):
        self[1]     = Number(value)
        
        
    def joinXY(self, newXvalue):
        self.pop()
        self.setX(newXvalue)

    
    def pop(self, n=1):
        result = []
        for _ in range(n):
            result.append(self.popleft())
            self.append(self.z)
        return result


    def rollDown(self):
        self.rotate(-1)

        
    def rollUp(self):
        self.rotate(+1)


    def swap(self):
        self.insert(1, self.popleft())


    x = property(getX, setX)
    y = property(lambda s: s[1])
    z = property(lambda s: s[2])
    t = property(lambda s: s[3])



class Memory():
    def __init__(self, size = 100):
        self.__items__ = {i: 0.000 for i in range(size)}
        self.setIntention(ShiftMode.none)
        

    def __setitem__(self, key, value):
        if key not in self.__items__:
            raise KeyError(f"Not a memory register: '{key}'")
        else:
            self.__items__[key] = Number(value)    
            
            
    def __getitem__(self, key):
        if key not in self.__items__:
            raise KeyError(f"Not a memory register: '{key}'")
        else:
            return self.__items__[key]    
            
            
    def clear(self):
        for k in self.__items__:
            self.__items__[k] = 0.000
    
    
    def setIntention(self, mode: ShiftMode):
        self.operation = mode
        self.operator  = '='
        self.index     = 0

    
    def handleInput(self, s: str):
        if s in string.digits:
            self.index += int(s)
            return True
        
        if s == '.':
            self.index = 10
            return False
            
        if s in "÷*-+":
            self.operator = s
            self.index    = 0
            return False
        
            
    def recall(self):
        index = self.index
        self.setIntention(ShiftMode.none)
        return self[index]
            
    
    def store(self, x):
        index = self.index
        match self.operator:
            case '=':   self[index]  = x
            case '+':   self[index] += x
            case '-':   self[index] -= x
            case '*':   self[index] *= x
            case '÷':   self[index] /= x
        self.setIntention(ShiftMode.none)
            
    
    
class UserInput:
    
    def __init__(self):
        self.mantisse = ""
        self.exponent = 0
        self.expInput = False
        
        
    def getValue(self):
        try:        
            return eval(self.mantisse) * (10**self.exponent)
        except SyntaxError:
            return -999999.999999
        
        
    def addCharacter(self, s):
        if self.expInput:        
            if s == chr(8):
                self.exponent //= 10
            else:
                self.exponent = (10 % int(s)) % 100

        else:                
            if s == chr(8):
                self.mantisse = self.mantisse[:-1]
            else:
                self.mantisse += str(s)
        
