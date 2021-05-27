from pyannote.core import Segment, notebook
from pyannote.metrics.diarization import DiarizationErrorRate, JaccardErrorRate
from pyannote.database.util import load_rttm

import numpy as np
import pandas as pd

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

def stat(test, uns, normalize_name_func=lambda x:x):
    stat = pd.DataFrame(columns=["file", "DER", "JER", "FA", "Missed", "counted person", "person"])
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
                            "person":real}, ignore_index=True)
    stat = stat.append({"file":"--ALL--", "DER":stat["DER"].mean()}, ignore_index=True)
    return stat


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