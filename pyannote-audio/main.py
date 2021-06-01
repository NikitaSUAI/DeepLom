import os
import re
import sys
import time
from ipcqueue import posixmq

import torch



def alon():
    if len(sys.argv) != 2:
        raise BaseException("Karamba")
    dia_pipline = torch.hub.load('pyannote/pyannote-audio', 'dia_ami')
    file_info = {
        "uri":".".join(sys.argv[1].split("/")[-1].split(".")[:-1]),
        "audio":sys.argv[1]
    }
    print("start diarization via pyannote.audio")
    start = time.time()
    result = dia_pipline(file_info)
    output_filename = os.path.join(os.getcwd(), "out", ".".join((file_info["uri"], "rttm")))
    with open(output_filename, "w") as f:
        result.write_rttm(f)
    duration = time.time() - start
    with open("out/out.dur", "a") as f:
        f.write(f"{file_info}\t{duration}")
    print("diarization via pyannote audio ended with time " + str(duration))

def on_service():
    q_name = "/pyanno"
    if len(sys.argv) >= 3 and sys.argv[2] != "&":
        q_name = sys.argv[2]
    dia_pipline = torch.hub.load('pyannote/pyannote-audio', 'dia_ami')

    front_q = posixmq.Queue(q_name)
    bask_q = posixmq.Queue(f"{q_name}_return")
    while True:
        msg = front_q.get()
        if msg == "break":
            break
        print("Processing")
        file_info = {
            "uri": ".".join(msg.split("/")[-1].split(".")[:-1]),
            "audio": msg
        }
        out = re.sub(".wav", ".rttm", msg)
        result = dia_pipline(file_info)
        with open(out, "w") as f:
            result.write_rttm(f)
        bask_q.put(out)



if __name__ == "__main__":
    if sys.argv[1] == "service":
        on_service()
    else:
        alon()







#@inproceedings{Bredin2020,
#  Title = {{pyannote.audio: neural building blocks for speaker diarization}},
#  Author = {{Bredin}, Herv{\'e} and {Yin}, Ruiqing and {Coria}, Juan Manuel and {Gelly}, Gregory and {Korshunov}, Pavel and {Lavechin}, Marvin and {Fustes}, Diego and {Titeux}, Hadrien and {Bouaziz}, Wassim and {Gill}, Marie-Philippe},
#  Booktitle = {ICASSP 2020, IEEE International Conference on Acoustics, Speech, and Signal Processing},
#  Address = {Barcelona, Spain},
#  Month = {May},
#  Year = {2020},
#}


