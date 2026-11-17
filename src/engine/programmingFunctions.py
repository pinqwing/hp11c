from engine.calculatorFunction import CalculatorFunction


class CF_toggleProgramMode(CalculatorFunction):
    "P/R"


class CF_toggleUserMode(CalculatorFunction):
    "USER"


class CF_indirectOperation(CalculatorFunction):
    "(i)"


class CF_backStep(CalculatorFunction):
    "BST"


class CF_clearFlag(CalculatorFunction):
    "CF"


class CF_testFlag(CalculatorFunction):
    "F?"


class CF_gosub(CalculatorFunction):
    "GSB"


class CF_goto(CalculatorFunction):
    "GTO"


class CF_indexRegister(CalculatorFunction):
    "I"

    
class CF_decrementSkipIfEqual(CalculatorFunction):
    "DSE"


class CF_incrementSkipIfGreater(CalculatorFunction):
    "ISG"


class CF_label(CalculatorFunction):
    "LBL"


class CF_clearProgram(CalculatorFunction):
    "PRGM"


class CF_pause(CalculatorFunction):
    "PSE"


class CF_runStop(CalculatorFunction):
    "R/S"


class CF_return(CalculatorFunction):
    "RTN"


class CF_setFlag(CalculatorFunction):
    "SF"


class CF_singleStep(CalculatorFunction):
    "SST"


class CF_test_x_lt_0(CalculatorFunction):
    "x&lt;0"


class CF_test_x_eq_0(CalculatorFunction):
    "x=0"


class CF_test_x_eq_y(CalculatorFunction):
    "x=y"


class CF_test_x_gt_0(CalculatorFunction):
    "x>0"


class CF_test_x_gt_y(CalculatorFunction):
    "x>y"


class CF_average(CalculatorFunction):
    "x̄"


class CF_test_x_ne_0(CalculatorFunction):
    "x≠0"


class CF_test_x_ne_y(CalculatorFunction):
    "x≠y"


class CF_test_x_le_y(CalculatorFunction):
    "x≤y"


class CF_swap_x_Indirect(CalculatorFunction):
    "x↔(i)"


class CF_swap_x_I(CalculatorFunction):
    "x↔I"


CF_memoryStatus         = CalculatorFunction.spawn("CF_memoryStatus",       caption = "MEM")
