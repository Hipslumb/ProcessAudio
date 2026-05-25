import sys
import locale
import time

import pyaudio
import wave
import os
import keyboard
import csv
import numpy as np
from datetime import datetime

#sys.stdout.reconfigure(encoding='cp1251')

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 7

class MicrophoneData():

    def __init__(self, dir):
        self.dir = dir
        self.p = pyaudio.PyAudio()
        # self.device = self.select_micro()
        self.device = 0
        time.sleep(0.5)
        self.record_session()


    def select_micro(self):
        print('Input devices available:')
        devices = []
        channels = []
        for i in range(self.p.get_device_count()):
            info = self.p.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0 and (info['maxInputChannels'] not in channels):
                channels.append(info['maxInputChannels'])
                print(f" {i}. {info['name']} (Channel: {info['maxInputChannels']})")
                devices.append([i, info['name']])

        if not devices:
            print('Input devices not found')
            self.p.terminate()
            sys.exit(1)

        choice = input("Select micro index: ").strip()
        if choice.isdigit() and int(choice) in [d[0] for d in devices]:
            idx, name = int(choice), devices[[d[0] for d in devices].index(int(choice))][1]
        else:
            idx, name = devices[0]
            print(f"Autoselected: {name} (ID: {idx})")

        return idx



    def record(self, name):

        stream = self.p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=self.device)

        frames = []

        total_chunks = int((RATE / CHUNK) * RECORD_SECONDS)

        for _ in range(total_chunks):
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)
        self.save_audio(name, frames, self.p)

        stream.stop_stream()
        stream.close()


    def save_audio(self, name, frames, p):
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

        exists = True
        i = 1
        while exists:
            if os.path.exists(f'{self.dir}/{name}_{i}.wav'):
                i += 1
            else:
                exists = False
        name = f'{self.dir}/{name}_{i}.wav'
 
        file = wave.open(name, 'wb')
        file.setnchannels(CHANNELS)
        file.setsampwidth(p.get_sample_size(FORMAT))
        file.setframerate(RATE)
        file.writeframes(b''.join(frames))
        file.close()

    def record_session(self):
        i = 1
        while True:
            print(f'\nEnter key name to record or ESC to finish recording session {i} : ')
            i+=1
            name = keyboard.read_key()
            if name == 'esc':
                self.p.terminate()
                break
            else:
                self.record(name)


# OUT_DIR = input('Give output directory a name: ')

MicrophoneData('tests')

