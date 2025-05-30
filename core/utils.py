import requests
from bs4 import BeautifulSoup
import instructor
from groq import Groq
from pydantic import BaseModel
import os
GROQ_API_KEY = "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"
client  = instructor.from_groq(Groq(api_key=GROQ_API_KEY), mode = instructor.Mode.JSON)
class EmployeeAndCompanySummary(BaseModel):
    company_summary: str
    employee_summary: str


def search_duckduckgo(query):
    url = "https://html.duckduckgo.com/html/"
    res = requests.post(url, data={"q": query})
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("a", class_="result__a", limit=5)
    snippets = soup.find_all("a", class_="result__snippet", limit=5)

    texts = []
    for r, s in zip(results, snippets):
        texts.append(f"{r.get_text()}. {s.get_text()}")
    return "\n".join(texts)



  # Store in .env or set as environment variable

def call_open_llm_api(prompt):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        response_model = EmployeeAndCompanySummary,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.model_dump()





    # url = "https://api.groq.com/openai/v1/chat/completions"
    # headers = {
    #     "Authorization": f"Bearer {GROQ_API_KEY}",
    #     "Content-Type": "application/json"
    # }
    # payload = {
    #     "model": "llama3-8b-8192",  # or try `llama3-70b-8192` if needed
    #     "messages": [
    #         {"role": "user", "content": prompt}
    #     ],
    #     "temperature": 0.7
    # }

    # response = requests.post(url, headers=headers, json=payload)
    # response.raise_for_status()
    # return response.json()["choices"][0]["message"]["content"]
