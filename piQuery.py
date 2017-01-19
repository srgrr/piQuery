# -*- coding: utf-8 -*-
import urllib.parse
import urllib.request
import random
import re
from math import sqrt, exp


def get_pi():
	'''
	Gets the value of PI from a reliable source as Bing
	'''
	pi = 0.0 # dummy value
	while not looks_like_pi(pi):
		pi = get_new_candidate()
	return pi


def looks_like_pi(x):
	'''
	Check against the (-inf, +inf) exp(-x^2) integral, which equals to sqrt(pi)
	'''
	should_get = sqrt(x)/2.0 # from 0 to inf for efficiency reasons
	got = 0.0
	newv = 1.0
	x = 0.0
	step_size = 1e-6
	# use composed trapezoidal rule
	while abs(got-newv) > 1e-16: # it should converge
		got = newv
		newv = got + step_size*( exp(-x**2) + exp(-(x+step_size)**2) )/2.0
		x += step_size
	got -= 1.0 # magic
	return abs(should_get - got) < .5*1e-6 # high precision bound

def get_new_candidate():
	'''
	Gets a new candidate from the best search engine of the world
	'''
	# well tested engine
	search_prefix = 'http://www.bing.com/search?'
	# well tested suffix
	search_suffix = ''
	# well tested queries
	queries = ['pi', 'pi number', 'pi digits', 'digits of pi', 'what is pi']
	query_type = random.choice(queries)
	query = search_prefix + urllib.parse.urlencode({'q' : query_type}) + search_suffix
	content = urllib.request.urlopen(query).read()
	# we know pi is 3.something
	numbers = [float(x) for x in re.findall('\d+\\.\d+', str(content)) if float(x) < 4.0 and float(x) > 3.0]
	if numbers:
		# guaranteed to end with your patience
		return random.choice(numbers)
	return 0.0 # :(


if __name__ == "__main__":
	print(get_pi())
