import librosa
import re 
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
    import os
    import re
    res = dict()
    for i  in os.listdir("./Audio"):
        wav, sr = librosa.load(f"./Audio/{i}")
        res[re.sub(".wav", "", i)] = len(wav)/sr
    return res

list_dur = tmp()



if __name__ == "__main__":
    import sys
    print(get_duration_list(sys.argv[-1]))
