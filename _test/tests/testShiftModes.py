from engine.const import ShiftMode
from engine.calculator import HP11C

from _testCase import CustomTestCase
from engine import *


class TestShiftModes(CustomTestCase):
        
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        
    def calculator(self, x=0, y=0, z=0, t=0):
        calculator = HP11C()
        for x in (t, z, y, x):
            calculator.enter(x)
        return calculator


    def test_fAndG(self):
        clc = self.calculator()
        self.assertEqual(clc.shiftMode, ShiftMode.plain)
        
        clc.execute(CF_shiftF)
        self.assertEqual(clc.shiftMode, ShiftMode.fMode)
        
        clc.execute(CF_shiftG)
        self.assertEqual(clc.shiftMode, ShiftMode.gMode)
        
        clc.execute(XF_NOP)
        self.assertEqual(clc.shiftMode, ShiftMode.plain)
        
        
        clc.execute(CF_shiftF)
        self.assertEqual(clc.shiftMode, ShiftMode.fMode)
        
        clc.execute(CF_shiftF)
        self.assertEqual(clc.shiftMode, ShiftMode.plain)
        
        
    def test_hyperbole(self):
        clc = self.calculator()
        self.assertEqual(clc.shiftMode, ShiftMode.plain)
        
        clc.execute(CF_shiftF)
        self.assertEqual(clc.shiftMode, ShiftMode.fMode)
        
        clc.execute(CF_hyperbolic)
        self.assertEqual(clc.shiftMode, ShiftMode.hyperbole)
        
        clc.execute(CF_sinh)
        self.assertEqual(clc.shiftMode, ShiftMode.plain)
        
        
    def test_hyper_inv(self):
        clc = self.calculator()
        self.assertEqual(clc.shiftMode, ShiftMode.plain)
        
        clc.execute(CF_shiftF)
        self.assertEqual(clc.shiftMode, ShiftMode.fMode)
        
        clc.execute(CF_hyperbolicInv)
        self.assertEqual(clc.shiftMode, ShiftMode.hyper_inv)
        
        clc.execute(CF_arcSinh)
        self.assertEqual(clc.shiftMode, ShiftMode.plain)
        
    # sto + . 1
        
        
        
        
        
        
        
            
if __name__ == '__main__':
    from _testBasics import testUnit    
    testUnit()
