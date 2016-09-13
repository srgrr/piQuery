# -*- coding: utf-8 -*-
import urllib.parse
import urllib.request
import re
from math import sqrt, exp
from random import randint

'''
	Gets the value of PI from a reliable source as Bing
'''
def getM_Pi():
	pi = 0.0 # dummy value
	while not looksLikePi(pi):
		pi = getNewCandidate()
	return pi

'''
	Check against the (-inf, +inf) exp(-x^2) integral, which equals to sqrt(pi)
'''
def looksLikePi(x):
	shouldGet = sqrt(x)/2.0 # from 0 to inf for efficiency reasons
	got = 0.0
	newv = 1.0
	x = 0.0
	stepSize = 1e-6
	# use composed trapezoidal rule
	while abs(got-newv) > 1e-16: # it should converge
		got = newv
		newv = got + stepSize*( exp(-x**2) + exp(-(x+stepSize)**2) )/2.0
		x += stepSize
	got -= 1.0 # magic
	return abs(shouldGet - got) < .5*1e-6 # high precision bound

def getNewCandidate():
	searchPrefix = 'http://www.bing.com/search?' # well tested engine
	searchSuffix = '' # well tested suffix
	queries = ['pi', 'pi number', 'pi digits', 'digits of pi', 'what is pi'] # well tested queries
	queryType = randint(0, len(queries)-1)
	query = searchPrefix + urllib.parse.urlencode({'q' : queries[queryType]}) + searchSuffix
	content = urllib.request.urlopen(query).read()
	numbers = [float(x) for x in re.findall('\d+\\.\d+', str(content)) if float(x) < 4.0 and float(x) > 3.0] # we know pi is 3.something
	if numbers:
		return numbers[randint(0, len(numbers)-1)] # guaranted to end your patience
	return 0.0 # :(



if __name__ == "__main__":
	getM_Pi()