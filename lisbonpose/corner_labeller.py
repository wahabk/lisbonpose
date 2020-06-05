from qtpy.QtWidgets import QMessageBox, QApplication, QWidget, QPushButton, QToolTip, QLabel
from qtpy.QtGui import QFont, QPixmap, QImage
from qtpy.QtCore import Qt, QTimer
import numpy as np
import cv2
import sys
from lisbonpose import Lisbon

class Window(QWidget):

	def __init__(self, stack):
		super().__init__()
		self.ogstack = stack
		self.label = QLabel(self)
		self.initUI()

	def initUI(self):
		#initialise UI
		self.setWindowTitle('LisbonPose')
		self.update()
		self.resize(self.pixmap.width(), self.pixmap.height())

	def update(self):
		#Update displayed image
		self.image = self.np2qt(self.npstack)
		self.pixmap = QPixmap(QPixmap.fromImage(self.image))
		self.label.setPixmap(self.pixmap)
		
	def keyPressEvent(self, event):
		#close window if esc or q is pressed
		if event.key() == Qt.Key_Escape or event.key() == Qt.Key_Q :
			self.close()

	def np2qt(self, image):
		#transform np cv2 image to qt format
		# cv2.putText(image, str(self.slice), (10,50), cv2.FONT_HERSHEY_SIMPLEX, 
		# 	2, (255,255,255), 2, cv2.LINE_AA)
		
		if self.grayscale == True:
			height, width = image.shape
			bytesPerLine = width
			return QImage(image.data, width, height, bytesPerLine, QImage.Format_Indexed8)
		else:
			height, width, channel = image.shape
			bytesPerLine = 3 * width
			return QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)

class order_labeller(Window):
	def __init__(self, stack):
		super().__init__(stack) #inherit methods from vie.window
		self.ogstack = stack
		self.corners = []
		self.corners_labels = ['Tl', 'TR', 'BR', 'BL']
		self.order = 0
		self.initUI()

	def initUI(self):
		#initialise UI
		self.setWindowTitle('[LisbonPose] please click on the corners in order')
		self.update()
		self.label.mousePressEvent = self.getPixel
		self.resize(self.pixmap.width(), self.pixmap.height())

	def getPixel(self , event):
		#get pixels of every click and assign circle order
		x = event.pos().x()
		y = event.pos().y()
		self.corners.append([x,y])
		self.draw_corner(x, y)

	def draw_corner(self, x, y):
		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(slice_, str(self.corners_labels[self.order]), (x,y), font, 4, (255,255,255), 2, cv2.LINE_AA)
		self.order += 1
		self.update()
		if self.order == 4: self.check()

	def check(self):
		self.b1 = QPushButton("Happy?", self)
		self.b1.toggle()
		self.b1.clicked.connect(self.Happy)
		self.b1.move(30, 50)

		self.b1 = QPushButton("Retry", self)
		self.b1.toggle()
		self.b1.clicked.connect(self.unHappy)
		self.b1.move(80, 50)

	def Happy(self):
		self.success = True
		self.close()

	def unHappy(self):
		self.success = False
		self.close()

	def get_corners(self):
		return self.success, np.array(self.corners), self.npstack


def corner_labeller(img):
	success = False
	while success == False:
		app = QApplication(sys.argv)
		ex = order_labeller(labelled_img)
		ex.show()
		app.exec_()
		success, corners, image = ex.get_corners()
	return corners, image


if __name__ == "__main__":
	lisbon = Lisbon()
	vidpath = 'Data/Videos/PA_02_LAC_13.mp4'
	image = lisbon.getFrame(vidpath)

	cv2.imshow('image', image)
	cv2.waitKey(27)


