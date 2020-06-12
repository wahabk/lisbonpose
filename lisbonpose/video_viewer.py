from qtpy.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QToolTip, QLabel, QVBoxLayout, QSlider, QGridLayout
from qtpy.QtGui import QFont, QPixmap, QImage
from qtpy.QtCore import Qt, QTimer
import matplotlib.pyplot as plt
import numpy as np
import cv2
import sys
from lisbonpose import Lisbon

class MainWindow(QMainWindow):

	def __init__(self, vidpath):
		super().__init__()
		self.vidpath = vidpath
		self.initUI()

	def initUI(self):
		#initialise UI
		self.setWindowTitle('Lisbonpose video viewer')
		self.statusBar().showMessage('Status bar: Ready')
		
		self.viewer = Viewer(self.vidpath)
		self.setCentralWidget(self.viewer)
		#widget.findChildren(QWidget)[0]

		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		self.setGeometry(1100, 10, self.viewer.width(), self.viewer.height())
		
	def keyPressEvent(self, event):
		#close window if esc or q is pressed
		if event.key() == Qt.Key_Escape or event.key() == Qt.Key_Q :
			self.close()

class Viewer(QWidget):

	def __init__(self, vidpath):
		super().__init__()
		self.framenum = 0
		self.vidpath = vidpath
		self.label = QLabel(self)

		vidcap = cv2.VideoCapture(vidpath)
		vidcap.set(cv2.CAP_PROP_POS_AVI_RATIO,1)
		length = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)-20
		self.vidlength = int(length)

		lisbon = Lisbon()

		p = self.palette()
		p.setColor(self.backgroundRole(), Qt.cyan)
		self.setPalette(p)
		self.setAutoFillBackground(True)

		self.initSlider()
		self.initUI()


	def initUI(self):
		#initialise UI
		self.update()
		self.slider.setGeometry(10, self.pixmap.height()+10, self.pixmap.width(), 50)
		self.label.setMargin(10)
		self.setGeometry(0, 0, self.pixmap.width()+20, (self.pixmap.height()+self.slider.height()*2))
		self.slider.valueChanged.connect(self.valuechange)

	def update(self):
		#Update displayed image
		lisbon = Lisbon()
		self.npimage = lisbon.getFrame(self.vidpath, self.framenum)
		self.npimage = cv2.resize(self.npimage, (960, 540))     
		self.image = self.np2qt(self.npimage)
		self.pixmap = QPixmap(QPixmap.fromImage(self.image))
		self.label.setPixmap(self.pixmap)

	def wheelEvent(self, event):
		#scroll through slices and go to beginning if reached max
		self.framenum = self.framenum + int(event.angleDelta().y()/120)*5
		if self.framenum > self.vidlength: 	self.framenum = 0
		if self.framenum < 0: 					self.framenum = self.vidlength
		self.slider.setValue(self.framenum)
		self.update()

	def np2qt(self, image):
		#transform np cv2 image to qt format
		height, width, channel = image.shape
		bytesPerLine = 3 * width
		return QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
	
	def initSlider(self):
		self.slider = QSlider(Qt.Horizontal, self)
		self.slider.setMinimum(0)
		self.slider.setMaximum(self.vidlength)

	def valuechange(self):
		self.framenum = self.slider.value()
		self.update()

	def getframenum(self):
		return self.framenum



def video_viewer(vidpath):
	app = QApplication(sys.argv)
	win = MainWindow(vidpath)
	win.show()
	app.exec_()
	return win.viewer.getframenum()


if __name__ == "__main__":
	lisbon = Lisbon()
	vidpath = 'Data/clean/01/LAC/L2/Y_01_LAC_L2_C.mp4'
	
	framenum = video_viewer(vidpath)
	print(framenum)




