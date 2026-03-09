from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(resume,job_description):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume,job_description])
    score = cosine_similarity(tfidf_matrix[0:1],tfidf_matrix[1:2])
    return score[0][0]