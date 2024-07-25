from sklearn.linear_model import LogisticRegression
import numpy as np

# Ovdje bi trebao imati svoje prethodno trenirane modele ili obučeni model
model = LogisticRegression()  # Ovo je samo primjer, trebat će ti stvarni obučeni model

def predict_risk(features):
    # Pretvori feature u numpy array i dodaj dimenziju za model
    features_array = np.array([list(features.values())])
    probability = model.predict_proba(features_array)[0, 1]  # Vjerojatnost pozitivnog slučaja
    return probability
