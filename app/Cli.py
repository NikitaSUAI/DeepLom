from typing import List

from SDBridge import SDBridge, Algo


class Cli:
    def __init__(self):
        self.bridge = SDBridge()

    def monolog(self, params:List[str]):
        algo = None
        next_param = params[1]
        if params[0] == "pyanno":
            algo = Algo.pyannote_audio
        elif params[0] == "pybk":
            algo = Algo.pyBK
        elif params[0] == "pyaudio":
            algo = Algo.pyAudioAnalysis
            next_param = f"{next_param}|-|{params[2]}"
        else:
            raise BaseException("Karamba")

        self.bridge.go(next_param, algo, self.info)

    def info(self, path:str)->None:
        print(f"file with diarization will save in {path}")
