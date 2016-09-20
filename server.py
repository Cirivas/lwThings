# -*- coding: utf-8 -*-
import zerorpc
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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
- Problema conocido: Muchas conjugaciones de la primera y tercera persona son la misma. Freeling asigna siempre la conjugación de la 3ra persona.
	* e.g. que compre => que YO compre, que ÉL compre; freeling dirá que "compre" está en 3ra persona.
'''

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
			if os.path.exists(os.getcwd() + '/public/vids/' + word + '.mp4'):
				final.append(unicode(word))
			else:
				final.extend(unicode(word))
		return final

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

	questionMarks = ['qué', 'cómo']
	femenineWords = ['ella', 'esposa', 'tía', 'prima', 'hermana', 'cuñada', 'nuera', 'niña', 'hija']
	possessives = ['mi', 'tu', 'su', 'nuestro', 'nuestra', 'vuestro', 'vuestra', 'sus']

	
	pronouns = ["yo", "tú", "usted", "él","ella", "nosotros", "vosotros", "ustedes", "ellos", "ellas"]
	pronounsDict = { "1S": "yo", "2S": "tú", "3S": "él",
					 "1P": "nosotros", "2P": "ustedes", "3P": "ellos"}

	pronouns2 = {'me':'a-mi', 'te':'a-ti', 'se':'se', 'nos':'a-nosotros', 'os':'a-vosotros', 'lo': 'eso', 'la': 'eso'}

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
		- line[0] word: from the speech
		- line[1] lemma: lemma of the word (e.g. cantó => cantar, dulces => dulce)
		- line[2] tags: depends on the word. Show if a word is a Noun, Verb, Adverb, etc, and characteristics of them. E.g. a Verb has a tense, mood, person, singular or plural, etc.
		- line[3] prob: the probability of the lemma to be correct. 
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
		
			#if there is no pronoun in the sentense, add it from the verb
			if not flagSubject and not (pronounsDict[line[2][4:6]] in final or 'ella' in final):
				final.append(pronounsDict[line[2][4:6]])
			else:				
				flagSubject = False

			flagArt = False		

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
			
			
			verb = line[1]
			
			#identify pronoun and tense
			#TODO: 2 verbal times
			if line[2][3] != 'P':
				final.insert(0, tenses[line[2][3]])

			#if there is no pronoun in the sentense, add it from the verb
			if not flagSubject and not (pronounsDict[line[2][4:6]] in final or 'ella' in final):
				final.append(pronounsDict[line[2][4:6]])
			else:
				flagSubject = False
		
		elif line[1] == 'de':
			flagDe = True
			final.append(line[1])
		
		elif line[1] in pronouns:
			flagSubject = True
			final.append(line[1])
		
		##Check if the pronoun if a reflexive or a indirect complement
		elif line[1] in pronouns2.keys():
			flagArt = False
			sub = line[2][2] + line[2][4]
			index = phrase.index(line)
			if phrase[index-1][2][0] == 'V' and phrase[index-1][2][2] == 'N':
				##'Pronombre enclítico' add it in front of the verb
				final.insert(index-1, pronouns2[line[1]])

				
				
			elif phrase[index-2][2][0] == 'V' and phrase[index-2][2][2] == 'N' and phrase[index-1][0] == 'se':
				##cases: selo, sela, sele, selos, selas, seles	
				final.insert(index-2, pronouns2[line[1]])

			elif phrase[index+1][2][0] == 'V' and phrase[index+1][2][4:6] == sub:
				#It is actually a reflexive, we can add a pronoun from it
				if not flagSubject and not (pronounsDict[sub] in final or 'ella' in final):
					flagSubject = True
					final.append(pronounsDict[sub])
				if pronoun2 != '':
					final.append(pronouns2[pronoun2])
				pronoun2 = line[0]
			
			else:
				#It is a complement, we store it to add it later
				if pronoun2 != '':
					final.append(pronouns2[pronoun2])
				pronoun2 = line[1]
		
		else:
			if flagArt:
				flagSubject = True
			flagArt = False
			final.append(line[1])
		
	#Add pronoun2 pronoun, verb and question mark (if any)
	if pronoun2 != '':
		final.append(pronouns2[pronoun2])

	if verb != '':
		final.append(verb)

	if flagNegative:
		final.append('no')

	if question != '':
		final.append(question)

	#De-inversion, only has sense if it is a possession case.
	#ToDo: look for adjectives
	#Working cases: <noun> de [<possessive>] noun
	if flagDe:
		i = final.index('de')

		if final[i+1] in possessives:
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


s = zerorpc.Server(Lemmatizer())
s.bind("tcp://0.0.0.0:4242")
print "Corriendo"
s.run()

'''
strTest = "No sé si mañana iré a la piscina"

a = Lemmatizer()
print a.lemma(strTest)
'''
