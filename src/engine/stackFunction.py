from engine.stack import Stack
from engine.calculatorFunction import CalculatorFunction



class StackFunction(CalculatorFunction):
    fn = lambda stack: None

    @classmethod
    def __exec__(cls, this):
        cls.fn(this)


class CF_rollStackUp(StackFunction):
    "R↑"
    fn = Stack.rollUp


class CF_rollStackDown(StackFunction):
    "R↓"
    fn = Stack.rollDown


class CF_swap_x_y(StackFunction):
    "x↔y"
    fn = Stack.swap

        
        
