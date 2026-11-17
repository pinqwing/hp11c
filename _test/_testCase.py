import unittest
import warnings
import inspect
from enum import EnumMeta, Enum
from pathlib import Path


class __metaverbosity__(EnumMeta):
    # if an invalid argument is passed in the construction of an Enum, default is used instead
    
    def __call__(cls, value, default=0):
        try:    value = value.value # assume Enum ...
        except: pass
        try:    value = int(value)
        except: value = -1

        if value < 0: value = default.value if isinstance(default, Enum) else default 
        
        value = min(value, max([t.value for t in cls]))
        return super().__call__(value)


        
    
class Verbosity(Enum, metaclass = __metaverbosity__):
    default = -1
    verbose = 0
    limited = 1
    minimal = 2  
    silent  = 3  


BASEPATH    = Path("/tmp/ramdisk/") 
# NB: CustomTestCase.setUpClass initialiseert environment


class CustomTestCase(unittest.TestCase):

    VERBOSITY       = Verbosity.limited 
    currentTest     = "(unknown)"
    skippingReason  = None
    warnings        = []

    
    def __str__(self):
        return f"  \u25AA {self._testMethodName:30s}"
        return f"{type(self).__name__}.{self._testMethodName}"

    
    def _callTestMethod(self, method):
        # we don't need those deprecation warnings
        method()


    def assertSameMethods(self, meth1: callable, meth2: callable, msg = None):
        if None in (meth1, meth2):
            self.assertIs(meth1, meth2, msg)
        else:
            self.assertIs(meth1.__func__, meth2.__func__, msg)


    def assertNotSameMethods(self, meth1: callable, meth2: callable, msg = None):
        if None in (meth1, meth2):
            self.assertIsNot(meth1, meth2, msg)
        else:
            self.assertIsNot(meth1.__func__, meth2.__func__, msg)


    # === skipping tests: =====    
    @classmethod
    def allowedToRun(cls): 
        return not bool(CustomTestCase.skippingReason)

    @classmethod
    def skipRemainingTests(cls, reason = "canceled"):
        CustomTestCase.skippingReason = reason
        
        
    def _callSetUp(self):
        method = self._testMethodName
        type(self).currentTest = method

        if getattr(method, "rollbackRequired", False):
            if not self.allowedToRun():
                self.skipTest(self.skippingReason)
        super()._callSetUp()

        
    @classmethod
    def setUpClass(cls):
        print(f"\n{'-'*60}\n    case: {cls.__name__}\n{'-'*60}")
        # === manage warnings: =====
        cls.warnings = []
        cls.warningsProc = warnings.showwarning
        warnings.showwarning = cls.addWarning
    
    
    @classmethod
    def tearDownClass(cls):
        warnings.showwarning = cls.warningsProc
        for args, kwargs in cls.warnings:
            warnings.showwarning(*args, **kwargs)
           
            
    @classmethod
    def addWarning(cls, *args, **kwargs):
        args[0].source = cls.currentTest
        cls.warnings.append((args, kwargs))
        
        
    # === other: =====
    def nyi(self):
        # curframe = inspect.currentframe()
        # calframe = inspect.getouterframes(curframe, 2)
        # # self.addWarning(f"test not yet implemented: '{calframe[1][3]}'", stacklevel=2, category=Informing)        
        # warnings.warn(f"test not yet implemented: '{calframe[1][3]}'", stacklevel=2, category=Informing)        
        warnings.warn("test not yet implemented'", stacklevel=2) #, category=Informing)        



