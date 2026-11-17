from engine.stack import Stack
from _testBasics import TestMaker


from _testCase import CustomTestCase

class TestStack(CustomTestCase):
        
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
    def setUp(self):
        super().setUp()
        self.stack = Stack()
        for x in (4, 3, 2, 1):
            self.stack.enter(x)
 

    def _checkRegisters(self, tst, x, y, z, t):
        self.assertEqual(tst.x, x)
        self.assertEqual(tst.y, y)
        self.assertEqual(tst.z, z)
        self.assertEqual(tst.t, t)


    def test_basic(self): 
        self._checkRegisters(self.stack, 1.0, 2.0, 3.0, 4.0)

        
    def test_clear(self): 
        self.stack.clearStack()
        self._checkRegisters(self.stack, 0.0, 0.0, 0.0, 0.0)
        

    def test_setX(self):
        t   = 3.141592 
        self.stack.setX(t) 
        self._checkRegisters(self.stack, t, 2.0, 3.0, 4.0)
        

    def test_enter(self): 
        self.stack.enter()
        self._checkRegisters(self.stack, 1.0, 1.0, 2.0, 3.0)
        

    def test_enterX(self): 
        t   = 3.141592 
        self.stack.enter(t)
        self._checkRegisters(self.stack, t, 1.0, 2.0, 3.0)
        

    def test_joinXY(self): 
        t   = 3.141592 
        self.stack.joinXY(t)
        self._checkRegisters(self.stack, t, 3.0, 4.0, 4.0)
        

    def test_pop(self): 
        self._checkRegisters(self.stack, 1.0, 2.0, 3.0, 4.0)
        t = self.stack.pop()
        self._checkRegisters(self.stack, 2.0, 3.0, 4.0, 4.0)
        self.assertEqual(t, [1.0])

        t = self.stack.pop(2)
        self._checkRegisters(self.stack, 4.0, 4.0, 4.0, 4.0)
        self.assertEqual(t, [2.0, 3.0])


    def test_rollDown(self): 
        self._checkRegisters(self.stack, 1.0, 2.0, 3.0, 4.0)
        self.stack.rollDown()
        self._checkRegisters(self.stack, 2.0, 3.0, 4.0, 1.0)
        

    def test_rollUp(self): 
        self._checkRegisters(self.stack, 1.0, 2.0, 3.0, 4.0)
        self.stack.rollUp()
        self._checkRegisters(self.stack, 4.0, 1.0, 2.0, 3.0)
        

    def test_swap(self): 
        self.stack.swap()
        self._checkRegisters(self.stack, 2.0, 1.0, 3.0, 4.0)


    def test_lastX(self):
        self.stack.enter(1)
        self.stack.enter(2)
        self.stack.enter(3)
        self.assertEqual(self.stack.x, 3.0)
        self.assertEqual(self.stack._lastX, 2.0)
        self.stack.setX(123)
        self.assertEqual(self.stack._lastX, 3.0)
        self.stack.lastX()
        self.assertEqual(self.stack.x, 3.0)
        self.assertEqual(self.stack._lastX, 3.0)
        
        
if __name__ == '__main__':
    from _testBasics import testUnit    
    testUnit()
