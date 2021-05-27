import os 
import urllib.request
from typing import List
import re

def load_dataset(source_patern:str, download_patern:str, list_of_names):
        for name in list_of_names:
            name = re.sub("\n", "", name)
            source = source_patern.format(name)
            download = download_patern.format(name)
            urllib.request.urlretrieve(source, download)
        return True
source_patern = "http://groups.inf.ed.ac.uk/ami/AMICorpusMirror/amicorpus/{0}/audio/{0}.Mix-Headset.wav"
download_patern_train = os.path.join(os.getcwd(), "tmp/{0}.Mix-Headset.wav")

with open("train.lst") as f:
        load_dataset(source_patern, download_patern_train, f)
