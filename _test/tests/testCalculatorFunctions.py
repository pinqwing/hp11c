from engine.calculator import HP11C
from engine.calculatorFunction import *
from engine.const import AngularMode

import math
from _testBasics import TestMaker
from _testCase import CustomTestCase
from engine.arithmeticFunction import CF_operatorDiv

FN_NOP = CalculatorFunction.spawn("NOP", exec = lambda this: None)  # @UndefinedVariable


class TestCalculatorFunctions(CustomTestCase):
        
    @classmethod
    def setUpClass(cls):
        super().setUpClass()


    def setUp(self):
        super().setUp()        
        FN_NOP.exec = lambda this: self.skipTest("not implemented")
        
        
    def calculator(self, x=0, y=0, z=0, t=0):
        calculator = HP11C()
        for x in (t, z, y, x):
            calculator.enter(x)
        return calculator


    def test_CF_angleModes(self):
        clc = self.calculator()
        clc.setAngularMode(AngularMode.degrees)
        for fn in (CF_angleModeRadians, CF_angleModeDegrees, CF_angleModeGrades):
            clc.execute(fn)
            self.assertEqual(clc.angularMode, fn.mode)
            

    def test_CF_shiftModes(self):
        clc = self.calculator()
        for fn in ShiftKey.__subclasses__():
            clc.execute(fn)
            self.assertEqual(clc.shiftMode, fn.mode)
            

    def test_CF_clearX_Register(self):
        clc = self.calculator(123456)
        clc.execute(CF_clearX_Register)
        self.assertEqual(clc.x, 0.0)
            

    def test_CF_enter(self):
        clc = self.calculator(12345)
        clc.execute(CF_enter)
        self.assertEqual(clc.x, clc.y)
            

    def test_CF_enterExponent(self):
        clc = self.calculator(123.456)
        clc.execute(CF_number_1)
        clc.execute(CF_number_2)
        clc.execute(CF_number_3)
        clc.execute(CF_enterExponent)
        clc.execute(CF_number_2)
        clc.execute(CF_enter)
        self.assertEqual(clc.x, 12300.)
            

    def test_CF_lastX(self):
        clc = self.calculator(123)
        clc.setAngularMode(AngularMode.degrees)
        clc.execute(CF_enter)
        clc.execute(CF_operatorDiv)
        self.assertEqual(clc.x, 1.)
        clc.execute(CF_lastX)
        self.assertEqual(clc.x, 123.)
            

    def test_CF_notationEngineering(self):
        clc = self.calculator()
        clc.execute(FN_NOP)
            

    def test_CF_notationFixedDecimal(self):
        clc = self.calculator()
        clc.execute(FN_NOP)
            

    def test_CF_notationModeScientific(self):
        clc = self.calculator()
        clc.execute(FN_NOP)
            

    def test_numericEntry1(self): 
        clc = self.calculator()
        clc.execute(CF_number_1)
        self.assertTrue(clc.receivingInput)
        self.assertEqual(clc.x, 1.0)
        
        clc.execute(CF_shiftF)
        self.assertFalse(clc.receivingInput)
        
        
    def test_numericEntry2(self):
        def addKey(function, expectedX): 
            clc.execute(function)
            self.assertEqual(clc.x, expectedX)
            
        clc = self.calculator()
        addKey(CF_number_1,     1.0)
        addKey(CF_number_2,     12.0)
        addKey(CF_number_3,     123.0)
        addKey(CF_decimalPoint, 123.0)
        addKey(CF_number_4,     123.4)
        addKey(CF_number_5,     123.45)
        addKey(CF_number_6,     123.456)
        addKey(CF_backarrow,    123.45)
                    

    def test_CF_round(self):
        clc = self.calculator()
        clc.execute(FN_NOP)
            

    def test_CF_showMantissa(self):
        clc = self.calculator()
        clc.execute(FN_NOP)
            

    def test_CF_switchOn(self):
        clc = self.calculator()
        clc.execute(FN_NOP)
            

            
if __name__ == '__main__':
    from _testBasics import testUnit    
    testUnit()
