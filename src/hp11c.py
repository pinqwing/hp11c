import json
from pathlib import Path
from enum import Enum

from PyQt5.Qt import *  # @UnusedWildImport
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage

import hp11cDebug
from engine.calculator import HP11C, AngularMode


class DisplayLabel(Enum):
    displ = "mantissa"
    user  = "lblUser"
    f     = "lblFmod"
    g     = "lblGmod"
    begin = "lblBgin"
    angle = "lblGrad"
    # cmpd = "lblCmpd"
    prog  = "lblPrgm"
    


class HtmlBridge(QObject):
    textChanged = pyqtSignal(str, str)
    showLabel   = pyqtSignal(str, str)
    
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.onClick    = lambda tag: tag
        self.onKeyPress = lambda evt: evt.get("key", "")

    @pyqtSlot(str)  
    def buttonClicked(self, tag):
        print(f"Klik ontvangen voor: {tag}")
        self.displayText(self.onClick(tag))

    
    @pyqtSlot(str)  
    def keyPressed(self, event):
        event = json.loads(event)
        print(f"ontvangen voor: {event}")
        text = self.onKeyPress(event)
        if text is not None:
            self.displayText(text)

    
    def showHideLabel(self, label: DisplayLabel, visible: bool):
        self.showLabel.emit(label.value, "hidden" if not visible else "visible")
        
        
    def displayText(self, text, label = DisplayLabel.displ):
        self.textChanged.emit(label.value, text)


        
    
class HP11cUI(QWebEngineView):
    textChanged = pyqtSignal(str, str)
    showLabel   = pyqtSignal(str, str)

    contentFile = Path(__file__).parent.parent / "html/gui.html"
    
    class WebPage(QWebEnginePage):
        def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
            print(f"JsConsole({Path(sourceID).name}: {lineNumber}) - {message}")        

        
    def __init__(self):
        super().__init__()
        # self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        self.bridge  = HtmlBridge()
        self.channel = QWebChannel()
        self.channel.registerObject("backend", self.bridge)

        self.webPage = self.WebPage()
        self.webPage.setWebChannel(self.channel)
        self.webPage.loadFinished.connect(self.loadFinished)
        self.setPage(self.webPage)
        
        self.load(QUrl(f"file://{self.contentFile}"))
        self.setFixedSize(QSize(660, 440))
        self.calculator = HP11C()
        self.debugger   = hp11cDebug.HP11cDebugView(self.calculator)

        self.bridge.onClick     = self.keyClicked
        self.bridge.onKeyPress  = self.keyPressed
        self.show()
        

    def load(self, url):
        super().load(url)
        QTimer.singleShot(500, lambda: self.sync())


    def keyClicked(self, tag):
        if tag == HP11C.DEBUG:
            self.toggleDebugger()
        else:
            text = self.calculator.calculatorKey(tag)
            self.debugger.sync()
            
            if text == HP11C.QUIT:
                QApplication.instance().quit()
            
        return self.calculator.currentDisplay()
       
        
    def keyPressed(self, keyboardEvent):
        if keyboardEvent.get("key", "") == "?":
            self.toggleDebugger()
        else:
            self.calculator.keyboardKey(**keyboardEvent)
            self.debugger.sync()
        return self.calculator.currentDisplay()

        
    def setAngularMode(self, mode: AngularMode):
        self.bridge.displayText(mode.value, DisplayLabel.angle)
        self.bridge.showHideLabel(DisplayLabel.angle, visible = True)
        
        
    def toggleDebugger(self):
        if self.debugger.isVisible():
            self.debugger.close()
        else:
            self.debugger.open(self.pos().x() + self.width(), self.pos().y())
        
                
    def sync(self):
        self.setAngularMode(self.calculator.angularMode)



if __name__ == '__main__':


    app = QApplication([])
 
    b1 = HP11cUI() 
    app.exec_() 