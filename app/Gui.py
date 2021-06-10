from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, \
    QLineEdit, QPushButton,  QWidget, QFileDialog, QMessageBox, \
    QLayout, QComboBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QUrl, QRect, Qt


import os
import re

import myutil

from SDBridge import SDBridge, Algo
from pyannote.database.util import load_rttm

class Gui(QWidget):

    def __init__(self):
        super().__init__()
        self.bridge = SDBridge()
        self.resize(1000, 600)
        self.do_pyBK = False
        self.algo = Algo.pyannote_audio
        base_layout = QVBoxLayout()
        # top_layout = QVBoxLayout()
        # top_layout.setSizeConstraint(QLayout.SetFixedSize)
        # top_layout.setContentsMargins(1,1,1,1)
        # wid = QLabel("Добро пожаловать\nДля того что бы запустить процесс "
        #              "разделения говорящих необходимо:\n\t --Выбрать как "
        #              "скоро нужен результат(от этого зависит скорость "
        #              "выполнения, а так же качество)\n\t --Нажать кнопку "
        #              "\"Запустить процесс\"\n\t --Ждать окончания работы "
        #              "процесса")

        msg_box = QMessageBox()
        msg_box.setWindowTitle('О программе')
        msg_box.setText("Добро пожаловать!!!\nДля того что бы запустить "
                        "процесс "
                     "разделения говорящих необходимо:\n\t --Выбрать как "
                     "скоро нужен результат(от этого зависит скорость "
                     "выполнения, а так же качество)\n\t --Нажать кнопку "
                     "\"Запустить процесс\"\n\t --Ждать окончания работы "
                     "процесса")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

        # wid.resize(700, 30)
        # top_layout.addWidget(wid)
        self.path_layout = QHBoxLayout()

        self.path_line = QLineEdit("/root/user/speech.wav")
        self.path_line.resize(500, 10)
        self.path_layout.addWidget(self.path_line)

        observer_button = QPushButton("обзор")
        observer_button.clicked.connect(self.observer)
        self.path_layout.addWidget(observer_button)

        self.q_label = QLabel("Можно ли пренебречь качеством в угоду "
                                     "быстродействию?")
        self.path_layout.addWidget(self.q_label)
        self.is_fast = MySwitch()
        self.is_fast.setChecked(False)
        self.is_fast.clicked.connect(self.change)
        self.path_layout.addWidget(self.is_fast)

        chose_layout = QHBoxLayout()
        pyanno_but = QPushButton("process")
        pyanno_but.clicked.connect(self.send_processing)
        chose_layout.addWidget(pyanno_but)

        self.chose_algo = QComboBox()
        self.chose_algo.addItem("pyannote-audio")
        self.chose_algo.addItem("pyBK")
        self.chose_algo.addItem("pyAudioAnalysis")
        self.chose_algo.currentIndexChanged.connect(self.change_algo)
        chose_layout.addWidget(self.chose_algo)
        #
        # pybk_but = QPushButton("5% от Т\n62% DER")
        # pybk_but.clicked.connect(self.send_processing_pybk)
        # chose_layout.addWidget(pybk_but)
        #
        # pyaud_but = QPushButton("10% от Т\n 85% DER")
        # pyaud_but.clicked.connect(self.send_processing_pyaud)
        # chose_layout.addWidget(pyaud_but)

        # self.wav_widget = QWidget()
        # self.wav_label = QLabel(self.wav_widget)
        # wav_image = QPixmap("images/empty_vawe_form.png")
        # self.wav_label.setPixmap(wav_image)
        # self.wav_widget.resize(wav_image.width(), wav_image.height())

        self.pic_layout = QHBoxLayout()
        self.anno_widget = QWidget()
        self.anno_label = QLabel(self.anno_widget)
        image = QPixmap("images/pyannote-audio/ES2004a.Mix-Headset.png")
        self.anno_label.setPixmap(image)
        self.anno_label.setFixedSize(image.width(), image.height())
        self.pic_layout.addWidget(self.anno_widget)

        tmp_layout = QVBoxLayout()
        tmp_layout.setSpacing(10)
        # tmp_layout.addLayout(top_layout)
        tmp_layout.addLayout(self.path_layout)
        tmp_layout.addLayout(chose_layout)
        base_layout.addLayout(tmp_layout)
        base_layout.addLayout(self.pic_layout)
        self.setLayout(base_layout)

    def change_algo(self, *args):
        if self.algo == Algo.pyAudioAnalysis and \
                self.chose_algo.currentText() in ("pyBK", "pyannote-audio"):
            self.path_layout.removeWidget(self._amount_box)
            self._amount_box.deleteLater()
            self._amount_box = None
            self.q_label = QLabel("Можно ли пренебречь качеством в угоду "
                                  "быстродействию?")
            self.path_layout.addWidget(self.q_label)
            self.is_fast = MySwitch()
            self.is_fast.setChecked(False)
            self.is_fast.clicked.connect(self.change)
            self.path_layout.addWidget(self.is_fast)
        if self.chose_algo.currentText() == "pyBK":
            self.is_fast.setChecked(True)
            self.do_pyBK = True
            self.algo = Algo.pyBK
        elif self.chose_algo.currentText() == "pyannote-audio":
            self.is_fast.setChecked(False)
            self.do_pyBK = False
            self.algo = Algo.pyannote_audio
        else:
            self.path_layout.removeWidget(self.is_fast)
            self.is_fast.deleteLater()
            self.is_fast = None
            self.path_layout.removeWidget(self.q_label)
            self.q_label.deleteLater()
            self.q_label = None
            self._amount_box = QLineEdit("Введите колличество говорящих")
            self.path_layout.addWidget(self._amount_box)
            self.algo = Algo.pyAudioAnalysis

    def change(self):
        self.do_pyBK = not self.do_pyBK
        if self.do_pyBK:
            self.algo = Algo.pyBK
            self.chose_algo.setCurrentIndex(1)
        else:
            self.algo = Algo.pyannote_audio
            self.chose_algo.setCurrentIndex(0)
    def observer(self):
        direct = QFileDialog.getOpenFileUrl(self,
                                            "open File",
                                            QUrl(os.getcwd()),
                                            "Wav File (*.wav)")
        direct = re.sub("file://", "", direct[0].toString())
        print(direct)
        self.path_line.setText(direct)


    # def draw_wave(self, path_to_file):
    #     import matplotlib.pyplot as plt
    #     import librosa
    #     wav, _ = librosa.load(path_to_file)
    #     plt.plot(wav)
    #     plt.savefig("images/tmp.png")
    #     image = QPixmap("images/tmp.png")
    #     self.wav_label.setPixmap(image)
    #     self.wav_widget.resize(image.width(), image.height())

    def create_msg(self):
        if self.algo != Algo.pyAudioAnalysis:
            return self.path_line.text()
        else:
            amount = int(self._amount_box.text())
            return f"{self.path_line.text()}|-|{amount}"

    def send_processing(self):
        try:
            path_to_file = self.create_msg()
            self.bridge.go(path_to_file, self.algo, self.write_msg)
        except ValueError:
            msg_box = QMessageBox()
            msg_box.setText("Ошибка")
            msg_box.setInformativeText("Необходимо указать целое число "
                                       "говорящих")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()

        # self.draw_wave(path_to_file)

    # def send_processing_pybk(self):
    #     path_to_file = self.path_line.text()
    #     self.bridge.go(path_to_file, Algo.pyBK, self.write_msg)
    #     # self.draw_wave(path_to_file)
    #
    # def send_processing_pyaud(self):
    #     path_to_file = self.path_line.text()
    #     self.bridge.go(path_to_file, Algo.pyAudioAnalysis, self.write_msg)
    #     # self.draw_wave(path_to_file)

    def write_msg(self, msg):
        import matplotlib.pyplot as plt
        from pyannote.core.notebook import Notebook
        print("i tut")
        with open(msg) as f:
            myutil.draw(f, "images/tmp.png")
            print("End")
        image = QPixmap("images/tmp.png")
        # self.pic_layout.removeWidget(self.anno_widget)
        # self.base_layout.removeWidget(self.anno_label)
        # self.anno_widget.deleteLater()
        # self.anno_label.setPicture()
        #
        # # self.anno_widget = QWidget()
        # self.anno_label = QLabel(self.anno_widget)

        # self.anno_label.update(image)
        self.anno_label.setPixmap(image)
        self.anno_widget.resize(image.width(), image.height())
        # self.pic_layout.addWidget(self.anno_widget)
        msg_box = QMessageBox()
        msg_box.setText("Сохранение")
        msg_box.setInformativeText(f"Файл с дневником говорящих записан в "
                                   f"{msg}")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

    def closeEvent(self, event):
        self.bridge.close_q()


class MySwitch(QtWidgets.QPushButton):
    def __init__(self, parent = None):
        super().__init__(parent)
        print('init')
        self.setCheckable(True)
        self.setMinimumWidth(66)
        self.setMinimumHeight(22)

    def paintEvent(self, event):
        label = "Да" if self.isChecked() else "Нет"
        bg_color = Qt.green if self.isChecked() else Qt.red

        radius = 10
        width = 32
        center = self.rect().center()

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.translate(center)
        painter.setBrush(QtGui.QColor(0,0,0))

        pen = QtGui.QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)

        painter.drawRoundedRect(QRect(-width, -radius, 2*width, 2*radius), radius, radius)
        painter.setBrush(QtGui.QBrush(bg_color))
        sw_rect = QRect(-radius, -radius, width + radius, 2*radius)
        if not self.isChecked():
            sw_rect.moveLeft(-width)
        painter.drawRoundedRect(sw_rect, radius, radius)
        painter.drawText(sw_rect, Qt.AlignCenter, label)


# def close():
#     from ipcqueue import posixmq
#     items = ["/pyanno", "/pybk", "/pyaud"]
#     for i in items:
#         tmp = posixmq.Queue(i)
#         while tmp.qsize() > 0:
#             tmp.get()
#         while tmp.qsize() == 0:
#             tmp.put("break")
#         while tmp.qsize() > 0:
#             tmp.get()
#         tmp = posixmq.Queue(f"{i}_return")
#         while tmp.qsize() > 0:
#             tmp.get()