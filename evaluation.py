import requests
import numpy as np

API_URL = (
    "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
)
headers = {"Authorization": f"Bearer {HF_API_KEY}"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            f"Hugging Face API error: {response.status_code} - {response.text}"
        )


def calculate_similarity(answer1, answer2):

    payload = {"inputs": {"source_sentence": answer1, "sentences": [answer2]}}

    try:
        output = query(payload)
        similarity_score = output[0]
        return similarity_score
    except Exception as e:
        print(f"Error: {e}")
        return None
