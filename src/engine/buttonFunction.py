import sys
from PyQt5.Qt import *  
from engine import *
import inspect
from collections import namedtuple

BUTTONS = [
    ['sqrt', 'exp', '10x',  'pwr',  'inv', 'chs',   '7',    '8',    '9',    'div'],
    ['sst',  'gto', 'sin',  'cos',  'tan', 'eex',   '4',    '5',    '6',    'mul'],
    ['rs',   'gsb', 'r',    'swap', 'bsp', 'enter', '1',    '2',    '3',    'min'],
    ['on',   'f',   'g',    'sto',  'rcl',  None,   '0',  'dot', 'sigma',  'plus'],           
          ]   
             


class ButtonFunction:
    index     = -1
          
    def __init__(self, fMode = None, plain = None, gMode = None, css = {}, 
                 captions = True, default = XF_NOP, **specialFunctions):
        
        super().__init__()
        self.name       = type(self).__name__
        self.showCaps   = captions
        self.css        = "; ".join([f"{k}: {v}" for k, v in css.items()])
        self.functions  = {mode: None for mode in ShiftMode}
        self.default    = default
        self.functions.update({ShiftMode.plain: plain, 
                               ShiftMode.fMode: fMode,
                               ShiftMode.gMode: gMode})
        
        try:
            self.functions.update({ShiftMode[mode]: function for mode, function in specialFunctions.items()}) 
        except KeyError as e:
            tag = self.functions[ShiftMode.plain].getCaption() # approximately speaking ...
            raise TypeError(f"{type(self).__name__}.__init__() got an unexpected keyword argument '{e.args[0]}' [{tag}]") 
        
        
        
    x = property(lambda b:  79 + ((b.index  % 10) -1) %10 * 107)
    y = property(lambda b: 282 + ((b.index // 10) -1)     * 128)
    
    
    def __str__(self):
        return f"({self.index:02}) {self.name}"
    

    def __call__(self, mode: ShiftMode):
        self.getFunction(mode)()
                

    def getFunction(self, mode: ShiftMode, default = None):
        function = self.functions[mode]
        default  = self.default if default  is None else default
        return          default if function is None else function
                

    def getCaptions(self):
        return ["" if fn is None else fn.getCaption() for fn in self.functions]

    
    def generateHtml(self):
        tag         = self.name
        gFunction   = self.getFunction(ShiftMode.gMode) 
        pFunction   = self.getFunction(ShiftMode.plain)
        gCaption    = gFunction.getCaption()
        pCaption    = pFunction.getCaption()
        
        return f"""
        <div id="{tag}" class="button" style="top: {self.y}px; left: {self.x}px; {self.css}">
            <span class="plainText">{pCaption}</span><br/>
            <span class="blueText">{gCaption}</span>
            </div>"""
        
        
    
    @staticmethod
    def links():
        return {"0":     ButtonFunction(CF_factorial, CF_number_0, CF_average, default = CF_number_0),
                "1":     ButtonFunction(CF_permutations, CF_number_1, CF_combinations, default = CF_number_1),
                "2":     ButtonFunction(CF_convertToMinuteHours, CF_number_2, CF_convertToDecimalHours, default = CF_number_2),
                "3":     ButtonFunction(CF_convertToRadians, CF_number_3, CF_convertToDegrees, default = CF_number_3),
                "4":     ButtonFunction(CF_swap_x_I, CF_number_4, CF_setFlag, default = CF_number_4),
                "5":     ButtonFunction(CF_decrementSkipIfEqual, CF_number_5, CF_clearFlag, default = CF_number_5),
                "6":     ButtonFunction(CF_incrementSkipIfGreater, CF_number_6, CF_testFlag, default = CF_number_6),
                "7":     ButtonFunction(CF_notationModeFix, CF_number_7, CF_angleModeDegrees, default = CF_number_7),
                "8":     ButtonFunction(CF_notationModeSci, CF_number_8, CF_angleModeRadians, default = CF_number_8),
                "9":     ButtonFunction(CF_notationModeEng, CF_number_9, CF_angleModeGrades, default = CF_number_9),
                "dot":   ButtonFunction(CF_linearEstimateAndCoC, CF_decimalPoint, CF_standardDeviation, default = CF_decimalPoint),
                "10x":   ButtonFunction(CF_userKeyC, CF_exponentOf10, CF_logarithmBase10),
                "bsp":   ButtonFunction(CF_showMantissa, CF_backarrow, CF_clearX_Register),
                "chs":   ButtonFunction(CF_pi, CF_changeSign, CF_absoluteValue),
                "cos":   ButtonFunction(CF_indirectOperation, CF_cosinus, CF_arcCosinus, hyperbole = CF_cosh, hyper_inv = CF_arcCosh),
                "div":   ButtonFunction(CF_test_x_le_y, CF_operatorDiv, CF_test_x_lt_0),
                "eex":   ButtonFunction(CF_convertToCartesian, CF_enterExponent, CF_convertToPolar),
                "enter": ButtonFunction(CF_randomNumber, CF_enter, CF_lastX, css = {"height": f'{68 + 128}px', "padding-top": "13px"}, captions = False),
                "exp":   ButtonFunction(CF_userKeyB, CF_exponent, CF_logarithmNatural),
                "f":     ButtonFunction(CF_shiftF, CF_shiftF, CF_shiftF, css = {"background-image": "url('keyf.png')"}, captions = False),
                "g":     ButtonFunction(CF_shiftG, CF_shiftG, CF_shiftG, css = {"background-image": "url('keyg.png')"}, captions = False),
                "gsb":   ButtonFunction(CF_clearStatistics, CF_gosub, CF_return),
                "gto":   ButtonFunction(CF_hyperbolic, CF_goto, CF_hyperbolicInv),
                "inv":   ButtonFunction(CF_userKeyE, CF_reciprokeValue, CF_deltaPercent),
                "min":   ButtonFunction(CF_test_x_ne_y, CF_operatorMin, CF_test_x_ne_0),
                "mul":   ButtonFunction(CF_test_x_gt_y, CF_operatorMul, CF_test_x_gt_0),
                "on":    ButtonFunction(None, CF_switchOn, None),
                "plus":  ButtonFunction(CF_test_x_eq_y, CF_operatorPlus, CF_test_x_eq_0),
                "pwr":   ButtonFunction(CF_userKeyD, CF_operatorPower, CF_percentage),
                "r":     ButtonFunction(CF_clearProgram, CF_rollStackDown, CF_rollStackUp),
                "rcl":   ButtonFunction(CF_toggleUserMode, CF_recallValue, CF_memoryStatus),
                "rs":    ButtonFunction(CF_pause, CF_runStop, CF_toggleProgramMode),
                "sigma": ButtonFunction(CF_linearRegression, CF_statisticsAdd, CF_statisticsSubtract),
                "sin":   ButtonFunction(CF_swap_x_Indirect, CF_sinus, CF_arcSinus, hyperbole = CF_sinh, hyper_inv = CF_arcSinh),
                "sqrt":  ButtonFunction(CF_userKeyA, CF_sqareRoot, CF_square),
                "sst":   ButtonFunction(CF_label, CF_singleStep, CF_backStep),
                "sto":   ButtonFunction(CF_fraction, CF_storeValue, CF_integer),
                "swap":  ButtonFunction(CF_clearRegisters, CF_swap_x_y, CF_round),
                "tan":   ButtonFunction(CF_indexRegister, CF_tangens, CF_arcTangens, hyperbole = CF_tanh, hyper_inv = CF_arcTanh),
                }
        
        
class ButtonFunctions(dict):
          
    def __init__(self):
        super().__init__()
        self.update(ButtonFunction.links())
        self._assignIndices()
        
        
    def _assignIndices(self):
        for y, row in enumerate(BUTTONS, 1):
            for x, tag in enumerate(row, 1):
                bf = self.get(tag, False)
                if bf: 
                    bf.index = 10*y + x % 10
                    bf.name  = tag
        



if __name__ == '__main__':
    for b in sorted(ButtonFunctions().values(), key = lambda b: b.y * 10 + b.x):
        print(b.generateHtml())