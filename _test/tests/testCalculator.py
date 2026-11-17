from engine.calculator import HP11C
from engine import *

import math
from _testBasics import TestMaker
from _testCase import CustomTestCase


testdata = {
            DisplayMode.fixed: 
                [(12345678.9, ' 12 345 678.90'), (1234.56789, ' 1 234.5679'), (0.123456789, ' 0.1235'), 
                 (1.23456789e-05, ' 0.0000'), (1.23456789e-09, ' 0.0000')],
            DisplayMode.scientific: 
                [(12345678.9, ' 1.2346   07'), (1234.56789, ' 1.2346   03'), (0.123456789, ' 1.2346  -01'), 
                 (1.23456789e-05, ' 1.2346  -05'), (1.23456789e-09, ' 1.2346  -09')],
            DisplayMode.engineering: 
                [(12345678.9, ' 12.346   06'), (1234.56789, ' 1.2346   03'), (0.123456789, ' 123.46  -03'), 
                 (1.23456789e-05, ' 12.346  -06'), (1.23456789e-09, ' 1.2346  -09')],
                }
        

class TestCalculator(CustomTestCase):
        
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        
    def calculator(self, x=0, y=0, z=0, t=0):
        calculator = HP11C()
        for x in (t, z, y, x):
            calculator.enter(x)
        return calculator


    def test_Memory(self):
        clc = self.calculator(123.456)
        clc.store(1)
        clc.setX(0)
        self.assertEqual(clc.x, 0.0)
        clc.recall(1)
        self.assertEqual(clc.x, 123.456)
        
        
    def test_Memories(self):
        clc = self.calculator()
        for i in range(20):
            clc.enter(i)
            clc.store(i)
            self.assertEqual(clc.x, float(i))
            
        for i in range(20):
            clc.recall(i)
            self.assertEqual(clc.x, float(i))


    def test_falseMemories(self):
        clc = self.calculator()
        with self.assertRaises(KeyError):
            clc.store(99999)
        with self.assertRaises(KeyError):
            clc.recall("A")
            
            
    def test_angularMode(self):
        pi4 = math.pi/4
        clc = self.calculator()
        clc.setAngularMode(AngularMode.degrees)
        self.assertAlmostEqual(clc.fromRadians(pi4), 45.)
        self.assertAlmostEqual(clc.toRadians(45.), pi4)
        
        clc.setAngularMode(AngularMode.radians)
        self.assertAlmostEqual(clc.fromRadians(pi4), pi4)
        self.assertNotEqual(clc.toRadians(45.), math.pi/4)
        
        
    def test_displayModes(self):
        clc = self.calculator()
        for mode, dataPairs in testdata.items():
            clc.setDisplayMode(mode)
            clc.decimals    = 4
            for x, s in dataPairs:
                clc.setX(x)
                self.assertEqual(clc.currentDisplay(), s, f"for {mode.name}: {x}")


    def test_DisplayNegative(self):
        clc = self.calculator()
        for mode, dataPairs in testdata.items():
            clc.decimals    = 4
            for x, s in dataPairs:
                clc.setDisplayMode(mode)
                clc.setX(x)
                positive = clc.currentDisplay()
                clc.setX(-x)
                negative = clc.currentDisplay()
                
                self.assertEqual(positive[0], " ", f"missing space for {mode.name}: {x}")
                self.assertEqual(negative, '-' + positive[1:], f"for {mode.name}: {x}")
                
        
    def test_memorySimple(self):
        clc = self.calculator()
        for i in range(10):
            tst = 1000 * i
            clc.enter(tst)
            clc.setShiftMode(ShiftMode.store)
            clc.addToInput(str(i))
        
            self.assertEqual(clc.memory[i], tst)
            clc.enter(12345)
            self.assertNotEqual(clc.x, tst)
            
            clc.setShiftMode(ShiftMode.recall)
            clc.addToInput(str(i))
            self.assertEqual(clc.x, tst)
            
        
    def test_memoryDot(self):
        clc = self.calculator()
        for i in range(10):
            tst = 1000. * i
            clc.enter(tst)
            clc.setShiftMode(ShiftMode.store)
            clc.addToInput('.')
            clc.addToInput(str(i))
        
            self.assertEqual(clc.memory[10+i], tst)
            if i > 0:
                self.assertNotEqual(clc.memory[i], tst)
            clc.enter(12345)
            self.assertNotEqual(clc.x, tst)
            
            clc.setShiftMode(ShiftMode.recall)
            clc.addToInput('.')
            clc.addToInput(str(i))
            self.assertEqual(clc.x, tst)
            
        
    def test_memoryOperations(self):
        clc = self.calculator()
        clc.enter(1)
        clc.setShiftMode(ShiftMode.store)
        clc.addToInput("9")
        self.assertEqual(clc.memory[9], 1.0)
        
        clc.enter(4)
        clc.setShiftMode(ShiftMode.store)
        clc.addToInput("+")
        clc.addToInput("9")
        self.assertEqual(clc.memory[9], 5.0)
        
        clc.enter(2)
        clc.setShiftMode(ShiftMode.store)
        clc.addToInput("÷")
        clc.addToInput("9")
        self.assertEqual(clc.memory[9], 2.5)
        
        
    def test_enterExponent(self):
        clc = self.calculator()
        clc.execute(CF_number_1)
        clc.execute(CF_number_2)
        clc.execute(CF_number_3)
        
        self.assertEqual(clc.x, 123.)
        self.assertEqual(clc.shiftMode,   ShiftMode.plain)

        print(clc.currentDisplay())
                
        clc.execute(CF_enterExponent)
        self.assertEqual(clc.shiftMode,    ShiftMode.exponent)
        
        print(clc.currentDisplay())
        
        clc.execute(CF_number_4)
        print(clc.currentDisplay())
        clc.execute(CF_enter)
        
        print(clc.currentDisplay())
        self.assertEqual(clc.x, 1230000.)
        self.assertEqual(clc.shiftMode,   ShiftMode.plain)
        self.assertEqual(clc.display.mode, DisplayMode.fixed)
        
        
    
        
        
        
            
if __name__ == '__main__':
    from _testBasics import testUnit    
    testUnit()
