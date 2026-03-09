import spacy

# load NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")
# basic skill list (you can expand later)
skills_list = [
    "python","machine learning","sql","deep learning",
    "tensorflow","pytorch","pandas","scikit-learn",
    "nlp","spacy","nltk","transformers",
    "data analysis","statistics","tableau",
    "power bi","excel","docker","flask","django"
]

def extract_skills(text):

    doc = nlp(text)

    found_skills = []

    for token in doc:
        if token.text.lower() in skills_list:
            found_skills.append(token.text.lower())

    return list(set(found_skills))