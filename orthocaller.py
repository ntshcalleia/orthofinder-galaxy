import subprocess
import argparse
from pathlib import Path
import shutil

#Defining Data directory name
dataDirectory = 'MyData'

#Mkdir if it does not exists
Path(dataDirectory).mkdir(exist_ok=True)

#For parsing given args
parser = argparse.ArgumentParser()
parser.add_argument('files', type=argparse.FileType('r'), nargs='+')

args = parser.parse_args()

#Copying args files to Data directory
for f in args.files:
	shutil.copy(f.name, dataDirectory)

#Running orthocaller on Data directory (chamar caminho completo)
orthocaller = subprocess.Popen(['./orthofinder','-f',dataDirectory],
stdout=subprocess.PIPE, stderr=subprocess.PIPE,
universal_newlines=True)

#copiar arquivos desejados pro path de saida TODO
for line in orthocaller.stdout.readlines():
	print(line)
	
#cmd test (Apagar dps)	
#python3 orthocaller.py ~/Programs/OrthocallerTest/Mycoplasma_agalactiae.faa ~/Programs/OrthocallerTest/Mycoplasma_gallisepticum.faa ~/Programs/OrthocallerTest/Mycoplasma_genitalium.faa ~/Programs/OrthocallerTest/Mycoplasma_hyopneumoniae.faa


