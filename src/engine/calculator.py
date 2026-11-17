import string
from engine.stack import Stack, Memory
from engine.arithmeticFunction import *
from engine.stackFunction import *
from enum import Enum

from engine.calculatorFunction import CF_switchOn
from engine.buttonFunction import ButtonFunctions
from engine import AngularMode, ShiftMode
from engine.numberFormat import NumberFormat, DisplayMode, EnterExponent

class HP11C(Stack):
    QUIT  = "$quit application"
    DEBUG = "$debugger"


    def __init__(self):
        super().__init__()
        self.decimals       = 4
        self.buttons        = ButtonFunctions()
        self.userInput      = ""
        self.userExpnt      = "0"
        self.memory         = Memory(20)
        self.receivingInput = False
        self.displays       = [NumberFormat(11, "."),]
        self.displayMode    = DisplayMode.fixed
        self.shiftMode      = ShiftMode.plain
        self.angularMode    = AngularMode.radians
        
        
    display = property(lambda c: c.displays[0])
    # displayMode = property(lambda c: c.display.mode, lambda c, m: setattr(c.display, "mode", m))
        

    def execute(self, function):
        
        if function.numeric:
            if not self.receivingInput:
                self.enter()
        self.receivingInput = function.numeric
        
        mode = function.execute(self)
        self.setShiftMode(mode)
        

    def getX(self, input = False):
        if self.receivingInput or input:
            try:    result = float(self.userInput) * 10**int(self.userExpnt)
            except: result = 0.
        else:
            result = super().getX()
        return result
    
     
    def setAngularMode(self, mode: AngularMode):
        self.angularMode = mode
    
    
    def setDisplayMode(self, mode: DisplayMode):
        self.displayMode  = mode
        self.display.mode = mode
        
        
    def setShiftMode(self, mode: ShiftMode):
        if mode != ShiftMode.none:
            self.shiftMode = mode if mode != self.shiftMode else ShiftMode.plain
            
            match self.shiftMode :
                case ShiftMode.store | ShiftMode.recall:
                    self.memory.setIntention(self.shiftMode) 

                case ShiftMode.exponent:
                    if abs(self.x) < 1e7: # hardware limit
                        try:        mantisse = eval(self.userInput)
                        except:     mantisse = 1
                        self.displays.insert(0, EnterExponent(mantisse, 11, "."))
                        self.setX(0)
                 
                case ShiftMode.plain: 
                    while len(self.displays) > 1:
                        self.displays.pop(0)
                        if self.userExpnt != 0:
                            self.x = self.getX(input=True)

                
    
    def setMemoryOperator(self, operator: str):
        self.memory.operator = operator
        
        
    def toRadians(self, value):
        return self.angularMode.toRadians(value)
            
            
    def fromRadians(self, value):
        return self.angularMode.fromRadians(value)
            
            
    def addToInput(self, s):
        match self.shiftMode:
            
            case ShiftMode.store:
                if self.memory.handleInput(s):
                    self.memory.store(self.x)
                    self.setShiftMode(ShiftMode.plain)
                    
            case ShiftMode.recall:
                if self.memory.handleInput(s):
                    self.enter(self.memory.recall())
                    self.setShiftMode(ShiftMode.plain)
                    
            case ShiftMode.exponent:
                if s == chr(8):
                    self.userExpnt = self.useruserExpnt[:-1]
                else:
                    self.userExpnt += str(s)
                self.userExpnt = self.userExpnt[-2:]
                self.setX(self.userExpnt)
                
            case _:
                if s == chr(8):
                    self.userInput = self.userInput[:-1]
                else:
                    self.userInput += str(s)
                self.setX(float(self.userInput))
     
     
    def store(self, index):
        self.memory[index] = self.x
        
        
    def recall(self, index):
        self.enter(self.memory[index])
        
        
    def clearReg(self):
        self.memory.clear()
        

    def clearSigma(self):
        for i in range(6):
            self.memory[i] = 0.0
        self.clearStack()
        
         
    def currentDisplay(self):   
        return self.display.toString(self.x, self.decimals)

    
    def calculatorKey(self, tag):
        button   = self.buttons.get(tag)
        function = button.getFunction(self.shiftMode)
        if function == CF_switchOn:
            return self.QUIT
        else: 
            self.execute(function)
            return self.currentDisplay()

    
    def keyboardKey(self, key, code, shiftKey, ctrlKey, altKey):
        if key in string.digits + ".":
            return self.calculatorKey(key)
        
        else:
            function = CalculatorFunction.find(key) # todo: shiftmode
            if function is not None:
                self.execute(function)
                return self.currentDisplay()
    
    
        

        