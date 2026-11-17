
import pkgutil
import importlib
from importlib import resources
import pathlib

from pathlib import Path
from logging import info
import sys
from _testBasics import NosortLoader

class SuiteBuilder:
    
    def __init__(self, testSuite, testPackages = []):
        self.testSuite      = testSuite
        self.loader         = NosortLoader()
        self.testClasses  = set()
        for pkg in testPackages:
            self.addTests(pkg)
            
        
    def addTests(self, package, recursive = False):
        for module in self.getChildModules(package, recursive = recursive):
            self.addTest(module)
        
            
    def addTest(self, module):
        print(f"* adding tests from {module.__name__}")
        tests  = self.loader.loadTestsFromModule(module)
        for test in tests:
            # double-entry prevention:
            classes = set(type(t) for t in test._tests)
            if len(classes) == 1:
                cls = classes.pop()
                if cls.__name__ in self.testClasses:
                    continue
                self.testClasses.add(cls.__name__)
                
            # adding suites:
            if test not in self.testSuite:
                self.testSuite.addTest(test)
        
        
    def getModules(self, package):
        files = (resources.files(package))._paths
        if files:
            return [info for info in pkgutil.iter_modules([files[0]])]
        return []
        
        
    def getChildModules(self, package, pattern = "test*.py", recursive = True):
        modules  = []
        folder   = Path(list(package.__path__)[0])
        files    = folder.rglob(pattern) if recursive else folder.glob(pattern)
        children = [f for f in files]
        for file in children:
            name = f"{package.__name__}/{file.relative_to(folder)}".replace("/", ".") 
            try:
                spec    = importlib.util.spec_from_file_location(name, file)
                module  = importlib.util.module_from_spec(spec)
                sys.modules[name] = module
                spec.loader.exec_module(module)
    
                modules.append(module)
                print(f"* succesfully imported {file.stem} ")
            except Exception as e:
                print(f"* import of {name} failed: {e}")
                
        return modules



if __name__ == '__main__':
        
    class PT(list):
        
        def addTest(self, test):
            print(len(test._tests), test)
            self.append(test)

    pt = PT()
    
    bld = SuiteBuilder(pt, [])
    bld.addTests(_test, True)
