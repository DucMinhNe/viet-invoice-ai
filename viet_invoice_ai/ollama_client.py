import json
import urllib.error
import urllib.request


OLLAMA_URL = "http://localhost:11434"
PREFERRED_MODELS = ["llama3.2", "llama3.1", "qwen2.5", "qwen2", "mistral", "gemma2"]


class OllamaError(RuntimeError):
    pass


def request_json(path, payload=None, timeout=90):
    data = None
    method = "GET"
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        method = "POST"

    request = urllib.request.Request(
        f"{OLLAMA_URL}{path}",
        data=data,
        method=method,
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as error:
        raise OllamaError("Ollama is not running. Start it with `ollama serve`.") from error


def choose_model():
    response = request_json("/api/tags", timeout=10)
    models = [model["name"] for model in response.get("models", [])]

    for preferred in PREFERRED_MODELS:
        for model in models:
            if model.startswith(preferred):
                return model

    if not models:
        raise OllamaError("No Ollama model found. Run `ollama pull llama3.2`.")
    return models[0]


def extract_with_ollama(invoice_text):
    model = choose_model()
    prompt = f"""
Extract structured data from this Vietnamese invoice.

Return only valid JSON with these keys:
vendor, tax_code, invoice_number, date, buyer, description, total_amount_vnd, confidence, notes.

Invoice text:
{invoice_text}
""".strip()

    payload = {
        "model": model,
        "stream": False,
        "messages": [
            {
                "role": "system",
                "content": "You extract Vietnamese invoice data. Return strict JSON only.",
            },
            {"role": "user", "content": prompt},
        ],
        "options": {"temperature": 0.1, "num_predict": 500},
    }
    response = request_json("/api/chat", payload)
    content = response.get("message", {}).get("content", "").strip()
    return model, json.loads(content)
