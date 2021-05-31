from pyannote.core import Segment, notebook
from pyannote.metrics.diarization import DiarizationErrorRate, JaccardErrorRate
from pyannote.database.util import load_rttm

import numpy as np
import pandas as pd
import librosa

import os
import re


der_metric = DiarizationErrorRate()
jer_metric = JaccardErrorRate()


def delete_noise_name(name):
    return re.sub("_noise_lvl[0-9]+", "", name)

def delete_duration_name(name):
    return re.sub("_duration_x[.0-9]+", "", name)
#delete_duration_name("ES2004a.Mix-Headset_duration_x2")

def get_mult(name):
    return float(re.findall("[0-9]+[.0-9]*", name)[-1])
#get_mult("ES2004a.Mix-Headset_duration_x2.0")

def shrink(annote, coef):
    from pyannote.core.annotation import Annotation
    tmp = annote.for_json()
    for i in range(len(tmp["content"])):
        tmp["content"][i]["segment"]["start"] /= coef
        tmp["content"][i]["segment"]["end"] /= coef
    res = Annotation()
    res = res.from_json(tmp)
    return res

def stat(test, uns, dur_path, normalize_name_func=lambda x:x):
    dur = get_duration_list(dur_path)
    stat = pd.DataFrame(columns=["file", "DER", "JER", "FA", "Missed", "counted person", "person", "process_duration", "audio_duration"])
    for key, val in test.items():
        real = len(pd.DataFrame(uns[normalize_name_func(key)].for_json()["content"])["label"].unique())
        finded = len(pd.DataFrame(val.for_json()["content"])["label"].unique())
        der = der_metric(uns[normalize_name_func(key)], val, detailed=True)
        jer = jer_metric(uns[normalize_name_func(key)], val)
        stat = stat.append({"file":key, 
                            "DER":der["diarization error rate"], 
                            "JER":jer,
                            "FA":der["false alarm"],
                            "Missed":der["missed detection"],
                            "counted person":finded, 
                            "person":real,
                            "process_duration":sec_to_min(dur[key][0]),
                            "audio_duration":sec_to_min(dur[key][-1]),
                            "cost of process":dur[key][0]/dur[key][-1]
                           }, ignore_index=True)
    stat = stat.append({"file":"--ALL--",
                        "DER":stat["DER"].mean(), 
                        "JER":stat["JER"].mean(), 
                        "FA":stat["FA"].mean(), 
                        "Missed":stat["Missed"].mean(), 
                        "cost of process":stat["cost of process"].mean()}, ignore_index=True)
    return stat
 
sec_to_min = lambda x: x/60
    
def get_duration_list(path):
    res = dict()
    with open(path) as f:
        for line in f:
            key, val = line.split("\t")
            res[key] = [float(re.sub("\n", "", val)), ]
            try:
                res[key].append(list_dur[key])
            except KeyError as e:
                print(e)
    return res

def tmp():
    res = dict()
    for i  in os.listdir("./Audio"):
        wav, sr = librosa.load(f"./Audio/{i}")
        res[re.sub(".wav", "", i)] = len(wav)/sr
    return res

list_dur = tmp()



if __name__ == "__main__":
    import sys
    print(get_duration_list(sys.argv[-1]))


def get_rttms(out_path):
    res = dict()
    for rttm in os.listdir(out_path):
        res.update(load_rttm(os.path.join(out_path, rttm)))
    with_noise = dict()
    raw = dict()
    with_duration = dict()
    for key, val in res.items():
        if "noise" in key:
            with_noise[key] = val
        elif "duration" in key:
            with_duration[key] = val
        else:
            raw[key] = val
            
    return with_noise, raw, with_duration

test = load_rttm("rttm/MixHeadset.test.rttm")