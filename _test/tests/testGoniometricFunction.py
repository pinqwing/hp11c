from engine.calculator import HP11C
from engine import *

from _testBasics import TestMaker, testClass
from _testCase import CustomTestCase

ALPHA = 30
argX  = 0.5

class TestGoniometricFunction(CustomTestCase):
        
    def __init__(self, *args):
        super().__init__(*args)
        
        
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
    def setUp(self):
        super().setUp()
        self.calculator = HP11C()
        self.calculator.setAngularMode(AngularMode.degrees)
        
        for x in (9, 8, 7, 6):
            self.calculator.enter(x)
 

    def _checkRegisters(self, tst, x, y, z, t):
        self.assertEqual([x, y, z, t], list(tst), "expVal stack differs from realized stack")


    def test_CF_arcCosinus(self):
        x           = argX
        expected    = 60.0
        iterations  = {mode: value for mode, value in zip(AngularMode, AngularMode.degreesForAll(expected))}
        for mode, expVal in iterations.items():
            with self.subTest(msg=str(mode)):
                self.calculator.angularMode = mode 
                self.calculator.setX(x)
                self.calculator.execute(CF_arcCosinus)
                self.assertAlmostEqual(expVal, self.calculator.x, delta = 0.001)
            

    def test_CF_arcSinus(self):
        x           = argX
        expected    = 30.0
        iterations  = {mode: value for mode, value in zip(AngularMode, AngularMode.degreesForAll(expected))}
        for mode, expVal in iterations.items():
            with self.subTest(msg=str(mode)):
                self.calculator.angularMode = mode 
                self.calculator.setX(x)
                self.calculator.execute(CF_arcSinus)
                self.assertAlmostEqual(expVal, self.calculator.x, delta = 0.001)
            

    def test_CF_arcTangens(self):
        x           = argX
        expected    = 26.5651
        iterations  = {mode: value for mode, value in zip(AngularMode, AngularMode.degreesForAll(expected))}
        for mode, expVal in iterations.items():
            with self.subTest(msg=str(mode)):
                self.calculator.angularMode = mode 
                self.calculator.setX(x)
                self.calculator.execute(CF_arcTangens)
                self.assertAlmostEqual(expVal, self.calculator.x, delta = 0.001)
            

    def test_CF_convertToDegrees(self):
        expVal = 45.00
        x, y     = math.pi/4, 0
        self.calculator.setY(y)
        self.calculator.setX(x)
        self.calculator.execute(CF_convertToDegrees)
        self.assertAlmostEqual(expVal, self.calculator.x, delta = 0.001)
            

    def test_CF_convertToRadians(self):
        expVal = math.pi/4.
        x      = 45
        self.calculator.setX(x)
        self.calculator.execute(CF_convertToRadians)
        self.assertAlmostEqual(expVal, self.calculator.x, delta = 0.001)
            

    def test_CF_cosinus(self):
        expVal = 0.50
        xxs    = AngularMode.degreesForAll(60)
        iterations  = {mode: x for mode, x in zip(AngularMode, xxs)}
        for mode, x in iterations.items():
            with self.subTest(msg=str(mode)):
                self.calculator.angularMode = mode 
                self.calculator.setX(x)
                self.calculator.execute(CF_cosinus)
                self.assertAlmostEqual(expVal, self.calculator.x, delta = 0.001)
            

    def test_CF_sinus(self):
        expVal = 0.500
        xxs    = AngularMode.degreesForAll(30)
        iterations  = {mode: x for mode, x in zip(AngularMode, xxs)}
        for mode, x in iterations.items():
            with self.subTest(msg=str(mode)):
                self.calculator.angularMode = mode 
                self.calculator.setX(x)
                self.calculator.execute(CF_sinus)
                self.assertAlmostEqual(expVal, self.calculator.x, delta = 0.001)
            

    def test_CF_tangens(self):
        expVal = 1.00
        xxs    = AngularMode.degreesForAll(45)
        iterations  = {mode: x for mode, x in zip(AngularMode, xxs)}
        for mode, x in iterations.items():
            with self.subTest(msg=str(mode)):
                self.calculator.angularMode = mode 
                self.calculator.setX(x)
                self.calculator.execute(CF_tangens)
                self.assertAlmostEqual(expVal, self.calculator.x, delta = 0.001)
            

    def test_CF_convertToCartesian(self):
        expVal = 10.3923, 6.000
        x, yys = 12, AngularMode.degreesForAll(30) # r, theta
        iterations  = {mode: y for mode, y in zip(AngularMode, yys)}
        for mode, y in iterations.items():
            with self.subTest(msg=str(mode)):
                self.calculator.angularMode = mode 
                self.calculator.setY(y)
                self.calculator.setX(x)
                self.calculator.execute(CF_convertToCartesian)
                self.assertAlmostEqual(expVal[0], self.calculator.x, delta = 0.001)
                self.assertAlmostEqual(expVal[1], self.calculator.y, delta = 0.001)
            

    def test_CF_convertToPolar(self):
        expVal = 11.1803, AngularMode.degreesForAll(26.5651) # r, theta
        x, y   = 10, 5
        iterations  = {mode: (expVal[0], v) for mode, v in zip(AngularMode, expVal[1])}
        for mode, expVal in iterations.items():
            with self.subTest(msg=str(mode)):
                self.calculator.angularMode = mode 
                self.calculator.setY(y)
                self.calculator.setX(x)
                self.calculator.execute(CF_convertToPolar)
                self.assertAlmostEqual(expVal[0], self.calculator.x, delta = 0.001)
                self.assertAlmostEqual(expVal[1], self.calculator.y, delta = 0.001)
                

        
        
if __name__ == '__main__':
    from _testBasics import testUnit    
    testClass(TestGoniometricFunction)
