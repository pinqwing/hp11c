import unittest
import inspect
import sys



class NosortLoader(unittest.TestLoader):
    def getTestCaseNames(self, testCaseClass):
        return [
            name
            for name, obj in testCaseClass.__dict__.items()
            if name.startswith(self.testMethodPrefix) and callable(obj)
            ]    


class TestMaker: 
    """
        
    def test_{name}(self): {comment}
        # ret = {className}.{name}({callParams})
        self.nyi()
    ./.
    def test_{name}(self): {comment}
        # tst = {className}({initParams})
        # ret = tst.{name}({callParams})
        self.nyi()
        
    """
    
    def __init__(self, aClass):
        self.clazz = aClass
    
    
    def classHeader(self, aClass):
        hdr = f"""
from _testCase import CustomTestCase

class Test{aClass.__name__}(CustomTestCase):
        
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
    def setUp(self):
        super().setUp()"""
        print(hdr, "\n")
                
                
    def classFooter(self):
        print("""if __name__ == '__main__':
    from _testBasics import testUnit    
    testUnit()""")
    
    def methodDefined(self, methodName):
        return methodName in self.clazz.__dict__
    
    
    def template(self, index):    
        doc = inspect.getdoc(self)
        src = doc.split("./.")[index]
        return src.replace("\n", "\n    ")
    
    
    def signature(self, fn):
        s = inspect.signature(fn)
        p = s.parameters.copy()
        p.pop("self", None)
        p.pop("cls", None)
        return ", ".join([str(par) for par in p])
         
    
    def makeTest(self, name, fn, templateIndex):
        className   = self.clazz.__name__
        callParams  = self.signature(fn)
        initParams  = self.signature(self.clazz.__init__)
        template    = self.template(templateIndex)
        comment     = "# inherited method" if not self.methodDefined(name) else ""
        
        print(template.format(**locals()))
        
        
    def makeTests(self, objectMethods    = True, 
                        classMethods     = True, 
                        inheritedMethods = False):
        
        filters  = ((0, inspect.ismethod),)   if classMethods  else ()
        filters += ((1, inspect.isfunction),) if objectMethods else ()
        
        self.classHeader(self.clazz)
        
        for i, fltr in filters:
            for name, fn in inspect.getmembers(self.clazz, fltr):
                if not name.startswith('_'):
                    if inheritedMethods or self.methodDefined(name): 
                        self.makeTest(name, fn, templateIndex = i)
                        
        self.classFooter()


def testUnit(testOnly = None): 
    parent = inspect.stack()[1]
    module = inspect.getmodule(parent.frame)    
    loader = NosortLoader()
    if testOnly is None:
        suite  = loader.loadTestsFromModule(module) 
    else:
        name  = testOnly.__qualname__ 
        suite = loader.loadTestsFromName(name, module)
    runner = unittest.TextTestRunner(stream = sys.stdout, verbosity = 2)
    runner.run(suite)            

    
def testClass(testClass):
    loader = NosortLoader()
    suite = loader.loadTestsFromTestCase(testClass)
    
    runner = unittest.TextTestRunner(stream = sys.stdout, verbosity = 2)
    runner.run(suite)            
    
    
