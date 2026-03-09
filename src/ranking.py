import os
from src.resume_parser import extract_resume_text
from src.similarity_model import calculate_similarity

def rank_resumes(folder_path,job_description):
    results = []
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path,file)
        resume_text = extract_resume_text(file_path)
        score = calculate_similarity(resume_text,job_description)
        results.append((file,score))
    ranked = sorted(results,key=lambda x:x[1],reverse=True)
    return ranked