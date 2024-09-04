
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
        'smoking': 0.2,
        'alcohol': 0.2,
        'heartburn': 6.0,
        'chest_pain': 5.0,
        'dysphagia': 5.0,
        'h_pylori': 0.0,
        'nsaids': 0.2,
        'abdominal_pain': 1.0,
        'nausea_vomiting': 1.0,
        'postprandial_pain': 0.5,
        'diarrhea': 0.1,
        'cramps': 0.3,
        'fatigue_anemia': 0.4,
        'urgency': 0.1,
        'weight_loss': 0.1,
        'stress': 1.0,
        'appetite_loss': 0.4,
    },
    'Gastritis': {
        'smoking': 1.2,
        'alcohol': 1.1,
        'heartburn': 1.3,
        'chest_pain': 0.9,
        'dysphagia': 0.4,
        'h_pylori': 2.5,
        'nsaids': 2.2,
        'abdominal_pain': 3.5,
        'nausea_vomiting': 2.3,
        'postprandial_pain': 1.4,
        'diarrhea': 0.7,
        'cramps': 0.6,
        'fatigue_anemia': 0.5,
        'urgency': 0.2,
        'weight_loss': 0.4,
        'stress': 0.8,
        'appetite_loss': 2.2,
    },
    'Dispepsija': {
        'smoking': 1.2,
        'alcohol': 1.0,
        'heartburn': 0.5,
        'chest_pain': 0.8,
        'dysphagia': 0.3,
        'h_pylori': 0.0,
        'nsaids': 1.8,
        'abdominal_pain': 3.0,
        'nausea_vomiting': 2.0,
        'postprandial_pain': 2.8,
        'diarrhea': 0.9,
        'cramps': 1.0,
        'fatigue_anemia': 0.7,
        'urgency': 0.3,
        'weight_loss': 0.4,
        'stress': 1.5,
        'appetite_loss': 1.5,
    },
    'Crohnova bolest': {
        'smoking': 1.7,
        'alcohol': 1.4,
        'heartburn': 0.3,
        'chest_pain': 0.4,
        'dysphagia': 0.3,
        'h_pylori': 0.1,
        'nsaids': 0.4,
        'abdominal_pain': 2.7,
        'nausea_vomiting': 1.6,
        'postprandial_pain': 1.3,
        'diarrhea': 2.4,
        'cramps': 2.6,
        'fatigue_anemia': 2.2,
        'urgency': 1.3,
        'weight_loss': 2.3,
        'stress': 1.1,
        'appetite_loss': 2.4,
    },
    'IBS': {
        'smoking': 1.3,
        'alcohol': 1.2,
        'heartburn': 0.8,
        'chest_pain': 0.7,
        'dysphagia': 0.5,
        'h_pylori': 0.4,
        'nsaids': 0.6,
        'abdominal_pain': 2.5,
        'nausea_vomiting': 1.3,
        'postprandial_pain': 1.4,
        'diarrhea': 1.6,
        'cramps': 2.2,
        'fatigue_anemia': 0.9,
        'urgency': 1.3,
        'weight_loss': 0.9,
        'stress': 1.5,
        'appetite_loss': 0.8,
    },
    'Celijakija': {
        'smoking': 1.2,
        'alcohol': 1.2,
        'heartburn': 0.6,
        'chest_pain': 0.5,
        'dysphagia': 0.4,
        'h_pylori': 0.3,
        'nsaids': 0.4,
        'abdominal_pain': 2.3,
        'nausea_vomiting': 2.0,
        'postprandial_pain': 1.6,
        'diarrhea': 2.8,
        'cramps': 2.0,
        'fatigue_anemia': 2.2,
        'urgency': 1.6,
        'weight_loss': 2.4,
        'stress': 1.3,
        'appetite_loss': 2.3,
    }
}

def map_answers_to_values(survey_response):
    values = {
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
    z-=55.0
    z /= len(values)  # Ovo smanjuje ukupni zbroj i sprječava ekstremne vrijednosti, dijeli se s brojem simptoma
    
    return logistic_regression(z)

#za svaku bolest računa vjerojatnost
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

def generate_disease_recommendation(probability):
    if probability >= 0.8:  
        return "Preporučujemo da hitno posjetite liječnika."
    elif probability >= 0.4:  
        return "Bilo bi dobro da svoje stanje provjerite s liječnikom."
    else:  
        return "Za sada ne morate posjetiti liječnika."

def generate_top_n_recommendations(survey_response, n=3):
    values = map_answers_to_values(survey_response)
    probabilities = generate_probabilities(values)
    
    sorted_diseases = sorted(probabilities, key=probabilities.get, reverse=True)

    highest_probability_disease = sorted_diseases[0]
    highest_probability = probabilities[highest_probability_disease]

    urgency_recommendation = generate_disease_recommendation(highest_probability)
    
    top_diseases = [f"{disease} s vjerojatnošću {probabilities[disease]:.4f}." for disease in sorted_diseases[:n]]
    
    recommendations = [urgency_recommendation]
    recommendations.append(f"Najvjerojatnija bolest: {highest_probability_disease} s vjerojatnošču {highest_probability:.4f}.")
    recommendations.extend(get_recommendations_for_condition(highest_probability_disease))
   

    return recommendations, top_diseases

def get_recommendations_for_condition(condition):
    recommendations = {
        'GERB': [
            "Izbjegavajte masnu i začinjenu hranu.",
            "Jedite manje obroke češće umjesto velikih obroka.",
            "Izbjegavajte ležanje odmah nakon jela.",
        ],
        'Gastritis': [
            "Izbjegavajte začinjenu hranu.",
            "Jedite manje obroke tijekom dana.",
            "Uzmite lijekove koje vam liječnik preporuči, uključujući antibiotike ako je gastritis uzrokovan bakterijom Helicobacter pylori.",
        ],
        'Dispepsija': [
            "Izbjegavajte masnu i tešku hranu, ograničite unos alkohola, kave i gaziranih pića.",
            "Jedite redovito i izbjegavajte prejedanje.",
            "Povećajte unos vlakana u prehrani."
        ],
        'Crohnova bolest': [
            "Jedite pet manjih obroka tijekom dana, smanjite unos masne i pržene hrane.",
            "Izbjegavajte mlijeko i mliječne prerađevine, kao i vlaknaste namirnice.",
            "Pijte puno tekućine i izbjegavajte alkohol i gazirana pića."
        ],
        'IBS': [
            "Izbjegavajte hranu koja uzrokuje nadutost, kao što su grah i kupus.",
            "Uvedite redovite obroke i jedite polako.",
            "Razmislite o promjeni prehrane prema FODMAP prehrani."
        ],
        'Celijakija': [
            "Potpuno izbjegavajte gluten u prehrani.",
            "Pažljivo pročitajte etikete na prehrambenim proizvodima.",
            "Koristite alternativne žitarice poput riže, kukuruza i kvinoje.",
            "Pratite svoj nutritivni status i konzultirajte se s dijetetičarom."
        ]
    }
    return recommendations.get(condition, [])

