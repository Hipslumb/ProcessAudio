import pandas as pd
import sklearn as skl
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report

df = pd.read_csv('dataset.csv')
#missing = df.isnull().sum()
print(df['key'])
X, Y = df.drop(columns=['key']), df['key']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3, random_state = 18, stratify = Y)


model = SVC(kernel='rbf', gamma=0.1)
model.fit(X_train, Y_train)
Y_pred = model.predict(X_test)
metrics = pd.DataFrame(classification_report(Y_test, Y_pred, output_dict = True))
metrics = metrics.drop('support')
print(metrics)