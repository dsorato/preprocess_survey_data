"""
Python3 script for preprocessing MCSQ data for the first case study.
Before running the script, install requirements: pandas and gensim
Author: Danielly Sorato 
Author contact: danielly.sorato@gmail.com
""" 
import string
import os
import sys
import pandas as pd
import gensim
import re

def text_cleaning(text):
	if isinstance(text, str):
		text = text.lower()
		text = text.translate(str.maketrans('', '', string.punctuation))
		text = gensim.utils.simple_preprocess(text, deacc=True)
		text = ' '.join(text)
	else:
		text = ''
	

	return text


def clean_dataframe(df):
	column_names = df.columns
	text = column_names[-1]
	cleaned_df = pd.DataFrame(columns=['survey_item_ID','Study','module','item_type','item_name','item_value', text])
	for i, row in df.iterrows():
		clean_text = text_cleaning(row[text])
		if isinstance(clean_text, str) and clean_text != '':
			data = {'survey_item_ID': row['survey_item_ID'],'Study': row['Study'],'module': row['module'],
			'item_type': row['item_type'],'item_name': row['item_name'],'item_value': row['item_value'], text:clean_text}
			cleaned_df = cleaned_df.append(data, ignore_index=True)

	return cleaned_df

def concatenate_by_country(file_lists):
	for file_list in file_lists:
		df = pd.DataFrame(columns=['survey_item_ID','Study','module','item_type','item_name','item_value', file_list[0]])
		for file in file_list[1:]:
			print(file_list[1:])
			questionnaire = pd.read_csv(file)
			df =  df.append(questionnaire,ignore_index=True)
		cleaned_df = clean_dataframe(df)
		cleaned_df.to_csv(folder_path+'/'+file_list[0]+".tsv", sep='\t', index=False)



def main(folder_path):
	os.chdir(folder_path)
	files = os.listdir(folder_path)
	spanish_files = ['SPA_ES']
	norwegian_files = ['NOR_NO']
	ger_at_files = ['GER_AT']
	ger_ch_files = ['GER_CH']
	ger_de_files = ['GER_DE']
	fre_be_files = ['FRE_BE']
	fre_ch_files = ['FRE_CH']
	fre_fr_files = ['FRE_FR']
	eng_ie_files = ['ENG_IE']
	eng_gb_files = ['ENG_GB']
	eng_source_files = ['ENG_SOURCE']

	for index, file in enumerate(files):
		if file.endswith(".csv"):
			if 'SPA' in file:
				spanish_files.append(file)
			elif 'NOR' in file:
				norwegian_files.append(file)
			elif 'GER' in file:
				if 'AT' in file:
					ger_at_files.append(file)
				elif 'CH' in file:
					ger_ch_files.append(file)
				else:
					ger_de_files.append(file)
			elif 'FRE' in file:
				if 'BE' in file:
					fre_be_files.append(file)
				elif 'CH' in file:
					fre_ch_files.append(file)
				else:
					fre_fr_files.append(file)
			elif 'ENG' in file:
				if 'IE' in file:
					eng_ie_files.append(file)
				elif 'GB' in file:
					eng_gb_files.append(file)
				else:
					eng_source_files.append(file)

	concatenate_by_country([spanish_files,norwegian_files,ger_at_files,ger_ch_files,ger_de_files, fre_be_files,
		fre_ch_files, fre_fr_files, eng_ie_files, eng_gb_files, eng_source_files])


if __name__ == "__main__":
	folder_path = str(sys.argv[1])
	main(folder_path)
