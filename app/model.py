import joblib

# Загружаем модель из файла
model = joblib.load("model/model.pkl")


# Предсказываем класс и вероятность
def make_prediction(df):
    prediction = model.predict(df.values)[0]
    probability = model.predict_proba(df.values)[:, 1][0]
    return prediction, probability
