import joblib
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from feature_extracting import plot_keypress, detect_keypress, cut_peak, ste, dff_features
from scipy.signal import find_peaks

def predict_segment(filepath, model, threshold =0.2):
    
    signal, sr = sf.read(filepath)
    ste_vals = ste(signal, sr, window_ms=20, shift_ms=10)

    noise_floor = np.percentile(ste_vals, 90)
    # height=np.max(ste_vals) * threshold

    peaks, _ = find_peaks(ste_vals,height=noise_floor * 6, distance=30)
    
    result = []

    for peak in peaks:

        shift_len = int(10*sr /1000)
        center = peak * shift_len
        start = max(0, center - 300)
        end = min(len(signal), center + 1748)

        segment = signal[start:end]
        segment = segment / (np.max(np.abs(segment)) + 1e-9)

        features = dff_features(segment, sr)
        if len(features) == 88:
            X = np.array(features).reshape(1, -1)
            prediction = model.predict(X)[0]
            result.append(prediction)
    return result

model = joblib.load('model.pkl')
keys = predict_segment('./text/h_1.wav', model)

processed_keys = [' ' if key == 'space' else key for key in keys]
corrected_text = ''.join(processed_keys)

with open('keys.txt', 'w', encoding='utf-8') as file:
    file.write(corrected_text)

print('Нажатые клавиши:', keys)