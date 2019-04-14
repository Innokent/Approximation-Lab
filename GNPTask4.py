import numpy
import pylab
import pandas
import math
import matplotlib.pyplot as plt

file = pandas.read_csv('Gaaga.csv', sep=';', header = 6)

y = file['Местное время в Роттердаме / Зестинховене (аэропорт)'][::-1]
y = y.values
lenTime = len(y)
xs = numpy.linspace(1., 30., lenTime)
NODECOUNT = 10000


def qubic_spline_coeff(x_nodes, y_nodes):
	N = len(x_nodes)
	a = []
	b = []
	c = []
	d = []
	h = []
	
	h1 = [1]
	h2 = [0]
	h3 = []

	for i in range(N - 1):
		h += [x_nodes[i + 1] - x_nodes[i]]
	for i in range(N): 
		a += [y_nodes[i]]

	for i in range(len(h) - 1):
		h1 += [2 * (h[i] + h[i + 1])]
		h2 += [h[i + 1]]
		h3 += [h[i]]
	h1 += [1]
	h3 += [0]

	Matrix = numpy.diag(h1, 0) + numpy.diag(h2, 1) + numpy.diag(h3, -1) 
	
	M = [0]
	for i in range(len(h) - 1):
		M += [3 * (a[i+2] - a[i+1]) / h[i + 1] - 3 * (a[i + 1] - a[i]) / h[i]]
	M += [0]

	Matrix = numpy.linalg.inv(Matrix)
	c = numpy.dot(M, Matrix)

	for i in range(len(h)):
		b += [(a[i + 1] - a[i]) / h[i] - h[i] * (c[i + 1] + 2 * c[i]) / 3]
	for i in range(len(h)):
		d += [(c[i + 1] - c[i]) / (3 * h[i])]
	
	return [a, b, c, d]

def qubic_spline(x, qs_coeff, xList):
	N = len(xList)
	index = N - 2
	for i in range(N - 2):
		if ((xList[i] <= x) and (xList[i+1] >= x)):
			index = i
	return qs_coeff[0][index] + qs_coeff[1][index] * (x - xList[index]) + qs_coeff[2][index] * ((x - xList[index]) ** 2) + qs_coeff[3][index] * ((x - xList[index]) ** 3)
	
def d_qubic_spline(x, qs_coeff, xList):
	N = len(xList)
	index = N - 2
	for i in range(N - 1):
		if ((xList[i] <= x) and (xList[i+1] >= x)):
			index = i
	return qs_coeff[1][index] + 2 * qs_coeff[2][index] * (x - xList[index]) + 3 * qs_coeff[0][index] * ((x - xList[index]) ** 2)

def plots (xList, yList):
	qs_coeff = qubic_spline_coeff(xList, yList)
	xNew = numpy.linspace(numpy.min(xList), numpy.max(xList), NODECOUNT)
	yNew = [qubic_spline(i, qs_coeff, xList) for i in xNew]

	pylab.plot(xList, yList, 'o')
	pylab.plot(xNew, yNew)

	pylab.title("Functions")
	pylab.legend(("F(x)","Cubic spline"))
	pylab.show()

def checkingDist (num):
	summ = 0             
	xList = xs[0::num]
	yList = y[0::num]
	qs_coeff = qubic_spline_coeff(xList, yList)
	yNewList = [qubic_spline(i, qs_coeff, xList) for i in xs]
	for i in range(len(xs)):
		summ += (yNewList[i] - y[i]) ** 2
	norm = math.sqrt(math.fabs(summ / len(xs)))
	
	return norm

def dailyTemp (num):
	qs_coeff = qubic_spline_coeff(xs[0::num], y[0::num])
	yNew = [qubic_spline(i, qs_coeff, xs[0::num]) for i in xs]
	daily= numpy.zeros(30)
	for i in range (len(xs)):
		k = (int)(i/30)
		daily[k] = daily[k] + yNew[i]
	return numpy.max(daily/24)

dist = numpy.zeros(2)
dist[0]=checkingDist(3)
dist[1]=checkingDist(6)

print("Dist(every 3 hour) & Dist(every 6 hour) = ", dist)

daily = numpy.zeros(30)
dailyDist = numpy.zeros(len(dist))

for i in range (len(xs)):
    k = (int)(i / 24)
    daily[k] = daily[k] + y[i]
daily = daily / 24

dailyDist[0] = numpy.abs(numpy.max(daily - dailyTemp(3)))
dailyDist[1] = numpy.abs(numpy.max(daily - dailyTemp(6)))

print("Daily dist(every 3 hour) & Daily dist(every 6 hour) = ", dailyDist)




plots (xs, y)
plots (xs[1::3], y[1::3])
plots (xs[1::6], y[1::6])
