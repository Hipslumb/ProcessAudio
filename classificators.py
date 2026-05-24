import pandas as pd
import sklearn as skl
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
import joblib
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

df = pd.read_csv('dataset.csv')
X, Y = df.drop(columns=['key']), df['key']

X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.3, random_state=18, stratify=Y
)

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('svm', SVC(kernel='rbf', gamma='scale', C=10))
])

pipeline.fit(X_train, Y_train)
Y_pred = pipeline.predict(X_test)
print(classification_report(Y_test, Y_pred))

# Сохраняем pipeline целиком со scaler внутри
joblib.dump(pipeline, 'model.pkl')

# Матрица ошибок

# cm = confusion_matrix(Y_test, Y_pred, labels=pipeline.classes_)
# disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=pipeline.classes_)

# fig, ax = plt.subplots(figsize=(14, 14))
# disp.plot(ax=ax, colorbar=False, cmap='Blues')
# plt.title('Матрица ошибок')
# plt.tight_layout()
# plt.show()