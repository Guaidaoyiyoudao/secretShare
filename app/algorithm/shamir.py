import random
import numpy
import time
from math import pow


#求逆的函数
def oj(a, n):
	a = a % n
	for x in range(n):
		if x*a%n == 1:
			return x

#解多项式
def dePloy(p, list_xy):
	x_list, y_list = zip(*list_xy)
	secret = 0
	for i in range(len(x_list)):
		xlist_tmp = list(x_list)
		xlist_tmp.remove(x_list[i])
		res_tmp = 0
		numerator = 1
		denominator = 1
		for x_numerator in xlist_tmp:
			numerator = numerator*(-x_numerator)
		for x_denominator in xlist_tmp:
			denominator = denominator*(x_list[i]-x_denominator)
		res = (numerator*oj(denominator,17)*y_list[i])
		secret = (secret+res)%p
	# print(secret)
	return secret


class Shamir(object):
	"""docstring for Shamir"""
	def __init__(self, n, k , secret):
		super(Shamir, self).__init__()
		self.k = k
		self.n = n
		self.secret = secret
		self.p = 17
		self.a = self.Get_a()
		self.list_xy = self.GetPloy()
		

#获取点值
	def GetX(self):
		t = time.time()
		r_1 = int(round(t * 1000)) 
		r_2 = random.randint(1, 15)
		return ((r_1+r_2)%14+1)

#获取参数
	def Get_a(self):
		a_list = []
		for x in range(self.k-1):
			t = time.time()
			t = int(round(t * 1000)) 
			r_2 = random.randint(0, 17)*t
			r_1 = random.randint(0, 17)
			a_list.append((r_1*r_2)%17+1)
		return a_list

#构建多项式
	def GetPloy(self):
		x_list = []
		list_xy = []
		ploy = numpy.poly1d(self.a+[self.secret])
		while len(x_list) < self.n:
			x =  self.GetX()
			if x in x_list:
				continue
			y = (ploy(x))%self.p
			if y > 15:
				continue
			list_xy.append((x,int(y)))
			x_list.append(x)
		# print(ploy)
		# print(list_xy)
		return(list_xy)



#分发点值对
	def DistributeXY(self, i):
		if i < len(self.list_xy):
			return self.list_xy[i]
		else:
			return 0
		

if __name__ == '__main__':

	p1 = Shamir(11, 6, 12)
	a = p1.DistributeXY(0)
	b = p1.DistributeXY(7)
	c = p1.DistributeXY(1)
	d = p1.DistributeXY(2)
	e = p1.DistributeXY(6)
	f = p1.DistributeXY(3)
	print([a,b,c,d])
	print(dePloy(17,[a,b,c,d,e,f]))
	a = p1.DistributeXY(0)
	b = p1.DistributeXY(7)
	c = p1.DistributeXY(1)
	d = p1.DistributeXY(2)
	e = p1.DistributeXY(6)
	f = p1.DistributeXY(3)
	dePloy(17,[a,b,c,d,e,f])
	# print(dePloy(17,[(3, 9), (3, 13), (12, 12), (2, 0)]))




















