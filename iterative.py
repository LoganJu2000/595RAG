import pandas as pd
import numpy as np
import os
from typing import List
import requests
from openai import OpenAI
from huggingface_hub import InferenceClient


def feedback_evaluate(
    query: str, retrieved_content: str, model_name="meta-llama/Meta-Llama-3-8B-Instruct"
) -> str:
    """
    Evaluate the relevance of retrieved content for a given query using Llama.

    :param query: The original query.
    :param retrieved_content: The retrieved content to be evaluated.
    :param model_name: The Llama model name.
    :return: Feedback as "Irrelevant", "Partially Relevant", or "Fully Relevant".
    """
    prompt = f"""
    You are an expert evaluator. Your task is to assess how relevant a piece of retrieved content is to a given query.
    The retrieved content should directly address the query and provide useful information.
    
    Here are the evaluation criteria:
    - "Fully Relevant": The content completely addresses the query with accurate and detailed information.
    - "Partially Relevant": The content somewhat addresses the query but lacks important details or includes unrelated information.
    - "Irrelevant": The content does not address the query or is unrelated to it.
    
    Query: {query}
    Retrieved Content: {retrieved_content}
    
    Based on the criteria above, provide one of the following labels: "Fully Relevant", "Partially Relevant", or "Irrelevant".
    """

    client = InferenceClient(api_key="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")

    messages = [{"role": "user", "content": prompt}]

    stream = client.chat.completions.create(
        model=model_name, messages=messages, max_tokens=100, stream=True
    )

    # Initialize an empty string to store the accumulated result
    result_string = ""

    # Iterate through the stream and accumulate content into the result string
    for chunk in stream:
        result_string += chunk.choices[0].delta.content

    # Extract the feedback label from the response
    feedback = result_string.strip()

    # Ensure the feedback is valid
    if feedback not in ["Fully Relevant", "Partially Relevant", "Irrelevant"]:
        feedback = "Irrelevant"  # Default to "Irrelevant" if response is unclear

    return feedback
