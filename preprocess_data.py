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
		text = re.sub("[^\w\d'\d\-\d\(a)/a\s]+",'',text)
		# text = text.translate(str.maketrans('', '', string.punctuation))
		# text = gensim.utils.simple_preprocess(text, deacc=True)
		# text = ' '.join(text)
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
	df_dict = dict()
	for file_list in file_lists:
		df = pd.DataFrame(columns=['survey_item_ID','Study','module','item_type','item_name','item_value', file_list[0]])
		for file in file_list[1:]:
			print(file)
			questionnaire = pd.read_csv(file)
			df =  df.append(questionnaire,ignore_index=True)
		cleaned_df = clean_dataframe(df)
		df_dict[file_list[0]] = cleaned_df
		


	return df_dict

def intersection(lst1, lst2): 
    return list(set(lst1) & set(lst2)) 

def compute_intersection(dictionary):
	reference = dictionary['ENG_GB']
	reference = reference["item_name"]
	i = 0
	for k,v in list(dictionary.items()):
		if k !='ENG_GB':
			temp_v = v["item_name"]
			if i==0:
				inter = intersection(list(dict.fromkeys(reference)), list(dict.fromkeys(temp_v)))
				print(k, inter)
			else:
				inter = intersection(list(dict.fromkeys(inter)), list(dict.fromkeys(temp_v)))
				print(k, inter)

			i = i+1

	return inter

def filter_data(df_dict):
	intersection = compute_intersection(df_dict)
	print(intersection)
	for k,v in list(df_dict.items()):
		df = pd.DataFrame(columns=['survey_item_ID','Study','module','item_type','item_name','item_value', k])

		r1 = v[v['item_name'].isin(intersection)]
		print(r1)

		df =  df.append(r1,ignore_index=True)


		df.to_csv(k+"_r06.tsv", sep='\t', index=False)
		del df



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
				if 'CH' in file:
					ger_ch_files.append(file)
				elif 'AT' in file:
					ger_at_files.append(file)
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
				if 'GB' in file:
					eng_gb_files.append(file)
				elif 'IE' in file:
					eng_ie_files.append(file)
				else:
					eng_source_files.append(file)

	df_dict = concatenate_by_country([spanish_files,norwegian_files,ger_at_files,ger_ch_files,ger_de_files, fre_be_files,
		fre_ch_files, fre_fr_files, eng_ie_files, eng_gb_files, eng_source_files])
	filter_data(df_dict)
	# df_dict = concatenate_by_country([spanish_files,norwegian_files,eng_gb_files])


if __name__ == "__main__":
	folder_path = str(sys.argv[1])
	main(folder_path)
