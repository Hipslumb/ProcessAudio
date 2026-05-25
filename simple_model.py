import joblib
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from feature_extracting import plot_keypress, detect_keypress, cut_peak, ste, dff_features

def predict_segment(filepath, model, threshold =0.1):
    
    signal, sr = sf.read(filepath)
    ste_vals = ste(signal, sr, window_ms=20, shift_ms=10)

    from scipy.signal import find_peaks
    peaks, _ = find_peaks(ste_vals, 
                          height=np.max(ste_vals) * threshold,
<<<<<<< HEAD
                        distance=30)
=======
                          distance=25)
>>>>>>> yarikbranch
    
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
keys = predict_segment('./tests/space_1.wav', model)
print('Нажатые клавиши:', keys)