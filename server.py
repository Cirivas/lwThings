# -*- coding: utf-8 -*-
import zerorpc
import pattern.es as pes
from unidecode import unidecode
import os

'''
Notas:

- Resolver qué hacer con palabras que se escriben igual pero tienen distinto significado. 
- Marcar palabras que representan a hombre y mujer (esposo-esposa, tío-tía, él-ella, etc) => hay que listar todas las posibilidades. 
- Pasar oraciones en voz pasiva a voz activa para hacer más claro el enunciado (el dado fue dado por mí => yo di el dado)
- Crear las marcas de pasado, presente y futuro. Esto corresponde a identificar el tiempo verbal del verbo principal de la oración. Hay frases
que tienen el mismo valor de pasado e.g. ha corrido = corrió, pero a su vez, no es lo mismo corrió que corría, ambos tienen distinta marca en seña:
corrió = correr + pasado + marca de finalización (pasado simple). 
corría = correr + pasado + marca de incertidumbre (imperfecto).
- Invertir el orden cuando se trata de posesión (uso de 'de'). A considerar:
	* Si 'de' está entre un sustantivo o adjetivo y un sustantivo o posesivo, se hace la inversión.
		- La casa grande de mi abuelo => mi-abuelo de casa-grande.
	* Cualquier otro uso de 'de' debe ser investigado: Origen (viene de, despertó de), Material (cuchara de palo, plato de cerámica), Locuciones (de corazón, de verdad, de alegría),
	Magnitud (velocidad de, vientos de), Aposición (cuidad de España, pueblo de Sevilla), Diferencia (distinto de, diferente de), Contenido (vaso de agua, botella de vino), Edad, Empleo,
	Abundancia, Partitivo.
- Resolver como marcar los verbos de Concordancia (aquellos que tienen dos sujetos involucrados, e.g. decir) y los verbos espacio-locativos (aquellos que están ligados al objeto, e.g. mover)
- Frases interrogativas: la palabra que marca la pregunta (cómo, por qué, cuál, etc) va al final. => Listo.
- Los números pueden ir en distintas partes del enunciado, generalmente al final si están ligados al verbo (querer X cosas => cosas querer X).
- En frases subordinadas, se puede simplemente eliminar el 'que' y dividir en partes la oración, dejando el verbo después del 'que' al final:
	* El dijo que ella no canta muy bien => el decir ella no bien cantar. => Listo.
'''
#

class Lemmatizer(object):
	def lemma2(self, text):
		print "Lemmatizacion de", text

		#Get lemmas of the phrase
		string = pes.parse(text, lemmata=True)
		words = filter(string.split()[0])

		#Get videos of words. If the word doesnt have a video, add each letter as a word
		print words
		final = []
		for word in words:
			
			if os.path.exists(os.getcwd() + '/vids/' + word + '.mp4'):
				final.append(word)
			else:
				final.extend(word)
		return final
	def lemma(self, text):
		print "Lematizacion de", text

		#Create file
		meh = open("meh", "w")
		meh.write(text)
		meh.close()

		#Run script
		stream = os.popen("analyze -f es.cfg  < meh")

		#Get lemmas
		words = freelingParser(stream)

		final = []
		for word in words:
			
			if os.path.exists(os.getcwd() + '/vids/' + word + '.mp4'):
				final.append(word)
			else:
				final.extend(word)
		return final

##Remove articles and verb "ser" and "que"
def filter(string):
	final = []
	for w in string:
		if w[-1] == u'el':
			continue
		elif w[-1] == u'ser':
			continue
		elif w[-1] == u'que':
			continue
		elif w[-1] == u'del':
			final.append('de')
		elif w[-1] == u'al':
			final.append('a')
		elif w[-1] == u'porque':
			#Pausa
			final.append('*')
		else:
			if w[1] == 'VBN':
				prons = semiStemmer(w[0])
				final.append(prons[1])
				if prons[2] != '':
					final.append(prons[2])
				final.append((pes.parse(prons[0], lemmata=True)).split()[0][0][-1])
				
			else:
				final.append(w[-1])
	return final

def semiStemmer(word):
	pronouns = ["me", "se", "sele", "selo", "sela", "selos", "selas", "seles", "la", "le", "lo", "las", "les", "los", "nos"]
	oldEnd = ["iéndo", "ándo", "ár", "ér", "ír"]
	newEnd = ["iendo", "ando", "ar", "er", "ir"]

	vowels = ["a", "á", "e", "é", "i", "í", "o", "ó", "u", "ú", "ü"]
	consonants = ["b","c","d","f","g","h","j","k","l","m","n","p","q","r","s","t","v","w","x","y","z"]

	maxN = 0
	pronoun = ''
	for p in pronouns:
		if p == word[-len(p):]:
			if maxN < len(p):
				maxN = len(p)
				pronoun = p
	newWord = word[:len(word)-maxN]

	p1 = ''
	p2 = ''
	if maxN > 3:
		p1, p2 = pronoun[:2], pronoun[2:]
	else:
		p1 = pronoun

	print unidecode(newWord), p1, p2
	return unidecode(newWord), p1, p2

def freelingParser(frobject):
	final = []

	#this variable helps to identify a participe verb used as a noun (el helado), so we do not add the lemma (helar).
	flagDet = False

	verb = ''
	question = ''
	pronoun = ''

	i = 0
	subjectPos = 0
	questionMarks = ['qué', 'cómo']
	femeninWords = ['ella', 'esposa', 'tía']

	pronouns = ["yo", "tú", "usted", "él","ella", "nosotros", "vosotros", "ustedes", "ellos", "ellas"]
	pronounsDict = { "1S": "yo", "2S": "tú", "3S": "él",
					 "1P": "nosotros", "2P": "ustedes", "3P": "ellos"}

	tenses ={"I":"(imperfecto)", "F":"(futuro)","S":"(pasado)","C":"(condicional)"}
	for line in frobject:
		print line.strip()
		line = line.strip().split(' ')
		if len(line) < 2:
			continue
		elif line[1] == 'el':
			flagDet = True
			continue
		elif line[1] == 'ser':
			continue
		elif line[1] == 'que':
			final.append(verb)
			continue
		elif line[1] in '¿?':
			continue
		else:
			if flagDet and line[2][0] == 'V':
				#if an article was removed, and the current word is a identified as a verb, it is really a noun, so we do not add the lemma.
				#e.g. 'el helado', 'el dado'.
				final.append(line[0])
				flagDet = False
			elif line[0] in questionMarks:
				#store question word to put it at the end
				question = line[0]

			elif line[0] in femeninWords:
				#Words like "ella", "esposa" have a masculine lema, but we need to keep it in femenine
				final.append(line[0])

			elif line[2][0] == 'V' and line[2][2] != 'N':
				#store verb to put it at the end			
				verb = line[1]

				#identify subject and tense
				#TODO: 2 verbal times, 2 subjects
				if line[2][3] != 'P':
					final.insert(0, tenses[line[2][3]])
					subjectPos += 1

				flag = False
				for p in pronouns:
					if p in final[subjectPos+1:]:
						print final, subjectPos, p
						flag = True
						subjectPos = final.index(p)
						

				if flag:
					continue
				else:
					final.append(pronounsDict[line[2][4:6]])
					print final
			
			else:
				final.append(line[1])
		i = len(final)
	#Add verb and question mark (if any)
	final.append(verb)

	if question != '':
		final.append(question)
	
	print final
	return final

'''
s = zerorpc.Server(Lemmatizer())
s.bind("tcp://0.0.0.0:4242")
print "Corriendo"
s.run()

'''
strTest = "dijo que no cantaba muy bien"

'''
string = pes.parse(strTest, relations=True, lemmata=True)

a = Lemmatizer()
print a.lemma(strTest)

pes.pprint(string)
'''
meh = open("meh", "w")
meh.write(strTest)
meh.close()

stream = os.popen("analyze -f es.cfg  < meh")

#stream2 = os.popen("analyze -f es.cfg --output conll < meh")

words = freelingParser(stream)
final = []
for word in words:
	if os.path.exists(os.getcwd() + '/vids/' + word + '.mp4'):
		final.append(word)
	else:	
		final.extend(word)
print final


