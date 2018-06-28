import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

import pygame

import struct
import pyaudio
from scipy.fftpack import fft
from scipy.signal import kaiser, butter, filtfilt, argrelextrema

import sys
import time

from itertools import zip_longest


class AudioStream(object):
    def __init__(self):

        # pyqtgraph
        pg.setConfigOptions(antialias=True)
        self.traces = dict()
        self.app = QtGui.QApplication(sys.argv)
        self.win = pg.GraphicsWindow(title='')
        self.win.setWindowTitle('')
        self.win.setGeometry(5, 115, 800, 600)

        self.waveform = self.win.addPlot(row=1, col=1)
        self.spectrum = self.win.addPlot(row=2, col=1)
        self.waveform.hideAxis('bottom')
        self.spectrum.hideAxis('bottom')
        self.waveform.hideAxis('left')
        self.spectrum.hideAxis('left')

        # pyaudio
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 4096

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            output=True,
            frames_per_buffer=self.CHUNK,
        )

        # waveform and spectrum x points
        self.x = np.arange(0, 2 * self.CHUNK, 2)
        self.f = np.linspace(0, self.RATE / 2, self.CHUNK / 2)
        self.b, self.a = butter(4, (73/self.RATE, 1175/self.RATE), btype='bandpass')
        self.w = kaiser(self.CHUNK, beta=24)

        # pygame
        pygame.init()
        self.screen = pygame.display.set_mode((735, 355))
        self.screen.fill((0, 0, 0))
        pygame.display.flip()
        # self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 21)

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def set_plotdata(self, name, data_x, data_y):
        if name in self.traces:
            self.traces[name].setData(data_x, data_y)
        else:
            if name == 'waveform':
                self.traces[name] = self.waveform.plot(pen='c', width=3)
                self.waveform.setYRange(0, 255, padding=0)
                self.waveform.setXRange(0, 2 * self.CHUNK, padding=0.005)
            if name == 'spectrum':
                self.traces[name] = self.spectrum.plot(pen='c', width=3, symbol='d')
                self.spectrum.setLogMode(x=True, y=True)
                self.spectrum.setYRange(-4, 0, padding=0)
                self.spectrum.setXRange(np.log10(20), np.log10(self.RATE / 2), padding=0.005)
    
    def set_paint(self, data_x, data_y, color):
        for x, y in zip(data_x, data_y):
            self.screen.set_at((x, y), color)
        s = "-"
        self.screen.fill((0, 0, 0), rect=pygame.Rect((10, 300), (80, 21)))
        fps = self.font.render(s.join(map(str, color)), True, pygame.Color('white'))
        self.screen.blit(fps, (10, 300))
        pygame.display.flip()
        # print(self.clock.get_fps())
        # self.clock.tick(30)

    def control_frets_to_color(self, sp_data):
        n_freqs = argrelextrema(sp_data, np.greater)[0][:3]
        return [x + y for x, y in zip_longest((0, 0, 0), n_freqs, fillvalue=0)]

    def update(self):
        wf_data = self.stream.read(self.CHUNK)
        wf_data = struct.unpack(str(2 * self.CHUNK) + 'B', wf_data)
        wf_data = np.array(wf_data, dtype='b')[::2] + 128
        self.set_plotdata(name='waveform', data_x=self.x, data_y=wf_data,)

        wf_data_filtered = filtfilt(self.b, self.a, wf_data)

        sp_data = fft((np.array(wf_data_filtered, dtype='int8') - 128)*self.w)
        sp_data = np.abs(sp_data[0:int(self.CHUNK / 2)]) * 2 / (128 * self.CHUNK)

        sp_data = np.round(sp_data, decimals=3)

        self.set_plotdata(name='spectrum', data_x=self.f, data_y=sp_data)
        self.set_paint(data_x=self.f.astype(int)//10, data_y=wf_data.astype(int), color=self.control_frets_to_color(sp_data[:100]))

    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(20)
        self.start()


if __name__ == '__main__':
    audio_app = AudioStream()
    audio_app.animation()
