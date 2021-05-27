import os
import sys
import torch
from time import perf_counter

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise BaseException("Karamba")
    dia_pipline = torch.hub.load('pyannote/pyannote-audio', 'dia_ami')
    file_info = {
        "uri":".".join(sys.argv[1].split("/")[-1].split(".")[:-1]),
        "audio":sys.argv[1]
    }
    print("start diarization via pyannote.audio")
    start = perf_counter()
    result = dia_pipline(file_info)
    output_filename = os.path.join(os.getcwd(), "out", ".".join((file_info["uri"], "rttm")))
    with open(output_filename, "w") as f:
        result.write_rttm(f)
    duration = perf_counter() - start
    print("diarization via pyannote audio ended with time " + str(duration))






#@inproceedings{Bredin2020,
#  Title = {{pyannote.audio: neural building blocks for speaker diarization}},
#  Author = {{Bredin}, Herv{\'e} and {Yin}, Ruiqing and {Coria}, Juan Manuel and {Gelly}, Gregory and {Korshunov}, Pavel and {Lavechin}, Marvin and {Fustes}, Diego and {Titeux}, Hadrien and {Bouaziz}, Wassim and {Gill}, Marie-Philippe},
#  Booktitle = {ICASSP 2020, IEEE International Conference on Acoustics, Speech, and Signal Processing},
#  Address = {Barcelona, Spain},
#  Month = {May},
#  Year = {2020},
#}


