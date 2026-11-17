from PyQt5.Qt import *  
from engine.buttonFunction import ButtonFunction
from engine import *

BUTTONS = """sqrt sst rs on
             exp gto gsb f
             10x sin r g
             pwr cos swap sto
             inv tan bsp rcl
             chs eex enter
             7 4 1 0 
             8 5 2 . 
             9 6 3 sigma
             div mul min plus"""
             
             

class ButtonPanel(QFrame):
    
    def __init__(self):
        super().__init__()
        self.build()
        
        
    def build(self):
        buttons = [col.strip().split() for col in BUTTONS.split("\n")]
        self.setStyleSheet("""background-color: #272727; 
                              border-color:     gray; 
                              border-style:     solid; 
                              border-width:     4px 4px 8px 4px;  """)

        layout = QGridLayout(self)        
        for x, col in enumerate(buttons):
            for y, tag in enumerate(col):
                tag = "dot" if tag == '.' else tag
                bfn = ButtonFunction.factory(tag)
                layout.addWidget(bfn.getButton(), y, x)
                
    
    
    
if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication

    tpl = "\n    ".join([l.strip() for l in """
        <div id="{tag}" class="button" style="top: {yPxl}px; left: {xPxl}px;">
            <span class="plainText">{white}</span><br/>
            <span class="blueText">{blue}</span>
        </div>""".split("\n") if l])
    
    if True:
        buttons = [col.strip().split() for col in BUTTONS.split("\n")]
        for x, col in enumerate(buttons):
            for y, tag in enumerate(col):
                tag = "dot" if tag == '.' else tag
                bfn = ButtonFunction.factory(tag)
                if bfn is None:
                    raise Exception(f"unknown tag '{tag}'")
                _, w, b = bfn.getCaptions()
                print(tpl.format(
                    tag  = tag,
                    xPxl =  79 + 107*x,
                    yPxl = 282 + 128*y,
                    white= w,
                    blue = b))
            print()
    
    app = QApplication([])
    w   = ButtonPanel()
    w.show()
    
    # app.exec()