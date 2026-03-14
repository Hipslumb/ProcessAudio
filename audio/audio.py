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
DEVICE = 5

class MicrophoneData():

    def __init__(self):
        self.record()
        
    def record(self):

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=DEVICE)

        frames = []
        print("Press key that you want to record, then press it again")
        print("Press ESC to stop recording")
        # we create a name for the file
        name = keyboard.read_key()
        # continue recording (you need to press again)
        while True:
            data = stream.read(CHUNK)
            frames.append(data)
            # stop recording after pressing esc
            if keyboard.is_pressed('esc'):
                self.save_audio(name,frames,p)
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