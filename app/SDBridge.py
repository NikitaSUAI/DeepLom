from concurrent.futures.thread import ThreadPoolExecutor
from enum import IntEnum
from threading import Lock
from collections.abc import Callable

from ipcqueue import posixmq


class Algo(IntEnum):
    pyannote_audio = 0
    pyBK = 1
    pyAudioAnalysis = 2

class SDBridge:
    def __init__(self, pyanno_q:str="/pyanno", pyBK_q:str="/pybk",
                 pyAudio_q:str="/pyaud"):
        self.queues = [posixmq.Queue(pyanno_q),
                  posixmq.Queue(f"{pyanno_q}_return"),
                  posixmq.Queue(pyBK_q),
                  posixmq.Queue(f"{pyBK_q}_return"),
                  posixmq.Queue(pyAudio_q),
                  posixmq.Queue(f"{pyAudio_q}_return")]
        self.TPE = ThreadPoolExecutor(max_workers=1)
        # self.Lock = Lock()

    def go(self, file_name:str, algo_type:Algo,
           callback_fn):
        front, back = self.queues[2*algo_type], self.queues[2*algo_type+1]
        self.TPE.submit(self.__process, front, back, file_name, callback_fn)

    def __process(self, front_q:posixmq.Queue, back_q:posixmq.Queue,
                  msg, callback_fn):
        front_q.put(msg)
        result = back_q.get()
        callback_fn(result)


    def close_q(self):
        # опустошаем очередь
        for i in self.queues:
            while i.qsize() > 0:
                i.get()
        # закрываем сервисы
        for i in range(3):
            self.queues[i*2].put("break")
        print("All closed")