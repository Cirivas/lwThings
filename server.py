# -*- coding: utf-8 -*-
import zerorpc
import pattern.es as pes
import os



class Lemmatizer(object):
	def lemma(self, text):
		print "Lemmatizacion de", text

		#Get lemmas of the phrase
		string = pes.parse(text, lemmata=True)
		words = [w[-1] for w in string.split()[0]]

		#Get videos of words. If the word doesnt have a video, add each letter as word
		final = []
		for word in words:
			if os.path.exists(os.getcwd() + '\\vids\\' + word + '.mp4'):
				final.append(word)
			else:
				final.extend(word)
		return final


s = zerorpc.Server(Lemmatizer())
s.bind("tcp://0.0.0.0:4242")
print "Corriendo"
s.run()



#string = pes.parse('la casa del tío', relations=True, lemmata=True)

#final = []
##words = [w[-1] for w in string.split()[0]]
#for word in words:
#	if os.path.exists(os.getcwd() + '\\' + word + '.mp4'):
#		final.append(word)
#	else:
#		for letter in list(word):
#			final.append(letter)
#print final
#print string.split()[0]