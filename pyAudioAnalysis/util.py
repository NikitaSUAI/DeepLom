import numpy as np
from pyannote.core.annotation import Annotation

def to_json(speaker_map:np.array, file_name):
    rttm = {'pyannote': 'Annotation', "content":list(), 'uri':file_name}
    label = -1
    track = 0
    segment = dict()
    for i in range(len(speaker_map)):
        speach = speaker_map[i]
        type(i)
        if label != speach:
            if label == -1:
                label = speach
                segment["start"] = i/5
                continue
            else:
                segment["end"] = (i)/5
                rttm["content"].append({"segment":segment, "label":label, "track":track})
                track += 1
                segment = {"start":i / 5}
                label = speach
    return rttm

def to_rttm(speaker_map:np.array, file_name):
    '''return Annotation!!!'''
    res = Annotation()
    return res.from_json(to_json(speaker_map, file_name))