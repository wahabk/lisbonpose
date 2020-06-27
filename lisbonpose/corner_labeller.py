from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget, QPushButton, QToolTip, QLabel
from PyQt5.QtGui import QFont, QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer
import numpy as np
import cv2
import sys
from lisbonpose import Lisbon

class Window(QWidget):

	def __init__(self, stack):
		super().__init__()
		self.npstack = stack.copy()
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
		
		height, width, channel = image.shape
		bytesPerLine = 3 * width
		return QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)

class order_labeller(Window):
	def __init__(self, stack):
		super().__init__(stack) #inherit methods from vie.window
		self.corners = []
		self.corners_labels = ['TL', 'TR', 'BR', 'BL']
		self.order = 0
		self.success = False
		self.initUI()

	def initUI(self):
		#initialise UI
		self.setWindowTitle('[LisbonPose] please click on the corners in order TL, TR, BR, BL')
		self.update()
		self.label.mousePressEvent = self.getPixel
		self.resize(self.pixmap.width(), self.pixmap.height())

		self.b1 = QPushButton("Happy?", self)
		self.b1.toggle()
		self.b1.clicked.connect(self.Happy)
		self.b1.move(30, 50)

		self.b2 = QPushButton("Retry", self)
		self.b2.toggle()
		self.b2.clicked.connect(self.unHappy)
		self.b2.move(130, 50)

	def getPixel(self , event):
		#get pixels of every click and assign circle order
		x = event.pos().x()
		y = event.pos().y()
		if self.order < 4:
			self.corners.append([x,y])
			self.draw_corner(x, y)

	def draw_corner(self, x, y):

		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(self.npstack, str(self.corners_labels[self.order]), (x,y), font, 2, (255,255,255), 2, cv2.LINE_AA)
		cv2.rectangle(self.npstack, (x - 5, y - 5), (x + 5, y + 5), (255, 0, 0), -1)
		self.order += 1
		self.update()

	def Happy(self):
		if self.order == 4:
			self.success = True
			self.close()

	def unHappy(self):
		self.close()

	def get_corners(self):
		return self.success, np.array(self.corners, dtype = "float32")

def corner_labeller(img):

	app = QApplication(sys.argv)
	ex = order_labeller(img)
	ex.show()
	app.exec_()
	success, corners = ex.get_corners()
	return success, corners


if __name__ == "__main__":
	lisbon = Lisbon()
	vidpath = 'Data/clean/01/LAC/L2/Y_01_LAC_L2_C.mp4'
	image = lisbon.getFrame(vidpath)

	success = False
	while success == False:
		success, corners = corner_labeller(image)

	print(corners)
	tfm = lisbon.get_tfm_2(corners)
	print(tfm)
	warped = cv2.warpPerspective(image, tfm, (500,150)) #This bit crops around rectangle
	
	cv2.imshow('image', warped)
	cv2.waitKey()


