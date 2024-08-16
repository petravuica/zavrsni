
# Mapa za pretvorbu tekstualnih odgovora u numeričke vrijednosti
VALUE_MAP = {
    'Često': 5,
    'Ponekad': 4,
    'Rijetko': 2,
    'Nikad': 1,
    'Da': 5,
    'Ne': 0,
}
DISEASE_SYMPTOM_WEIGHTS = {
    'GERB': {
        'therapy': 1.0,
        'smoking': 0.3,
        'alcohol': 0.3,
        'heartburn': 5.0,
        'chest_pain': 4.0,
        'dysphagia': 4.0,
        'h_pylori': 0.0,
        'nsaids': 0.3,
        'abdominal_pain': 1.0,
        'nausea_vomiting': 1.0,
        'postprandial_pain': 0.5,
        'diarrhea': 0.2,
        'cramps': 0.5,
        'fatigue_anemia': 0.5,
        'urgency': 0.2,
        'weight_loss': 0.2,
        'stress': 1.0,
        'appetite_loss': 0.5,
    },
    'Gastritis': {
        'therapy': 1.0,
        'smoking': 1.4,
        'alcohol': 1.3,
        'heartburn': 1.5,
        'chest_pain': 1.0,
        'dysphagia': 0.5,
        'h_pylori': 2.3,
        'nsaids': 2.0,
        'abdominal_pain': 3.0,
        'nausea_vomiting': 2.0,
        'postprandial_pain': 1.2,
        'diarrhea': 0.8,
        'cramps': 0.8,
        'fatigue_anemia': 0.8,
        'urgency': 0.3,
        'weight_loss': 0.5,
        'stress': 1.0,
        'appetite_loss': 2.0,
    },
    'Dispepsija': {
        'therapy': 1.0,
        'smoking': 1.3,
        'alcohol': 1.2,
        'heartburn': 0.5,
        'chest_pain': 1.0,
        'dysphagia': 0.5,
        'h_pylori': 0.0,
        'nsaids': 1.9,
        'abdominal_pain': 2.5,
        'nausea_vomiting': 1.5,
        'postprandial_pain': 2.5,
        'diarrhea': 1.0,
        'cramps': 1.0,
        'fatigue_anemia': 0.8,
        'urgency': 0.5,
        'weight_loss': 0.5,
        'stress': 2.0,
        'appetite_loss': 1.2,
    },
    'Crohnova_bolest': {
        'therapy': 1.0,
        'smoking': 1.6,
        'alcohol': 1.3,
        'heartburn': 0.3,
        'chest_pain': 0.3,
        'dysphagia': 0.2,
        'h_pylori': 0.1,
        'nsaids': 0.4,
        'abdominal_pain': 2.5,
        'nausea_vomiting': 1.5,
        'postprandial_pain': 1.2,
        'diarrhea': 2.2,
        'cramps': 2.4,
        'fatigue_anemia': 2.0,
        'urgency': 1.2,
        'weight_loss': 2.0,
        'stress': 1.0,
        'appetite_loss': 2.2,
    },
    'IBS': {
        'therapy': 1.0,
        'smoking': 1.2,
        'alcohol': 1.1,
        'heartburn': 0.8,
        'chest_pain': 0.6,
        'dysphagia': 0.4,
        'h_pylori': 0.3,
        'nsaids': 0.5,
        'abdominal_pain': 2.2,
        'nausea_vomiting': 1.2,
        'postprandial_pain': 1.3,
        'diarrhea': 1.5,
        'cramps': 2.0,
        'fatigue_anemia': 0.7,
        'urgency': 1.2,
        'weight_loss': 0.8,
        'stress': 1.3,
        'appetite_loss': 0.7,
    },
    'Celijakija': {
        'therapy': 1.0,
        'smoking': 1.1,
        'alcohol': 1.1,
        'heartburn': 0.5,
        'chest_pain': 0.4,
        'dysphagia': 0.3,
        'h_pylori': 0.2,
        'nsaids': 0.3,
        'abdominal_pain': 2.0,
        'nausea_vomiting': 1.8,
        'postprandial_pain': 1.4,
        'diarrhea': 2.5,
        'cramps': 1.8,
        'fatigue_anemia': 2.0,
        'urgency': 1.5,
        'weight_loss': 2.0,
        'stress': 1.2,
        'appetite_loss': 2.0,
    }
}

def map_answers_to_values(survey_response):
    values = {
        'therapy': VALUE_MAP.get(survey_response.therapy, 0),
        'smoking': VALUE_MAP.get(survey_response.smoking, 0),
        'alcohol': VALUE_MAP.get(survey_response.alcohol, 0),
        'heartburn': VALUE_MAP.get(survey_response.heartburn, 0),
        'chest_pain': VALUE_MAP.get(survey_response.chest_pain, 0),
        'dysphagia': VALUE_MAP.get(survey_response.dysphagia, 0),
        'h_pylori': VALUE_MAP.get(survey_response.h_pylori, 0),
        'nsaids': VALUE_MAP.get(survey_response.nsaids, 0),
        'abdominal_pain': VALUE_MAP.get(survey_response.abdominal_pain, 0),
        'nausea_vomiting': VALUE_MAP.get(survey_response.nausea_vomiting, 0),
        'postprandial_pain': VALUE_MAP.get(survey_response.postprandial_pain, 0),
        'diarrhea': VALUE_MAP.get(survey_response.diarrhea, 0),
        'cramps': VALUE_MAP.get(survey_response.cramps, 0),
        'fatigue_anemia': VALUE_MAP.get(survey_response.fatigue_anemia, 0),
        'urgency': VALUE_MAP.get(survey_response.urgency, 0),
        'weight_loss': VALUE_MAP.get(survey_response.weight_loss, 0),
        'stress': VALUE_MAP.get(survey_response.stress, 0),
        'appetite_loss': VALUE_MAP.get(survey_response.appetite_loss, 0),
    }
    return values


import math
def logistic_regression(z):
    return 1 / (1 + math.exp(-z))

def calculate_probability(disease_weights, values):
    z = sum(disease_weights[symptom] * values[symptom] for symptom in values)
    # Regularizacija - podijelimo s brojem simptoma
    z /= len(values)  # Ovo smanjuje ukupni zbroj i sprječava ekstremne vrijednosti
    
    return logistic_regression(z)

def generate_probabilities(values):
    probabilities = {}
    for disease, weights in DISEASE_SYMPTOM_WEIGHTS.items():
        probabilities[disease] = calculate_probability(weights, values)
    return probabilities

def generate_recommendation(survey_response):
    values = map_answers_to_values(survey_response)
    probabilities = generate_probabilities(values)
    
    # Generirajte preporuku na temelju najviše vjerojatnosti
    recommended_disease = max(probabilities, key=probabilities.get)
    probability = probabilities[recommended_disease]

    recommendation = f"Preporučena bolest: {recommended_disease} s vjerojatnošću {probability:.4f}"
    
    return recommendation

def generate_top_n_recommendations(survey_response, n=3):
    values = map_answers_to_values(survey_response)
    probabilities = generate_probabilities(values)
    
    sorted_diseases = sorted(probabilities, key=probabilities.get, reverse=True)
    
    # Generiraj top n preporuka
    recommendations = []
    for disease in sorted_diseases[:n]:
        probability = probabilities[disease]
        recommendations.append(f"Preporučena bolest: {disease} s vjerojatnošću {probability:.4f}")
    
    return recommendations
