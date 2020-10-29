import subprocess
import argparse
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory
from datetime import datetime


#Defining which outputs we want and their paths in the OrthoFinder output directory
target_output_paths = [
	Path().joinpath('Orthogroups','Orthogroups.tsv'),
	Path().joinpath('Species_Tree','SpeciesTree_rooted_node_labels.txt'),
	Path().joinpath('Comparative_Genomics_Statistics','OrthologuesStats_many-to-many.tsv'),
	Path().joinpath('Comparative_Genomics_Statistics','Statistics_PerSpecies.tsv'),
	Path().joinpath('Comparative_Genomics_Statistics','Statistics_Overall.tsv')
]

#For parsing given args
parser = argparse.ArgumentParser()
parser.add_argument('out', type=str, nargs=len(target_output_paths))
parser.add_argument('files', type=str, nargs='+')
args = parser.parse_args()

#Defining current date and time in order to name folders accordingly
current_date = datetime.now()
date_month = current_date.strftime('%b')
date_day = current_date.strftime('%d')

#Creating a temporary directory to use with OrthoFinder
with TemporaryDirectory() as dataDirectory:
	#Mapping target output directory from OrthoFinder results with the ones from argv
	out_path_map = {}
	for src,dst in zip(target_output_paths,args.out):
		out_path_map[src]=dst

	#Copying args files to data directory
	for f in args.files:
		shutil.copy(f, dataDirectory)

	#Running orthocaller on data directory (!!!chamar caminho completo ou usar path do sistema!!!)
	orthocaller = subprocess.Popen(['./orthofinder','-f',dataDirectory],
	stdout=subprocess.PIPE, stderr=subprocess.PIPE,
	universal_newlines=True)

	#Waiting for the subprocess to finish
	orthocaller.wait()

	#Copy target files to their respective output paths defined in argv
	for src in target_output_paths:
		shutil.copy(Path().joinpath(dataDirectory, 'OrthoFinder', 'Results_'+date_month+date_day, src),out_path_map[src])
	
#cmd test (Apagar dps)	

#python3 orthocaller.py ~/Desktop/results_orthofinder ~/Desktop/results_orthofinder ~/Desktop/results_orthofinder ~/Desktop/results_orthofinder ~/Desktop/results_orthofinder2 ~/Programs/OrthocallerTest/Mycoplasma_agalactiae.faa ~/Programs/OrthocallerTest/Mycoplasma_gallisepticum.faa ~/Programs/OrthocallerTest/Mycoplasma_genitalium.faa ~/Programs/OrthocallerTest/Mycoplasma_hyopneumoniae.faa
