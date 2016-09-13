# -*- coding: utf-8 -*-
import zerorpc
import pattern.es as pes
from unidecode import unidecode
import os

'''
Notas:
Link Freeling analyzer tags: https://talp-upc.gitbooks.io/freeling-user-manual/content/tagsets/tagset-es.html

- Resolver qué hacer con palabras que se escriben igual pero tienen distinto significado. 
- Marcar palabras que representan a hombre y mujer (esposo-esposa, tío-tía, él-ella, etc) 
	=> hay que listar todas las posibilidades. 
- Pasar oraciones en voz pasiva a voz activa para hacer más claro el enunciado (el dado fue dado por mí => yo di el dado)
- Crear las marcas de pasado, presente y futuro. Esto corresponde a identificar el tiempo verbal del verbo principal de la oración. Hay frases
que tienen el mismo valor de pasado e.g. ha corrido = corrió, pero a su vez, no es lo mismo corrió que corría, ambos tienen distinta marca en seña:
corrió = correr + pasado + marca de finalización (pasado simple). 
corría = correr + pasado + marca de incertidumbre (imperfecto).
	* ¿Qué ocurre con el subjuntivo? ¿Tiene alguna marca especial?
	=> Las marcas ya están, pero falta precisar más información sobre los tiempos y qué hacer cuando hay más de un tiempo verbal en la frase.
- Invertir el orden cuando se trata de posesión (uso de 'de'). A considerar:
	* Si 'de' está entre un sustantivo o adjetivo y un sustantivo o posesivo, se hace la inversión.
		- La casa grande de mi abuelo => mi-abuelo de casa-grande.
		=> Ya está implementado sin adjetivos. 
	* Cualquier otro uso de 'de' debe ser investigado: Origen (viene de, despertó de), Material (cuchara de palo, plato de cerámica), Locuciones (de corazón, de verdad, de alegría),
	Magnitud (velocidad de, vientos de), Aposición (cuidad de España, pueblo de Sevilla), Diferencia (distinto de, diferente de), Contenido (vaso de agua, botella de vino), Edad, Empleo,
	Abundancia, Partitivo.
- Resolver como marcar los verbos de Concordancia (aquellos que tienen dos sujetos involucrados, e.g. decir
	=> Actualmente se deja el pronombre en frente del verbo.
- Resolver como marcar los verbos espacio-locativos (aquellos que están ligados al objeto, e.g. mover
- Frases interrogativas: la palabra que marca la pregunta (cómo, por qué, cuál, etc) va al final. 
	=> Listo, falta agregar más palabras interrogativas
- Los números pueden ir en distintas partes del enunciado, generalmente al final si están ligados al verbo (querer X cosas => cosas querer X).
- En frases subordinadas, se puede simplemente eliminar el 'que' y dividir en partes la oración, dejando el verbo después del 'que' al final:
	* El dijo que ella no canta muy bien => el decir ella no bien cantar. 
		=> Listo.
- La negación se agrega después del verbo. Si esto no es así en la realidad, solo hay que agregarlo antes :D
- 
'''
#

class Lemmatizer(object):
	def lemma(self, text):
		print "Lematizacion de", text
		
		#Create file
		meh = open("meh", "w")
		meh.write(text)
		meh.close()

		#Run script
		stream = os.popen("analyze -f es.cfg  < meh")

		#Get restructured speech
		words = freelingParser(stream)

		final = []
		for word in words:			
			if os.path.exists(os.getcwd() + '/vids/' + word + '.mp4'):
				final.append(word)
			else:
				final.extend(word)
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
	flagArt = False
	flagDe = False 
	flagSubject = False
	flagNegative = False
	verb = ''
	question = ''
	pronoun = ''
	pronoun2 = ''

	subjectPos = 0
	questionMarks = ['qué', 'cómo']
	femenineWords = ['ella', 'esposa', 'tía', 'prima', 'hermana', 'cuñada', 'nuera', 'niña']
	possessivs = ['mi', 'tu', 'su', 'nuestro', 'nuestra', 'vuestro', 'vuestra', 'sus']

	pronouns2 = ['me', 'te', 'se', 'nos', 'os']
	pronouns = ["yo", "tú", "usted", "él","ella", "nosotros", "vosotros", "ustedes", "ellos", "ellas"]
	pronounsDict = { "1S": "yo", "2S": "tú", "3S": "él",
					 "1P": "nosotros", "2P": "ustedes", "3P": "ellos"}

	tenses ={"I":"(imperfecto)", "F":"(futuro)","S":"(pasado)","C":"(condicional)"}

	#Convert stream object to list, so we can iterate freely through it
	phrase = []
	for line in list(frobject):
		if len(line) < 2:
			continue
		phrase.append(line.strip().split(' '))


	for line in phrase:
		'''
		Line structure
		- word: from the speech
		- lemma: lemma of the word (e.g. cantó => cantar, dulces => dulce)
		- tags: depends on the word. Show if a word is a Noun, Verb, Adverb, etc, and characteristics of them. E.g. a Verb has a tense, mood, person, singular or plural, etc.
		- prob: the probability of the lemma to be correct. 
		'''
		print line
		
		if len(line) < 2:
			continue
		elif line[1] in ['el', 'un', 'uno']:
			flagArt = True
			continue

		elif line[1] == 'no':
			flagNegative = True
			continue

		elif line[1] == 'ser':
			if line[2][3] != 'P':
				final.insert(0, tenses[line[2][3]])
				subjectPos += 1
			flagArt = False
			continue

		elif line[1] == 'que':
			flagArt = False
			#If 'que' goes after a verb, we add the stored verb, since it is not the main verb.
			if verb != '':
				final.append(verb)
				verb = ''
				flagSubject = False
				if flagNegative:
					final.append('no')
					flagNegative = False
			
			
		elif line[1] in '¿?.,':
			flagArt = False
			continue

		elif flagArt and line[2][0] == 'V':
			#if an article was removed, and the current word is a identified as a verb, it is really a noun, so we do not add the lemma.
			#e.g. 'el helado', 'el dado'.
			final.append(line[0])
			flagArt = False
		
		elif line[0] in questionMarks:
			flagArt = False
			#store question word to put it at the end
			question = line[0]

		elif line[0] in femenineWords:
			flagArt = False
			#Words like "ella", "esposa" have a masculine lema, but we need to keep it in femenine
			final.append(line[0])

		elif line[2][0] == 'V' and line[2][2] != 'N':
			flagArt = False
			#store verb to put it at the end
			#if there is already a verb, put it in the array since it is not the main verb.
			if verb != '':
				final.append(verb)
				subjectPos+=1
			
			verb = line[1]
			
			#identify pronoun and tense
			#TODO: 2 verbal times
			if line[2][3] != 'P':
				final.insert(0, tenses[line[2][3]])
				subjectPos += 1

			#Look if there is a pronoun in the sentense
			if not flagSubject: 
				flag = False
				for p in pronouns:
					if p in final[subjectPos+1:]:
						#There is a pronoun, so next time we find a verb, we search right next to the pronoun found
						flag = True
						subjectPos = final.index(p)

				if flag:
					continue
				else:
					final.append(pronounsDict[line[2][4:6]])
		
		elif line[1] == 'de':
			flagDe = True
			final.append(line[1])
		
		elif line[1] in pronouns:
			flagSubject = True
			final.append(line[1])
		
		##Check if the pronoun if a reflexive or a indirect complement
		##Known issue: Subjunctive of 1st and 3er person is the same. Freeling guess the verb as 3rd, so there is no way to guess the correct pronoun.
		##ex: me compre => que yo me compre;  que él me compre. Both have differents meanings. 
		elif line[1] in pronouns2:
			sub = line[2][2] + line[2][4]
			if phrase[phrase.index(line)+1][2][4:6] == sub:
				#It is actually a reflexive, we can add a pronoun from it
				flagSubject = True
				pronoun2 = line[0]
				final.append(pronounsDict[sub])
				
			else:
				#It is a indirect complement, we store it to add it later
				pronoun2 = line[1]
		
		else:
			if flagArt:
				flagSubject = True
			flagArt = False
			final.append(line[1])
		
	#Add pronoun2 pronoun, verb and question mark (if any)
	if pronoun2 != '':
		final.append(pronoun2)

	if verb != '':
		final.append(verb)

	if flagNegative:
		final.append('no')

	if question != '':
		final.append(question)

	#De-inversion, only works in possession cases
	if flagDe:
		i = final.index('de')

		if final[i+1] in possessivs:
			auxPos = final[i+1]
			auxNoun = final[i+2]
			print auxPos
			del final[i+1]
			print auxPos
			final[i+1] = final[i-1]
			final[i-1] = auxNoun
			final.insert(i-1, auxPos)
			
		else:
			aux = final[i+1]
			final[i+1] = final[i-1]
			final[i-1] = aux

	
	print final
	return final

'''
s = zerorpc.Server(Lemmatizer())
s.bind("tcp://0.0.0.0:4242")
print "Corriendo"
s.run()

'''
strTest = "él quiso comerme"

a = Lemmatizer()
print a.lemma(strTest)
