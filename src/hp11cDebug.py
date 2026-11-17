from pathlib import Path

from PyQt5.Qt import *  # @UnusedWildImport
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings

template = """<html><head><style>
body {{
  overflow: hidden; /* Hide scrollbars */
}}
table, th, td {{
  border: 1px solid gray;
  border-collapse: collapse;
  padding: 5px;
}}</style></head>
<body>
    <table width="100%">
        {content}
    </table>
</body></html>"

"""


class HP11cDebugView(QWebEngineView):
    def __init__(self, calculator):
        super().__init__()
        self.calculator = calculator
        self.setFixedSize(QSize(200, 130))
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
    def open(self, x, y):
        self.move(x, y)
        self.show()
        self.sync()


    def sync(self):
        getter = lambda attr: (attr, getattr(self.calculator, attr, "???"))
        n_v    = [getter(n) for n in "tzyx"]
        rows   = [f"\n<tr><td><b>{name}</b></td><td>{value}</td></tr>" for name, value in n_v]
        html   = template.format(content = ''.join(rows))
        self.setHtml(html)        
        