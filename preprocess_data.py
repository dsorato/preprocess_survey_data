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
		

	intersection = compute_intersection(df_dict)
	for k,v in list(df_dict.items()):
		df = pd.DataFrame(columns=['survey_item_ID','Study','module','item_type','item_name','item_value', k])

		r1 = v[v['Study'].str.contains("ESS_R01")]
		print(r1)
		intersection_r1 = intersection[intersection['Study'].str.contains("ESS_R01")]
		print(intersection_r1)
		intersection_r1_item_names = intersection_r1.item_name.unique()
		print(intersection_r1_item_names)
		r1 = r1[r1['item_name'].isin(intersection_r1_item_names)]
		print(r1)

		df =  df.append(r1,ignore_index=True)

		r2 = v[v['Study'].str.contains("ESS_R02")]
		intersection_r2 = intersection[intersection['Study'].str.contains("ESS_R02")]
		intersection_r2_item_names = intersection_r2.item_name.unique()
		r2 = r2[r2['item_name'].isin(intersection_r2_item_names)]
		df =  df.append(r2,ignore_index=True)

		r3 = v[v['Study'].str.contains("ESS_R03")]
		intersection_r3 = intersection[intersection['Study'].str.contains("ESS_R03")]
		intersection_r3_item_names = intersection_r3.item_name.unique()
		r3 = r3[r3['item_name'].isin(intersection_r3_item_names)]
		df =  df.append(r3,ignore_index=True)

		r4 = v[v['Study'].str.contains("ESS_R04")]
		intersection_r4 = intersection[intersection['Study'].str.contains("ESS_R04")]
		intersection_r4_item_names = intersection_r4.item_name.unique()
		r4 = r4[r4['item_name'].isin(intersection_r4_item_names)]
		df =  df.append(r4,ignore_index=True)

		r5 = v[v['Study'].str.contains("ESS_R05")]
		intersection_r5 = intersection[intersection['Study'].str.contains("ESS_R05")]
		intersection_r5_item_names = intersection_r5.item_name.unique()
		r5 = r5[r5['item_name'].isin(intersection_r5_item_names)]
		df =  df.append(r5,ignore_index=True)

		r6 = v[v['Study'].str.contains("ESS_R06")]
		intersection_r6 = intersection[intersection['Study'].str.contains("ESS_R06")]
		intersection_r6_item_names = intersection_r6.item_name.unique()
		r6 = r6[r6['item_name'].isin(intersection_r6_item_names)]
		df =  df.append(r6,ignore_index=True)

		evs = v[v['Study'].str.contains("EVS_")]
		intersection_evs = intersection[intersection['Study'].str.contains("EVS_")]
		intersection_evs_item_names = intersection_evs.item_name.unique()
		evs = evs[evs['item_name'].isin(intersection_evs_item_names)]
		df =  df.append(evs,ignore_index=True)

		df.to_csv(k+".tsv", sep='\t', index=False)


	return df_dict

def compute_intersection(dictionary):
	reference = dictionary['ENG_GB']
	i = 0
	for k,v in list(dictionary.items()):
		if k !='ENG_GB':
			if i==0:
				merged = pd.merge(reference, v, how="inner", on=["Study", "item_name"])
			else:
				merged = pd.merge(merged, v, how="inner", on=["Study", "item_name"])

			i = i+1

	return merged

	


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
				if 'GB' in file:
					eng_gb_files.append(file)
				elif 'IE' in file:
					eng_ie_files.append(file)
				else:
					eng_source_files.append(file)

	df_dict = concatenate_by_country([spanish_files,norwegian_files,ger_at_files,ger_ch_files,ger_de_files, fre_be_files,
		fre_ch_files, fre_fr_files, eng_ie_files, eng_gb_files, eng_source_files])
	# df_dict = concatenate_by_country([spanish_files,norwegian_files,eng_gb_files])


if __name__ == "__main__":
	folder_path = str(sys.argv[1])
	main(folder_path)
