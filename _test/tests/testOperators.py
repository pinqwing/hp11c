from engine.calculator import HP11C
from _testBasics import TestMaker


from _testCase import CustomTestCase
from engine.arithmeticFunction import CF_operatorPlus, CF_operatorMin,\
    CF_operatorMul, CF_operatorDiv, CF_operatorPower

class TestOperators(CustomTestCase):
        
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
    def setUp(self):
        super().setUp()
        self.calculator = HP11C()
        for x in (4, 3, 2, 1):
            self.calculator.enter(x)
 

    def _checkRegisters(self, tst, x, y, z, t):
        self.assertEqual([x, y, z, t], list(tst))


    def test_basic(self): 
        self._checkRegisters(self.calculator, 1.0, 2.0, 3.0, 4.0)

        
    def test_plus(self):
        fn = CF_operatorPlus
        self.calculator.execute(fn)
        self._checkRegisters(self.calculator, 3.0, 3.0, 4.0, 4.0)
            
        
    def test_minus(self):
        fn = CF_operatorMin
        self.calculator.execute(fn)
        self._checkRegisters(self.calculator, 1.0, 3.0, 4.0, 4.0)
            
        
    def test_muliply(self):
        fn = CF_operatorMul
        self.calculator.setX(4)
        self.calculator.execute(fn)
        self._checkRegisters(self.calculator, 8.0, 3.0, 4.0, 4.0)
            
        
    def test_divide(self):
        fn = CF_operatorDiv
        self.calculator.setX(4)
        self.calculator.execute(fn)
        self._checkRegisters(self.calculator, 0.5, 3.0, 4.0, 4.0)
            
        
    def test_power(self):
        fn = CF_operatorPower
        self.calculator.setX(4)
        self.calculator.execute(fn)
        self._checkRegisters(self.calculator, 16.0, 3.0, 4.0, 4.0)
            
        
        
if __name__ == '__main__':
    from _testBasics import testUnit    
    testUnit()
