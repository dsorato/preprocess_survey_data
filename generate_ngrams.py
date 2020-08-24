import nltk
import re
import pandas as pd
from nltk.util import ngrams
from nltk.probability import FreqDist
import os
import sys

def print_common_tag_ngrams(n, dataset):
	#Create dataframe with column names equal to predefined table in assignment 2 PDF file
	df_statistics = pd.DataFrame(columns=[str(n)+'-grams', 'Frequency', 'Accum.freq.'])
	
	
	#initialize FreqDist object. 
	fdist = FreqDist()
	#a variable to keep the total number of ngrams
	number_of_ngrams = 0
	#for each tagged sentence in the corpus
	all_grams = []
	for sentence in dataset:
		print(sentence)
		grams = list(ngrams(sentence, 1))
		all_grams.append(grams)
		number_of_ngrams = number_of_ngrams+len(grams)
		for gram in grams:
			fdist[gram] += 1
	
	print(all_grams)
	most_frequent = fdist.most_common()

	#a variable to keep the accum. freq.
	accum = 0
	for k,v in list(most_frequent):
		accum = accum + v/number_of_ngrams
		#data segment to be included in the dataframe
		data = {str(n)+'-grams': k, 'Frequency': '{:.2%}'.format(v/number_of_ngrams),
		'Accum.freq.': '{:.2%}'.format(accum)}
		#include the data segment in the dataframe (as row)
		df_statistics = df_statistics.append(data, ignore_index = True)
		df_statistics.to_csv("unigrams.tsv", sep='\t',encoding='utf-8-sig', index=False)
	

	return df_statistics



def main(folder_path):
	os.chdir(folder_path)
	files = os.listdir(folder_path)
	df = pd.DataFrame(columns=['survey_item_ID','Study','module','item_type','item_name','item_value', 'NOR_NO'])

	tokenizer = nltk.data.load('tokenizers/punkt/norwegian.pickle')

	for index, file in enumerate(files):
		if file.endswith(".tsv"):
			questionnaire = pd.read_csv(file, sep='\t')
			df =  df.append(questionnaire,ignore_index=True)


	dataset = []
	for i, row in df.iterrows():
		if isinstance(row['NOR_NO'], str) and row['NOR_NO'].isdigit() == False:
			text = row['NOR_NO'].replace("(", "")
			text = text.replace(")", "")
			text = text.split(' ')
			print(text)
			if '' in text:
				text = text.remove('')
			if text is not None:
				dataset.append(text)

	print(dataset)


	print_common_tag_ngrams(1, dataset)



if __name__ == "__main__":
	folder_path = str(sys.argv[1])
	main(folder_path)
