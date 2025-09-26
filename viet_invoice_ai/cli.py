import argparse
import json
import sys
from pathlib import Path

from viet_invoice_ai.fallback_parser import extract_with_rules
from viet_invoice_ai.ollama_client import OllamaError, extract_with_ollama


def extract(path, use_fallback):
    text = Path(path).read_text(encoding="utf-8")
    if not use_fallback:
        try:
            model, result = extract_with_ollama(text)
            result["_engine"] = f"ollama:{model}"
            return result
        except (OllamaError, json.JSONDecodeError) as error:
            print(f"Local AI unavailable, using fallback parser: {error}", file=sys.stderr)

    result = extract_with_rules(text)
    result["_engine"] = "regex-fallback"
    return result


def main():
    parser = argparse.ArgumentParser(description="Extract structured data from Vietnamese invoice text.")
    parser.add_argument("file", help="Path to invoice text extracted from PDF/OCR.")
    parser.add_argument("--fallback-only", action="store_true", help="Skip Ollama and use the local rule parser.")
    args = parser.parse_args()

    result = extract(args.file, args.fallback_only)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
