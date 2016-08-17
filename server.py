# -*- coding: utf-8 -*-
import zerorpc
import pattern.es as pes

class Lemmatizer(object):
	def lemma(self, text):
		print "Lemmatizacion de", text
		string = pes.parse(text, lemmata=True)
		return [w[-1] for w in string.split()[0]]


s = zerorpc.Server(Lemmatizer())
s.bind("tcp://0.0.0.0:4242")
print "Corriendo"
s.run()

#string = pes.parse('la casa del tío', relations=True, lemmata=True)

#for w in string.split()[0]:
#	print w[-1]
#print string.split()[0]