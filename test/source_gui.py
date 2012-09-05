#!/usr/bin/env python

import sys
sys.path.append("/usr/local/lib/python2.7/site-packages/")
sys.path.append("..")

from PySide.QtCore import QThread, Signal, QObject, QFile
from PySide.QtGui import QApplication, QListWidgetItem
from PySide.QtUiTools import QUiLoader
from Litterfinger.tools import const, rand, choice, gen_auto_iter
from Litterfinger import Source

def obj2str(d):
	return "%s" % ", ".join(["%s: %s" % i for i in d.items()])

class SourceThread(QThread):
	itemSent = Signal(str)

	def __init__(self, source, gen_iter):
		QThread.__init__(self)
		self.source = source
		self.gen_iter = gen_iter

	def run(self):
		for item in self.gen_iter:
			self.source.send(item)
			self.itemSent.emit(obj2str(item))


class GuiProxy(QThread):
	def __init__(self, ui_file):
	    loader = QUiLoader()
	    f = QFile(ui_file)
	    f.open(QFile.ReadOnly)
	    self.widget = loader.load(f)
	    f.close()
	    self.widget.startButton.clicked.connect(self.start_source)
	    self.source = None
	    self.widget.show()

	def start_source(self):
		if self.source:
			self.source.terminate()
			self.source.itemSent.disconnect(self.add_item)
		config = self.get_config()
		gen_iter = gen_auto_iter(config)
		host = self.widget.hostAddrEdit.text()
		source = Source(host)
		self.source = SourceThread(source, gen_iter)
		self.source.itemSent.connect(self.add_item)
		self.source.start()

	def get_config(self):
		pt = self.widget.configEdit.toPlainText()
		bl = []
		for line in pt.splitlines():
			l = line.strip().split("=")
			var = l[0].strip()
			val = "".join(l[1:]).strip()
			bl.append("\"%s\":%s" % (var, val))
		block = "{%s}" % ",".join(bl)
		conf = eval(
				block, 
				{"const":const, "rand":rand, "choice":choice})
		return conf

	def add_item(self, text):
		self.widget.sentWidget.addItem(QListWidgetItem(text))

if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	gui = GuiProxy("source_ui.ui")
	sys.exit(app.exec_())
