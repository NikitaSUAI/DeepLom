import util

from pyAudioAnalysis.audioSegmentation import speaker_diarization
from pyannote.database.util import load_rttm

import pandas as pd
import numpy as np

import os
import sys
import re
import time


def remove_wav(label):
    label = re.search("[a-zA-Z0-9-._]+.wav", label).group(0)
    print(label)
    #label = re.sub("[0-9]+lvl_esion_", "", label[::-1])
    label =  re.sub(".wav", "", label)
    
    print(label)
    return label

def get_truth(label, truth):
    return len(pd.DataFrame(
        load_rttm(truth)[label].for_json()["content"])["label"].unique())
     

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise BaseException("Karamba")
        
    f_name = sys.argv[-2]
    label = remove_wav(f_name)
    truth = get_truth(re.sub("_noise_lvl[0-9]+", "", label), sys.argv[-1])
    start_time = time.time()
    predict = speaker_diarization(f_name, truth, lda_dim= 0)
    duration_time = time.time() - start_time
    with open("out.dur","a") as f:
        f.write(f"{label}\t{duration_time}\n")
    with open(os.path.join("out", f"{label}.rttm"), "w") as f:
        util.to_rttm(predict, label).write_rttm(f)
    
    
