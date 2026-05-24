import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import scipy.signal as sgn
import scipy.fft as dpf
from matplotlib.colors import Normalize
import os
import csv
import shutil
import librosa

# Тестовая функция для визуализации сигнала и его спектра
def plot_keypress(filepath, show_spectrum= True):

    y, sampling_rate = sf.read(filepath)
    t = np.arange(len(y)) / sampling_rate

    num_plots = 2 if show_spectrum else 1

    fig, axes = plt.subplots(num_plots, 1, figsize=(10, 3 * num_plots), dpi=100)

    ax = axes[0] if num_plots > 1 else axes
    ax.plot(t, y, linewidth=0.5, color='blue')
    ax.set_title(f'Полный сигнал {len(y)/ sampling_rate * 1000:.1f} мс | {len(y)} отсчётов')
    ax.set_xlabel('Время (с)')
    ax.set_ylabel('Амплитуда')
    ax.grid(alpha=0.3)

    if show_spectrum:
        ax = axes[1]
        window = np.hanning(len(y))
        y_windowed = y * window
        Y = np.abs(dpf.rfft(y_windowed))
        freqs = dpf.rfftfreq(len(y), 1 / sampling_rate)

        ax.plot(freqs, Y, linewidth=0.5, color='blue')
        ax.set_title(f'Спектр сигнала')
        ax.set_xlabel('Частота, Гц')
        ax.set_ylabel('Амплитуда')
        ax.grid(alpha=0.3)


    plt.tight_layout()
    plt.show()

# Считает энергию сигнала для заданной величины окна
def ste(signal, sampling_rate, window_ms = 20, shift_ms = 10, smooth = False, visualize = False):
    window_len = int(window_ms * sampling_rate / 1000)
    shift_len = int(shift_ms * sampling_rate / 1000)

    n_frames = (len(signal) - shift_len) // (window_len - shift_len)
    ste = np.zeros(n_frames)
    time_axis = np.zeros(n_frames)

    for i in range(n_frames):
        start = i * shift_len
        ste[i] = np.sum(signal[start:start + window_len] ** 2)

    # В качестве временных меток для визуализации ste взята середина каждого окна
    time_axis = (np.arange(n_frames) * shift_len + window_len // 2) / sampling_rate

    if smooth:
        ste = sgn.medfilt(ste, kernel_size=3)

    if visualize:
        t_signal = np.arange(len(signal)) / sampling_rate
        plt.figure(figsize=(12, 5))
        plt.plot(t_signal, signal, linewidth=0.5, color='blue', label='Signal')
        plt.plot(time_axis, ste * np.max(np.abs(signal))/ np.max(ste), linewidth=1.5, color='red', label='STE')
        plt.title(f'Signal + STE (window={window_ms}ms, shift={shift_ms}ms)')
        plt.grid(alpha=0.3)
        plt.legend(loc='upper right')

        plt.tight_layout()
        plt.show()

    return ste


def detect_keypress(signal, sampling_rate, threshold = 0.2, window_ms = 20, shift_ms = 10, pad_ms = 40, visualize = True):
    ste_vals = ste(signal, sampling_rate, window_ms, shift_ms, False, False)
    key_frames = np.asarray(ste_vals > np.max(ste_vals) * threshold).nonzero()[0]

    start_frame = key_frames[0]
    end_frame = key_frames[-1]

    window_len = int(window_ms * sampling_rate / 1000)
    shift_len = int(shift_ms * sampling_rate / 1000)
    pad_len = int(pad_ms * sampling_rate / 1000)

    start_sample = max(start_frame * shift_len - pad_len, 0)
    end_sample = min(end_frame * shift_len + window_len + pad_len, len(signal))

    press_signal = signal[start_sample:end_sample]


    if visualize:
        t_signal = np.arange(len(signal)) / sampling_rate
        t_press_signal = t_signal[start_sample:end_sample]
        plt.figure(figsize=(12, 5))
        plt.plot(t_signal, signal, linewidth=0.5, color='blue', label='Signal')
        plt.plot(t_press_signal, press_signal, linewidth=1.5, color='red', label='Press_signal')
        plt.grid(alpha=0.3)
        plt.legend(loc='upper right')

        plt.tight_layout()
        plt.show()

    return press_signal

# Пока просто максимум, мб придётся учесть шум потом
def cut_peak(signal, sampling_rate, visualize = True):
    peak_ind = np.argmax(np.abs(signal))

    start_sample = max(0, int(peak_ind - 688))
    end_sample = min(len(signal), int(peak_ind + 1360))
    peak_signal = signal[start_sample:end_sample]

    if visualize:
        t_signal = np.arange(len(signal)) / sampling_rate
        t_peak_signal = t_signal[start_sample:end_sample]
        plt.figure(figsize=(12, 5))
        plt.plot(t_signal, signal, linewidth=0.5, color='blue', label='Signal')
        plt.plot(t_peak_signal, peak_signal, linewidth=1.5, color='red', label='Press_signal')
        plt.grid(alpha=0.3)
        plt.legend(loc='upper right')

        plt.tight_layout()
        plt.show()

    return peak_signal

def dff_features(signal, sr, normalize=False, logarithmize=True, weight=5, offset=5):    

    spectrum = np.abs(dpf.rfft(signal))
    spectrum = spectrum[:1024]

    if normalize:
        mean_val = np.mean(spectrum)
        min_val = np.min(spectrum)
        max_val = np.max(spectrum)
        spectrum = (spectrum - mean_val) / (max_val - min_val + 1e-9)

    if logarithmize:
        spectrum = spectrum * weight + offset
        spectrum = np.log(spectrum)
        min_val = np.min(spectrum)
        max_val = np.max(spectrum)

        spectrum = (spectrum - min_val) / (max_val - min_val) * 2 - 1

    mfcc = librosa.feature.mfcc(y=signal.astype(float), sr=sr, n_mfcc=40)
    mfcc_features = np.concatenate([np.mean(mfcc, axis=1), np.std(mfcc, axis=1)])

    return np.concatenate([spectrum, mfcc_features])  # 1024 + 80 = 1104


def build_dataset(folderpath, output_csv='dataset.csv'):
    subfolders = [str(i) for i in range(10)] + [chr(j) for j in range(97, 124)] + ['space']
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Обновлённый заголовок
        fft_cols = [f'fft_{i}' for i in range(1024)]
        mfcc_cols = [f'mfcc_{i}' for i in range(80)]
        header = fft_cols + mfcc_cols + ['key']
        writer.writerow(header)
        
        for foldername in subfolders:
            for i in range(1, 101):
                filepath = f'{folderpath}/{foldername}_{i}.wav'
                try:
                    signal, sr = sf.read(filepath)
                except Exception:
                    continue
                peak_signal = cut_peak(signal, sr, visualize=False)
                features = dff_features(peak_signal, sr)  # передаём sr
                if len(features) == 1104:                  # обновлённая проверка
                    key = '_' + foldername if foldername.isdigit() else foldername
                    writer.writerow(list(features) + [key])

build_dataset('dataset', 'dataset.csv')
