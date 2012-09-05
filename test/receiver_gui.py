#!/usr/bin/env python

import sys
sys.path.append("/usr/local/lib/python2.7/site-packages/")
sys.path.append("..")

from PySide.QtCore import QThread, Signal, QObject, QFile
from PySide.QtGui import QApplication, QListWidgetItem
from PySide.QtUiTools import QUiLoader
from Litterfinger import Receiver

def obj2str(d):
	return "%s" % ", ".join(["%s: %s" % i for i in d.items()])

class ReceiverThread(QThread):
	newItem = Signal(str)

	def __init__(self, receiver):
		QThread.__init__(self)
		self.receiver = receiver

	def run(self):
		for item in self.receiver:
			self.newItem.emit(obj2str(item))

class GuiProxy(QThread):
	def __init__(self, ui_file):
	    loader = QUiLoader()
	    f = QFile(ui_file)
	    f.open(QFile.ReadOnly)
	    self.widget = loader.load(f)
	    f.close()
	    self.widget.startButton.clicked.connect(self.start_recv)
	    self.widget.subsEdit.returnPressed.connect(self.start_recv)
	    self.receiver = None
	    self.widget.show()

	def start_recv(self):
		if self.receiver:
			self.receiver.terminate()
			self.receiver.newItem.disconnect(self.add_item)
		subs = self.widget.subsEdit.text()
		host = self.widget.hostAddrEdit.text()
		receiver = Receiver(subs, host)
		self.receiver = ReceiverThread(receiver)
		self.receiver.newItem.connect(self.add_item)
		self.receiver.start()
		
	def add_item(self, text):
		self.widget.receivedWidget.addItem(QListWidgetItem(text))

if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	gui = GuiProxy("receiver_ui.ui")
	sys.exit(app.exec_())