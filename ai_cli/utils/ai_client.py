
import httpx


def ask_llm(prompt: str) -> str:
    url = "http://localhost:1234/v1/chat/completions"

    payload = {
        "model": "lfm2-1.2b",
        "messages": [
            {"role": "system", "content": "You are a helpful programming assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 5000,
        "temperature": 0.7
    }

    try:
        response = httpx.post(url, json=payload, timeout=800)
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise RuntimeError(f"❌ Błąd HTTP {e.response.status_code}: {e.response.text}")
    except httpx.RequestError as e:
        raise RuntimeError(f"❌ Błąd połączenia: {e}")

    return response.json()["choices"][0]["message"]["content"].strip()
