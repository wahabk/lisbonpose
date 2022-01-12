import math
import numpy as np 
import matplotlib.pyplot as plt 
import random


class Person():
	def __init__(self):
		self.time = 0 # frames
		self.nSteps = random.randrange(5,10)
		self.m = random.uniform(-0.05, 0.05)
		if self.m == 0: self.m = 0.01
		self.a = random.uniform(0.8,1.2)
		self.c = random.randrange(-20,20)
		self.stepRate = random.uniform(0.03,0.06) # this controls nsteps
		self.speed = 2.5 # TODO CHANGE TO CM/S
		self.stanceWidth = 60 #random.randrange(40,60)
		self.strideLength = 70#random.randrange(60,80)

		self.trueCenter = [0, self.c]
		self.leftFoot = [0, self.trueCenter[0]-(self.stanceWidth/2)]
		self.rightFoot = [0, self.trueCenter[0]-(self.stanceWidth/2)]
		self.noise = 0

	
	def getTrajY(self, xt):
		return self.m*(xt**self.a)-self.c

	def getFeetX(self, xt):
		Lx = xt + (self.strideLength*math.sin((self.stepRate*xt)))
		Rx = xt + (self.strideLength*math.sin((self.stepRate*xt)+math.pi))
		return Rx, Lx

	def update(self,t):
		self.trueCenter[0] = t *self.speed
		self.trueCenter[1] = self.getTrajY(self.trueCenter[0])
		Lx, Rx = self.getFeetX(self.trueCenter[0])
		self.leftFoot = [Lx, self.trueCenter[1]-(self.stanceWidth/2)]
		self.rightFoot = [Rx, self.trueCenter[1]+(self.stanceWidth/2)]
		



if __name__ == '__main__':
	while True:
		TC = []
		LF = []
		RF = []
		person = Person()
		tsteps = [i for i in range(0,200)]
		for t in tsteps:
			person.update(t)
			print(person.trueCenter, person.leftFoot, person.rightFoot)
			TC.append(person.trueCenter)
			LF.append(person.leftFoot)
			RF.append(person.rightFoot)
		TC = np.array(TC)
		LF = np.array(LF)
		RF = np.array(RF)
		
		
		print(TC.shape)
		print(LF.shape)
		print(RF.shape)
		x = np.arange(0, 500, 2.5)
		plt.plot(x, TC, 'go')
		plt.plot(x, LF, 'bo')
		plt.plot(x, RF, 'ro')
		# plt.title('sine wave')
		# plt.xlabel('x distance')
		# plt.ylabel('foot acceleration')
		# plt.axhline(y=0, color='k')
		plt.xlim(0,500)
		plt.ylim(-100,100)
		plt.show()
		plt.cla()



	
	
	
	
	
	
def visualise():
	canvasshape = [500,100]
	scale = 0.06
	x = np.arange(0, 500, 0.1)
	y = [70*math.sin(scale*xi) for xi in x]
	yl = [70*math.sin((scale*xi)+math.pi) for xi in x]


	m = random.uniform(-0.05, 0.05)
	a = random.uniform(0.8,1.2)
	c = random.randrange(-20,20)
	y = [m*xi**a-c	 for xi in x]
	plt.plot(x, y, color='b')
	plt.plot(x, yl, color='r')
	plt.title('sine wave')
	plt.xlabel('x distance')
	plt.ylabel('foot acceleration')
	plt.axhline(y=0, color='k')
	plt.xlim(0,500)
	plt.ylim(-100,100)
	plt.show()





