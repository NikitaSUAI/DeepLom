import librosa
import soundfile as sf
import sys

def create_name(in_path, lvl):
    ext = in_path.split(".")[-1]
    name_w_o_ext = ".".join(in_path.split(".")[:-1])
    name_w_o_ext += f"_duration_x{lvl}." + ext
    return name_w_o_ext

if __name__ == "__main__":
    file_name = None
    mul = 2
    if len(sys.argv) >= 2:
        file_name = sys.argv[1]
        if len(sys.argv) == 3:
            mul = float(sys.argv[2])
    else: 
        raise BaseException("Karamba")
    wav, sr = librosa.load(file_name)
    sf.write(create_name(file_name, mul), wav, int(sr*mul))
