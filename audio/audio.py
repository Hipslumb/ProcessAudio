import sys
import locale
sys.stdout.reconfigure(encoding='cp1251')

import pyaudio
import wave
import time
import tkinter
import os
import keyboard

import numpy as np

p = pyaudio.PyAudio()


class MicrophoneData():
    def __init__(self):
        # for i in range (p.get_device_count()):
        #     print (i,p.get_device_info_by_index(i)['name'])

        self.record()
        
    def record(self):
        p = pyaudio.PyAudio()
        stream = p.open(
            rate = 44100,
            format=pyaudio.paInt16,
            channels=1,
            frames_per_buffer=1024,
            input=True,
            input_device_index=5
        )

        sounds = []
        print("Press ESC to stop recording audio")
        flag = False

        while True:
            name = keyboard.read_key()
            now = name
            if name!='esc':
                if not flag and keyboard.is_pressed(name):
                    data = stream.read(1024)
                    sounds.append(data)
                    flag = True
                elif flag and keyboard.is_pressed(name):
                    data = stream.read(1024)
                    sounds.append(data)
                elif flag and not keyboard.is_pressed(name):  
                    self.save_audio(name,sounds)
                    sounds = []
            if keyboard.is_pressed('esc'):
                break
        print("END")

        stream.stop_stream()
        stream.close()
        p.terminate()

    def save_audio(self,name, sounds):
        if not os.path.exists('key_sounds'):
            os.makedirs('key_sounds')
        
        exists = True
        i=1
        while exists:
            if os.path.exists(f'key_sounds/{name}{i}.wav'):
                i+=1
            else:
                exists=False
        name = f'key_sounds/{name}{i}.wav'

        file = wave.open(name,'wb')
        file.setnchannels(1)
        file.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        file.setframerate(44100)
        file.writeframes(b''.join(sounds))
        file.close()

MicrophoneData()