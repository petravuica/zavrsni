

# Mapa za pretvorbu tekstualnih odgovora u numeričke vrijednosti
VALUE_MAP = {
    'Često': 5,
    'Ponekad': 4,
    'Rijetko': 2,
    'Nikad': 1,
    'Da': 5,
    'Ne': 0,
    'M': 1,
    'Ž' : 0
}

def map_answers_to_values(survey_response):
    values = {
        'therapy': VALUE_MAP.get(survey_response.therapy, 0),
        'age': survey_response.age,
        'gender': VALUE_MAP.get(survey_response.gender, 0),
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

def simple_risk_assessment(values):
    score = (
        values['therapy'] +
        values['smoking'] +
        values['alcohol'] +
        values['heartburn'] +
        values['chest_pain'] +
        values['dysphagia'] +
        values['h_pylori'] +
        values['nsaids'] +
        values['abdominal_pain'] +
        values['nausea_vomiting'] +
        values['postprandial_pain'] +
        values['diarrhea'] +
        values['cramps'] +
        values['fatigue_anemia'] +
        values['urgency'] +
        values['weight_loss'] +
        values['stress'] +
        values['appetite_loss']
    )

    # Definiši granice rizika
    if score >= 70:
        return "Imate jako velike mogućnosti, javite se lječniku što prije"
    elif score >= 35:
        return "Imate mogućnosti, pratite simptome"
    else:
        return "Nemate nikakav rizik"

def generate_recommendation(survey_response):
    values = map_answers_to_values(survey_response)
    recommendation = simple_risk_assessment(values)
    return recommendation

