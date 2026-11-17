from engine.calculator import HP11C
from _testBasics import TestMaker


from _testCase import CustomTestCase
from engine.arithmeticFunction import ArithmeticFunction
from engine import *

class TestArithmeticFunction(CustomTestCase):
        
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
    def setUp(self):
        super().setUp()
        self.calculator = HP11C()
        for x in (1.25, 2.5, 5, 10):
            self.calculator.enter(x)
 

    def test_CF_deltaPercent(self):
        tst = 100.000
        fn  = CF_deltaPercent
        self.calculator.execute(fn)
        self.assertAlmostEqual(self.calculator.x, tst, delta = 0.00001)
        

    def test_CF_percentage(self):
        tst = 0.500
        fn  = CF_percentage
        self.calculator.execute(fn)
        self.assertAlmostEqual(self.calculator.x, tst, delta = 0.00001)
        

    def test_CF_pi(self):
        tst = 3.141592654
        fn  = CF_pi
        self.calculator.execute(fn)
        self.assertAlmostEqual(self.calculator.x, tst, delta = 0.00001)
        

    def test_CF_randomNr(self):
        fn  = CF_randomNumber
        self.calculator.execute(fn)
        self.assertTrue(0 <= self.calculator.x <= 1)
        

    def test_CF_absoluteValue(self):
        tst = 100.
        fn  = CF_absoluteValue
        
        self.calculator.setX(100)
        self.calculator.execute(fn)
        self.assertEqual(self.calculator.x, tst)
        
        self.calculator.setX(-100)
        self.calculator.execute(fn)
        self.assertEqual(self.calculator.x, tst)
        

    def test_CF_changeSign(self):
        tst = -10.000
        fn  = CF_changeSign
        self.calculator.execute(fn)
        self.assertEqual(self.calculator.x, tst)
        

    def test_CF_convertToDecHrs(self):
        tst = 12.500
        fn  = CF_convertToDecimalHours
        
        self.calculator.enter(12.3)
        self.calculator.execute(fn)
        self.assertAlmostEqual(self.calculator.x, tst, delta = 0.00001)
        

    def test_CF_convertToMinHrs(self):
        tst = 12.300
        fn  = CF_convertToMinuteHours
        self.calculator.enter(12.5)
        self.calculator.execute(fn)
        self.assertAlmostEqual(self.calculator.x, tst, delta = 0.00001)
        

    def test_CF_exponent(self):
        tst = 22026.46579
        fn  = CF_exponent
        self.calculator.execute(fn)
        self.assertAlmostEqual(self.calculator.x, tst, delta = 0.00001)
        

    def test_CF_exponentOf10(self):
        tst = 100000.000
        fn  = CF_exponentOf10
        self.calculator.swap()
        self.calculator.execute(fn)
        self.assertAlmostEqual(self.calculator.x, tst, delta = 0.00001)
        

    def test_CF_factorial(self):
        tst = 2869690.268
        fn  = CF_factorial
        self.calculator.enter(9.9)
        self.calculator.execute(fn)
        self.assertAlmostEqual(self.calculator.x, tst, delta = 0.001)
        

    def test_CF_fraction(self):
        tst = 0.456
        fn  = CF_fraction
        self.calculator.enter(123.456)
        self.calculator.execute(fn)
        self.assertAlmostEqual(self.calculator.x, tst, delta = 0.00001)
        

    def test_CF_integer(self):
        tst = 123.000
        fn  = CF_integer
        self.calculator.enter(123.456)
        self.calculator.execute(fn)
        self.assertAlmostEqual(self.calculator.x, tst, delta = 0.00001)
        

    def test_CF_logarithmBase10(self):
        tst = 4.0915
        fn  = CF_logarithmBase10
        self.calculator.enter(12345)
        self.calculator.execute(fn)
        self.assertAlmostEqual(self.calculator.x, tst, delta = 0.00001)
        

    def test_CF_logarithmBaseE(self):
        tst = 9.4210
        fn  = CF_logarithmNatural
        self.calculator.enter(12345)
        self.calculator.execute(fn)
        self.assertAlmostEqual(self.calculator.x, tst, delta = 0.00001)
        

    def test_CF_reciprokeValue(self):
        tst = 0.1000
        fn  = CF_reciprokeValue
        self.calculator.execute(fn)
        self.assertAlmostEqual(self.calculator.x, tst, delta = 0.00001)
        

    def test_CF_sqareRoot(self):
        tst = 3.1623
        fn  = CF_sqareRoot
        self.calculator.execute(fn)
        self.assertAlmostEqual(self.calculator.x, tst, delta = 0.001)
        

    def test_CF_square(self):
        tst = 100.000
        fn  = CF_square
        self.calculator.execute(fn)
        self.assertAlmostEqual(self.calculator.x, tst, delta = 0.00001)
        


    
                
        
        
if __name__ == '__main__':
    from _testBasics import testUnit    
    testUnit()
    # from engine.calculatorFunction import CalculatorFunction
    #
    # for cls in sorted(CalculatorFunction._subclasses_.values(), key=str):
    #     if issubclass(cls, ArithmeticFunction) and "CF_" in str(cls):
    #         print(f"""    def test_{cls.className}(self):
    #     tst = 0.000
    #     fn  = {cls.className}
    #     self.calculator.execute(fn)
    #     self.assertAlmostEqual(self.calculator.x, tst, delta = 0.00001)
    #     \n""")
    #

