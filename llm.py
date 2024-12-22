import pandas as pd
import numpy as np
import os
from typing import List
import requests
from openai import OpenAI
from huggingface_hub import InferenceClient

HF_API_TOKEN = os.getenv("HF_API_TOKEN")


def llama_answer(
    question: str, model_name="meta-llama/Meta-Llama-3-8B-Instruct"
) -> str:

    prompt = "You are an expert answering common sense question.\n"
    prompt += f"Question: {question}\n"
    client = InferenceClient(api_key=HF_API_TOKEN)

    messages = [{"role": "user", "content": prompt}]

    stream = client.chat.completions.create(
        model=model_name, messages=messages, max_tokens=5000, stream=True
    )
    # Initialize an empty string to store the accumulated result
    result_string = ""

    # Iterate through the stream and accumulate content into the result string
    for chunk in stream:
        result_string += chunk.choices[0].delta.content
    return result_string


def gpt_answer(question: str, model_name="gpt-4o-mini") -> str:
    client = OpenAI()
    messages = [
        {"role": "system", "content": f"You are an expert at common sense."},
        {"role": "user", "content": question},
    ]
    try:
        response = client.chat.completions.create(model=model_name, messages=messages)
        output = response.choices[0].message.content.strip()
        return output
    except Exception as e:
        print(f"Error: {e}")
        return None
