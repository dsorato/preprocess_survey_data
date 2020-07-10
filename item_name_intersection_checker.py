import os
import sys 
import pandas as pd

def main(folder_path):
	dict_item_names =  dict()
	os.chdir(folder_path)
	files = os.listdir(folder_path)
	for index, file in enumerate(files):
		if file.endswith(".tsv"):
			data = pd.read_csv(file, sep='\t', header=0)
			dict_item_names[file] = data.item_name.unique()

	
	reference = dict_item_names['ENG_GB_r06.tsv']
	
	for k,v in list(dict_item_names.items()):
		if k !='ENG_GB_r06.tsv':
			print(list(set(reference) - set(v)))

if __name__ == "__main__":
	folder_path = str(sys.argv[1])
	main(folder_path)
