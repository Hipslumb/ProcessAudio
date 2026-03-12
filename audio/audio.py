import sys
import locale
import pyaudio
import wave
import os
import keyboard

sys.stdout.reconfigure(encoding='cp1251')

CHUNK = 1024    
FORMAT = pyaudio.paInt16        
CHANNELS = 1
RATE = 44100                    
RECORD_SECONDS = 5  
DEVICE = 0

class MicrophoneData():

    def __init__(self):
        self.record()
        
    def record(self):

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=DEVICE)

        frames = []
        print("Press ESC to stop recording audio")
        flag = False

        while True:
            data = stream.read(CHUNK)
            frames.append(data)
            name = keyboard.read_key()
            if name!='esc':

                if not flag and keyboard.is_pressed(name):
                    data = stream.read(CHUNK)
                    frames.append(data)
                    flag = True

                elif flag and keyboard.is_pressed(name):
                    data = stream.read(CHUNK)
                    frames.append(data)

                elif flag and not keyboard.is_pressed(name):  
                    self.save_audio(name,frames,p)
                    frames = []

            if keyboard.is_pressed('esc'):
                break
        print("END")

        stream.stop_stream()
        stream.close()
        p.terminate()

    def save_audio(self, name, frames,p):
        if not os.path.exists('key_frames'):
            os.makedirs('key_frames')
        
        exists = True
        i=1
        while exists:
            if os.path.exists(f'key_frames/{name}{i}.wav'):
                i+=1
            else:
                exists=False
        name = f'key_frames/{name}{i}.wav'

        file = wave.open(name,'wb')
        file.setnchannels(CHANNELS)
        file.setsampwidth(p.get_sample_size(FORMAT))
        file.setframerate(RATE)
        file.writeframes(b''.join(frames))
        file.close()

MicrophoneData()