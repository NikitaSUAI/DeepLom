from os import get_terminal_size
import librosa
import numpy as np 
import math
import sys
import soundfile as sf

def create_name(in_path, lvl):
    ext = in_path.split(".")[-1]
    name_w_o_ext = ".".join(in_path.split(".")[:-1])
    name_w_o_ext += f"_noise_lvl{lvl}." + ext
    return name_w_o_ext
def get_white_noise(signal,SNR):
    #RMS value of signal
    RMS_s=math.sqrt(np.mean(signal**2))
    #RMS values of noise
    RMS_n=math.sqrt(RMS_s**2/(pow(10,SNR/10)))
    #Additive white gausian noise. Thereore mean=0
    #Because sample length is large (typically > 40000)
    #we can use the population formula for standard daviation.
    #because mean=0 STD=RMS
    STD_n=RMS_n
    noise=np.random.normal(0, STD_n, signal.shape[0])
    return noise


if __name__ == "__main__":
    file_name = None
    noise_lvl = 20  
    if len(sys.argv) == 2:
        file_name = sys.argv[1]
    elif len(sys.argv) == 3:
        file_name = sys.argv[1]
        noise_lvl = int(sys.argv[2])
    else:
        raise BaseException("Karamba")
    wav, sr = librosa.load(file_name)
    wav += get_white_noise(wav, SNR=noise_lvl)
    sf.write(create_name(file_name, noise_lvl), wav, sr)
    print("Noise added!")