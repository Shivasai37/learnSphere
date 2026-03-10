import requests
import os

def get_api_key():
    try:
        with open('.env') as f:
            for line in f:
                if line.startswith('GROQ_API_KEY'):
                    return line.strip().split('=', 1)[1]
    except:
        pass
    return os.environ.get('GROQ_API_KEY', '')

def call_groq(prompt):
    api_key = get_api_key()
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 2048
    }
    response = requests.post(url, json=body, headers=headers, timeout=60)
    data = response.json()
    if "choices" not in data:
        raise Exception(data.get("error", {}).get("message", "Groq API error"))
    return data["choices"][0]["message"]["content"]

def validate_ml_topic(topic):
    """
    Ask Groq itself to validate if the topic is ML/AI related.
    Returns True if valid ML topic, False otherwise.
    """
    api_key = get_api_key()
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": f"""
Is "{topic}" a topic related to Machine Learning, Artificial Intelligence, Deep Learning, Data Science, or Statistics?

Answer with ONLY one word: YES or NO
"""}],
        "temperature": 0,
        "max_tokens": 5
    }
    try:
        response = requests.post(url, json=body, headers=headers, timeout=15)
        data = response.json()
        answer = data["choices"][0]["message"]["content"].strip().upper()
        return "YES" in answer
    except:
        return True  # If validation fails, allow it through

def generate_text_explanation(topic, complexity="Intermediate"):
    if not validate_ml_topic(topic):
        raise Exception(f'"{topic}" is not an ML or AI related topic. Please enter a Machine Learning or AI topic like neural networks, decision trees, gradient descent, etc.')

    prompt = f"""
    You are an expert ML educator. Generate a {complexity} level explanation of: {topic}

    Structure:
    1. Overview
    2. Key Concepts
    3. How It Works (step by step)
    4. Real World Applications
    5. Summary

    Make it clear and appropriate for {complexity} level learners.
    If this topic is not related to Machine Learning or AI, respond with:
    "This topic is not related to ML. Please enter an ML or AI topic."
    """
    return call_groq(prompt)

def generate_code_explanation(topic, complexity="Intermediate"):
    if not validate_ml_topic(topic):
        raise Exception(f'"{topic}" is not an ML or AI related topic. Please enter a Machine Learning or AI topic.')

    prompt = f"""
    Generate a complete working Python implementation of the ML algorithm: {topic}

    Requirements:
    - Detailed inline comments
    - All import statements at top
    - Main execution block
    - Print statements showing output
    - Complexity: {complexity}
    - Runnable in Google Colab or locally
    - Comment block listing required libraries

    Return ONLY the Python code, no markdown.
    If this is not an ML topic, return a comment saying so.
    """
    return call_groq(prompt)

def generate_audio_script(topic, length="Medium"):
    if not validate_ml_topic(topic):
        raise Exception(f'"{topic}" is not an ML or AI related topic. Please enter a Machine Learning or AI topic.')

    length_map = {"Brief": "2-3 minutes", "Medium": "5-6 minutes", "Detailed": "8-10 minutes"}
    duration = length_map.get(length, "5-6 minutes")
    prompt = f"""
    Create a conversational podcast-style audio lesson about the ML topic: {topic}
    Duration: {duration}

    - Start with a friendly introduction
    - Use simple spoken language, no bullet points or markdown
    - Use analogies and real world examples
    - End with a clear summary
    - Write as if speaking directly to the listener

    Return only the plain script text.
    """
    return call_groq(prompt)

def generate_image_prompts(topic):
    if not validate_ml_topic(topic):
        raise Exception(f'"{topic}" is not an ML or AI related topic. Please enter a Machine Learning or AI topic.')

    prompt = f"""
    Create 3 detailed image generation prompts for educational diagrams about the ML topic: {topic}

    Format as numbered list. Each should describe a clear educational technical diagram.
    """
    return call_groq(prompt)
