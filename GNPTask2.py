import random
import pylab
import math

MAXFUNCNUMBER = 100 # Кол-во функций
FUNCSHOWNUMBER = 50 # Кол-во функций, которые выводятся на экран
XMIN = -1 # Максимум значения по X   x c [XMIN; XMAX]
XMAX = 1 # Максимум значения по X   x c [XMIN; XMAX]
FUNCTIONNODECOUNT = 10000 # Кол-во точек на графике исходной функции
APPROXNODECOUNT = 5 # Кол-во точек для апроксимации 

def l_i(i, x, x_nodes):
	result = 1.0
	newX_nodes = [float(xi) for xi in x_nodes]
	for j in range(len(x_nodes)):
		if j != (i - 1):
			result = result * ((x - newX_nodes[j]) / (newX_nodes[i - 1] - newX_nodes[j]))
	return result

def L(x, x_nodes, y_nodes):
	result = 0.0
	newX_nodes = [float(xi) for xi in x_nodes]
	newY_nodes = [float(yi) for yi in y_nodes]
	for i in range(len(newX_nodes)):
		result = result + newY_nodes[i] * l_i(i + 1, x, newX_nodes)
	return result

def funcGeneration():
	funcArray = []
	for i in range(MAXFUNCNUMBER):
		n = random.randint(7, 15)
		m = random.randint(7, 15)
		funcArraySum = [n] + [m]
		for a in range(n):
			funcArraySum = funcArraySum + [random.random()]
		for b in range(m):
			funcArraySum = funcArraySum + [random.random()]
		funcArray = funcArray + [funcArraySum]
	return funcArray

funcsArray = funcGeneration()

def funcCalc(x, funcNumber):
	n = funcsArray[funcNumber][0]
	m = funcsArray[funcNumber][1]
	numerator = 0
	denominator = 1
	for i in range(n):
		numerator = numerator + funcsArray[funcNumber][2 + i] * x ** i
	for j in range(m):
		denominator = denominator + funcsArray[funcNumber][2 + n + j] * x ** j
	return numerator / denominator

for funcNumber in range(FUNCSHOWNUMBER):
	xList = [x * ((XMAX - XMIN) / (FUNCTIONNODECOUNT - 1)) + XMIN for x in range(FUNCTIONNODECOUNT)]
	yList = [funcCalc(i, funcNumber) for i in xList]

	uniformListX = [x * ((XMAX - XMIN) / (APPROXNODECOUNT - 1)) + XMIN for x in range(APPROXNODECOUNT)]
	supportListFirst = [funcCalc(i, funcNumber) for i in uniformListX]
	uniformListY = [L(x, uniformListX, supportListFirst) for x in xList]

	chebyshevListX = [0.5 * (XMIN + XMAX) + 0.5 * (XMAX - XMIN) * math.cos(math.pi * (2 * (i + 1) - 1) / (APPROXNODECOUNT * 2)) for i in range(APPROXNODECOUNT)]
	supportListSecond = [funcCalc(i, funcNumber) for i in chebyshevListX]
	chebyshevListY = [L(x, chebyshevListX, supportListSecond) for x in xList]
	
	normUniform = 0.0
	normChebyshev = 0.0
	for i in range(FUNCTIONNODECOUNT):
		normUniform += (yList[i] - uniformListY[i]) ** 2 
		normChebyshev += (yList[i] - chebyshevListY[i]) ** 2
	normUniform /= FUNCTIONNODECOUNT
	normUniform = math.sqrt(normUniform)
	normChebyshev /= FUNCTIONNODECOUNT
	normChebyshev = math.sqrt(normChebyshev)

	print(normUniform)
	print(normChebyshev)	
	#print(yList)
	#print(supportListFirst)
	#print(supportListSecond)

	pylab.plot (xList, yList)
	pylab.plot (xList, uniformListY)
	pylab.plot (xList, chebyshevListY)

	pylab.title("Functions")
	pylab.legend(("F(X)","L(Xi)","L(Xch)"))
	pylab.show()
