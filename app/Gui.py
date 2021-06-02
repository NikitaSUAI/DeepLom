from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, \
    QLineEdit, QPushButton, QMainWindow, QWidget, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QUrl

import os
import re

from SDBridge import SDBridge, Algo
from pyannote.database.util import load_rttm

class Gui(QWidget):

    def __init__(self):
        super().__init__()
        self.bridge = SDBridge()
        self.resize(1000, 800)
        base_layout = QVBoxLayout()
        top_layout = QVBoxLayout()
        top_layout.addWidget(QLabel("Итак, нам надо выбрать файл а потом "
                                    "выбрать подходящий алгоритм исходя из "
                                    "априорных знаний о колличестве людей,\n "
                                    "а так же из желаемой скорости "
                                    "выполнения, если у нас нет ни того ни "
                                    "другого выбираем 1 кнопку"))
        path_layout = QHBoxLayout()

        self.path_line = QLineEdit("/root/user/speech.wav")
        self.path_line.resize(500, 10)
        path_layout.addWidget(self.path_line)

        observer_button = QPushButton("обзор")
        observer_button.clicked.connect(self.observer)
        path_layout.addWidget(observer_button)

        path_layout.addWidget(QLabel("Сколько человек говорит? "))
        self.amount_of_speakers = QLineEdit("Неизвестно")
        self.amount_of_speakers.resize(100, 10)
        path_layout.addWidget(self.amount_of_speakers)

        chose_layout = QHBoxLayout()
        pyanno_but = QPushButton("50% от Т\n32% DER")
        pyanno_but.clicked.connect(self.send_processing_pyanno)
        chose_layout.addWidget(pyanno_but)

        pybk_but = QPushButton("5% от Т\n62% DER")
        pybk_but.clicked.connect(self.send_processing_pybk)
        chose_layout.addWidget(pybk_but)

        pyaud_but = QPushButton("10% от Т\n 85% DER")
        pyaud_but.clicked.connect(self.send_processing_pyaud)
        chose_layout.addWidget(pyaud_but)

        self.wav_widget = QWidget()
        self.wav_label = QLabel(self.wav_widget)
        wav_image = QPixmap("images/empty_vawe_form.png")
        self.wav_label.setPixmap(wav_image)
        self.wav_widget.resize(wav_image.width(), wav_image.height())

        self.anno_widget = QWidget()
        self.anno_label = QLabel(self.anno_widget)
        anno_image = QPixmap("images/empty_annotation.png")
        self.anno_label.setPixmap(anno_image)
        self.anno_widget.resize(anno_image.width(), anno_image.height())

        base_layout.addLayout(top_layout)
        base_layout.addLayout(path_layout)
        base_layout.addLayout(chose_layout)
        base_layout.addWidget(self.wav_widget)
        base_layout.addWidget(self.anno_widget)
        self.setLayout(base_layout)

    def observer(self):
        direct = QFileDialog.getOpenFileUrl(self,
                                            "open File",
                                            QUrl(os.getcwd()),
                                            "Wav File (*.wav)")
        direct = re.sub("file://", "", direct[0].toString())
        print(direct)
        self.path_line.setText(direct)


    def draw_wave(self, path_to_file):
        import matplotlib.pyplot as plt
        import librosa
        wav, _ = librosa.load(path_to_file)
        plt.plot(wav)
        plt.savefig("images/tmp.png")
        image = QPixmap("images/tmp.png")
        self.wav_label.setPixmap(image)
        self.wav_widget.resize(image.width(), image.height())

    def send_processing_pyanno(self):
        path_to_file = self.path_line.text()
        self.bridge.go(path_to_file, Algo.pyannote_audio, self.write_msg)
        self.draw_wave(path_to_file)

    def send_processing_pybk(self):
        path_to_file = self.path_line.text()
        self.bridge.go(path_to_file, Algo.pyBK, self.write_msg)
        self.draw_wave(path_to_file)

    def send_processing_pyaud(self):
        path_to_file = self.path_line.text()
        self.bridge.go(path_to_file, Algo.pyAudioAnalysis, self.write_msg)
        self.draw_wave(path_to_file)

    def write_msg(self, msg):
        import matplotlib.pyplot as plt
        from pyannote.core.notebook import Notebook

        label = ".".join(msg.split("/")[-1].split(".")[:-1])
        rttm = load_rttm(msg)
        _, ax = plt.subplots()
        note = Notebook()
        note.plot_annotation(rttm[label], ax=ax)
        plt.savefig("images/tmp.png")
        image = QPixmap("images/tmp.png")
        self.anno_label.setPixmap(image)
        self.anno_widget.resize(image.width(), image.height())
        msg_box = QMessageBox()
        msg_box.setText("Сохранение")
        msg_box.setInformativeText(f"Файл с дневником говорящих записан в "
                                   f"{msg}")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

