from engine.calculator import HP11C
from engine import *

from _testBasics import TestMaker
from _testCase import CustomTestCase
from engine.calculatorFunction import CF_clearStatistics



class TestStackFunction(CustomTestCase):
        
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        
    def calculator(self, x=0, y=0, z=0, t=0):
        calculator = HP11C()
        for x in (t, z, y, x):
            calculator.enter(x)
        return calculator
        


    def _checkRegisters(self, clc, x, y, z, t):
        self.assertEqual([x, y, z, t], list(clc), "expected stack differs from realized stack")


    def test_basic(self): 
        clc = self.calculator(6.0, 7.0, 8.0, 9.0)
        self._checkRegisters(clc, 6.0, 7.0, 8.0, 9.0)

        
    def test_clear(self): 
        clc = self.calculator(6.0, 7.0, 8.0, 9.0)
        fn = CF_clearStatistics
        clc.execute(fn)
        self._checkRegisters(clc, 0.0, 0.0, 0.0, 0.0)


        
        
if __name__ == '__main__':
    from _testBasics import testUnit    
    testUnit()
