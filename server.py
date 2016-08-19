# -*- coding: utf-8 -*-
import zerorpc
import pattern.es as pes
import os



class Lemmatizer(object):
	def lemma(self, text):
		print "Lemmatizacion de", text

		#Get lemmas of the phrase
		string = pes.parse(text, lemmata=True)
		words = filter(string.split()[0])

		#Get videos of words. If the word doesnt have a video, add each letter as a word
		final = []
		for word in words:
			if os.path.exists(os.getcwd() + '\\vids\\' + word + '.mp4'):
				final.append(word)
			else:
				final.extend(word)
		return final

##Remove articles and verb "ser"
def filter(string):
	final = []
	for w in string:

		if w[-1] == 'el':
			continue
		elif w[-1] == 'ser':
			continue
		elif w[-1] == 'del':
			final.append('de')
		elif w[-1] == 'al':
			final.append('a')
		else:
			final.append(w[-1])
	return final

def semiStemmer(word):
	pronouns = ["me", "se", "sele", "selo", "sela", "selos", "selas", "seles", "la", "le", "lo", "las", "les", "los", "nos"]
	verbCases = ["iéndo", "ándo", "ár", "ér", "ír",
			"ando", "iendo", "ar", "er", "ir"]
	caseC = ["yendo"]

	vowels = ["a", "á", "e", "é", "i", "í", "o", "ó", "u", "ú", "ü"]
	consonants = ["b","c","d","f","g","h","j","k","l","m","n","p","q","r","s","t","v","w","x","y","z"]

	maxN = 0
	pronoun = ''
	print word[-3:]
	for p in pronouns:
		print p, len(p), word[-len(p):]
		if p == word[-len(p):]:
			print p
			if maxN < len(p):
				maxN = len(p)
				pronoun = p

	p1 = ''
	p2 = ''
	if maxN > 3:
		p1, p2 = pronoun[:2], pronoun[2:]


	print word[:len(word)-maxN], p1, p2


semiStemmer('acercándoseles')

#s = zerorpc.Server(Lemmatizer())
#s.bind("tcp://0.0.0.0:4242")
#print "Corriendo"
#s.run()


string = pes.parse('coma', relations=True, lemmata=True)

#a = Lemmatizer()
#print a.lemma('come me')


pes.pprint(string)