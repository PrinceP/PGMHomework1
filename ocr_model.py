

'''
#imageid character
character_list = []


#Read a file from ocr.dat
for j in range(0,999):
	prob = 0
	character = ''

	for line in open('ocr.dat'):
		item = line.rstrip()
		item_s = item.split('	')

		if int(item_s[0]) == j:
			if prob < item_s[2]:
				prob = item_s[2]
				character = item_s[1]
	
	character_list.append(character)		

'''
with open('trans.dat','r') as trans:
	 trans_content = trans.read()
trans_lines = trans_content.splitlines()


with open('ocr.dat','r') as ocr:
	 ocr_content = ocr.read()
ocr_lines = ocr_content.splitlines()

import pickle

#pickle.dump(character_list, open('model1.p','wb'))
character_list = pickle.load(open('model1.p','rb'))

import numpy as np

#Sequence of characters consider the ocr and trans
ids=[582,969,582,969]
seq = ['d',	'o',	'i',	'r',	'a',	'h',	't',	'n'	,'s',	'e']
ocr_character = []

for i in range(0,len(ids)):
	ocr_prob = []
	trans_prob = []
	
	if i == 0:
		ocr_character.append(character_list[ids[i]])
	else:
		for line in open('ocr.dat'):
			item = line.rstrip()
			item_s = item.split('	')

			if int(item_s[0]) == ids[i]:
				ocr_prob.append(float(item_s[2]))

		for char in seq:
			for trans_line in trans_lines:
				finalline = trans_line.split()
				if finalline[0] == ocr_character[i-1]:
					if finalline[1] == char :
						trans_prob.append(float(finalline[2]))



		
		maximum = 0
		final_index = 0				
		
		for index in range(0,10):
			if (maximum < ocr_prob[index]*trans_prob[index]):
				maximum = ocr_prob[index]*trans_prob[index]
				final_index = index

		ocr_character.append(seq[final_index])		


print ocr_character

with open('data.dat','r') as data:
	 data_content = data.read()
data_lines = data_content.splitlines()

def calculatemodel(ids):
	
	new_ocr = ['']*len(ids)
	for i in range(len(ids) - 1, -1 , -1):
		ocr_prob = []
		trans_prob = []
		if i == len(ids) - 1:
			new_ocr[i] = character_list[int(ids[i])]
		else:
			for line in open('ocr.dat'):
				item = line.rstrip()
				item_s = item.split('	')

				if int(item_s[0]) == ids[i]:
					ocr_prob.append(float(item_s[2]))
		
			for char in seq:
				for trans_line in trans_lines:
					finalline = trans_line.split()
					if finalline[1] == new_ocr[i+1]:

						if finalline[0] == char :

							trans_prob.append(float(finalline[2]))

			maximum = 0
			final_index = 0				
		
			for index in range(0,10):
				if (maximum < ocr_prob[index]*trans_prob[index]):
					maximum = ocr_prob[index]*trans_prob[index]
					final_index = index

				new_ocr[i] = seq[final_index]		
						
	return new_ocr


print calculatemodel(ids)




#Exhaustive inference 1st model 		


import itertools

def modelone(ids):
	final_listprob = []	
	for x in ids:
		list_prob = []
		for char in seq:
			for ocr_line in ocr_lines:
				ocr_linesplit = ocr_line.split()

				if int(ocr_linesplit[0])==x:
					if ocr_linesplit[1] == char:
						list_prob.append(float(ocr_linesplit[2]))
		final_listprob.append(list_prob)


	l1 = list(itertools.product(*final_listprob))
	#print len(l1)



	maxmodelscore = 0
	final = ()
	for x in l1:
		modelscore = 1
		for y in x:
			modelscore *= float(y)
		
		if modelscore >= maxmodelscore:
			maxmodelscore = modelscore
			final = x

	print final
	predict = []
	for i in range(0,len(final_listprob) ):

		predict.append(seq[  final_listprob[i].index(final[i])  ])

	print predict	
	print maxmodelscore

modelone(ids)
	
def modeltwo(ids):
	l = len(ids)
	final_listprob = []
	for i in range(0,l):
		final_listprob.append(seq)
	l1 = list(itertools.product(*final_listprob))
	#print l1
	
	maxmodelscore = 0
	final = ()
	
	for x in l1:
		modelscore = 1
		
		for i in range(0,len(x)):
			if i == 0:
				for ocr_line in ocr_lines:
					ocr_linesplit = ocr_line.split()
					if int(ocr_linesplit[0]) == ids[i]:
						if ocr_linesplit[1] == x[i]:
							modelscore *= float(ocr_linesplit[2])
							
			else:
				for ocr_line in ocr_lines:
					ocr_linesplit = ocr_line.split()
					if int(ocr_linesplit[0]) == ids[i]:
						if ocr_linesplit[1] == x[i]:
							modelscore *= float(ocr_linesplit[2])
							
				for trans_line in trans_lines:
					trans_linesplit = trans_line.split()
					if trans_linesplit[0] == x[i-1]:
						if trans_linesplit[1] == x[i]:
							modelscore *= float(trans_linesplit[2])

		
		if modelscore >= maxmodelscore:
			maxmodelscore = modelscore
			final = x
	
	print maxmodelscore
	print final		

			

#modeltwo(ids)


def modelthree(ids):
	l = len(ids)
	final_listprob = []
	for i in range(0,l):
		final_listprob.append(seq)
	l1 = list(itertools.product(*final_listprob))

	maxmodelscore = 0
	final = ()
	
	for x in l1:
		modelscore = 1
		for i in range(0,len(x)):
			if i == 0:
				for ocr_line in ocr_lines:
					ocr_linesplit = ocr_line.split()
					if int(ocr_linesplit[0]) == ids[i]:
						if ocr_linesplit[1] == x[i]:
							modelscore *= float(ocr_linesplit[2])
			else:
				for ocr_line in ocr_lines:
					ocr_linesplit = ocr_line.split()
					if int(ocr_linesplit[0]) == ids[i]:
						if ocr_linesplit[1] == x[i]:
							modelscore *= float(ocr_linesplit[2])
				for trans_line in trans_lines:
					trans_linesplit = trans_line.split()
					if trans_linesplit[0] == x[i-1]:
						if trans_linesplit[1] == x[i]:
							modelscore *= float(trans_linesplit[2])

		#Skip factor
		for i in range(0,len(ids)):
			for j in range(i,len(ids)):
				if ids[i]==ids[j]:
					if x[i] == x[j] :
						modelscore *= float(5)

		if modelscore >= maxmodelscore:
			maxmodelscore = modelscore
			final = x

	print maxmodelscore
	print final	



modelthree(ids)


					



		
		




						





		

































	





			


#Read from a file data.dat
for line in open('data.dat','r'):
	item = line.rstrip()
	image_ids = item.split('	')
	