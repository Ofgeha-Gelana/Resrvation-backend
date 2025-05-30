import requests
GROQ_API_KEY="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"
def call_open_llm_api(prompt):
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
    )
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content'].strip()
