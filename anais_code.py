#!/usr/bin/env python

import os
import sys

from math import cos, sin
import numpy as np

import Tkinter as tk
import ttk
import ScrolledText as st

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

############# Morse code #############
#		- The length of a dot in one unit
#		- A dash is three units 
#		- The space between parts of the same letter is one unit
#		- The space between letters is three units
#		- The space between words is seven units

class test():
	def __init__(self):
		self.msg = ""

		self.MORSE = dict(zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ', [
	    '.-', '-...', '-.-.', '-..', '.', '..-.', '--.', '....',
	    '..', '.---', '-.-', '.-..', '--', '-.', '---', '.--.',
	    '--.-', '.-.', '...', '-', '..-', '...-', '.--', '-..-',
	    '-.--', '--..']))

		print("morse code : " + str(self.MORSE) + "\n")

		# Read a file containing A-Z only words, one per line.
		# self.WORDS = set(word.strip().upper() for word in open('/usr/share/dict/american-english').readlines())
		self.WORDS = set(word.strip().upper() for word in open('/usr/share/dict/french').readlines())
		# self.WORDS = set(word.strip().upper() for word in open('/home/hbildstein/anais_code_ws/dict').readlines())

		# A set of all possible prefixes of English words.
		self.PREFIXES = set(word[:j+1] for word in self.WORDS for j in xrange(len(word)))

	def translate(self, msg, c_sep=' ', w_sep=' / '):
	    """Turn a message (all-caps space-separated words) into morse code."""
	    return w_sep.join(c_sep.join(self.MORSE[c] for c in word)
	                      for word in msg.split(' '))

	def encode(self, msg):
	    """Turn a message into timing-less morse code."""
	    return self.translate(msg, '', '')

	def c_trans(self, morse):
		"""Construct a map of char transitions.

		The return value is a dict, mapping indexes into the morse code stream
		to a dict of possible characters at that location to where they would go
		in the stream. Transitions that lead to dead-ends are omitted.
		"""
		result = [{} for i in xrange(len(morse))]
		for i_ in xrange(len(morse)):
			i = len(morse) - i_ - 1
			for c, m in self.MORSE.iteritems():
				if i + len(m) < len(morse) and not result[i + len(m)]:
					continue
				if morse[i:i+len(m)] != m:
					continue
				result[i][c] = i + len(m)
		return result

	def find_words(self, ctr, i, prefix=''):
	    """Find all legal words starting from position i.

	    We generate all possible words starting from position i in the
	    morse code stream.
	    ctr is a char transition dict, as produced by c_trans.
	    """
	    if prefix in self.WORDS:
	        yield prefix, i
	    if i == len(ctr): return
	    for c, j in ctr[i].iteritems():
	        if prefix + c in self.PREFIXES:
	            for w, j2 in self.find_words(ctr, j, prefix + c):
	                yield w, j2

	def w_trans(self, ctr):
	    """Like c_trans, but produce a word transition map."""
	    result = [{} for i in xrange(len(ctr))]
	    for i_ in xrange(len(ctr)):
	        i = len(ctr) - i_ - 1
	        for w, j in self.find_words(ctr, i):
	            if j < len(result) and not result[j]:
	                continue
	            result[i][w] = j
	    return result

	def sentence_count(self, wt):
	    result = [0] * len(wt) + [1]
	    for i_ in xrange(len(wt)):
	        i = len(wt) - i_ - 1
	        for j in wt[i].itervalues():
	            result[i] += result[j]
	    return result[0]

	def all_sentences(self, wt):
		"""Given a word transition map, find all possible sentences.

		"""
		all_sentences = [[] for i in range(len(wt)+1)]
		result = [-1 for i in range(len(wt))] + [0]

		for i_ in xrange(len(wt)):
			i = len(wt) - i_ - 1
			for w, j in wt[i].iteritems():
				if result[j] == -1:
					continue
				result[i] = 0

				if all_sentences[j]:
					for s in all_sentences[j]:
						# print([w] + s)
						# val = raw_input("Is possible (yn) : ")
						# if val == 'y':
						all_sentences[i].append([w] + s)
				else:
					all_sentences[i].append([w])

		print(all_sentences)

		return all_sentences[0]

	def isCorrect(self, msg_encoded, all_sentences):
		"""Check if all possible sentences are ok.

		"""
		for i, sentence in enumerate(all_sentences):
			if sentence == ['LA', 'VIE', 'EST', 'BELLE']:
				print(sentence)
			# print(str(i) + " : " + str(sentence))
			sentence = ''.join(sentence)
			if msg_encoded != self.encode(sentence):
				return False
		return True

	def main(self):
		# self.msg = 'LA VIE EST BELLE'
		self.msg = 'LA VIE'

		msg_encoded = self.encode(self.msg)
		# msg_encoded = '.-..--..-...-...-...-.....-..--.-..-..-.----'
		print("msg encoded : " + str(msg_encoded) + "\n")
		print("size msg : " + str(len(msg_encoded)) + "\n")

		# Caractere Map 
		# cmap = self.c_trans(self.encode(self.msg))
		cmap = self.c_trans(msg_encoded)

		print("cmap = " + str(cmap) + "\n")

		# Words Map 
		wmap = self.w_trans(cmap)
		print("wmap = " + str(wmap) + "\n")

		# Sentences count
		nb_sentences = self.sentence_count(wmap)
		print("nb sentences = " + str(nb_sentences))

		# Possible sentences 
		all_sentences = self.all_sentences(wmap)
		# print(all_sentences)

		# Test if correct
		print(self.isCorrect(msg_encoded, all_sentences))


if __name__ == '__main__':
	tester = test()
	tester.main()

















