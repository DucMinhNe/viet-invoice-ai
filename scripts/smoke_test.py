import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main():
    result = subprocess.run(
        [sys.executable, "main.py", "data/sample_invoice.txt", "--fallback-only"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        print(result.stderr)
        return result.returncode

    payload = json.loads(result.stdout)
    required = ["vendor", "tax_code", "invoice_number", "date", "total_amount_vnd"]
    missing = [field for field in required if not payload.get(field)]
    if missing:
        print(f"Missing fields: {missing}")
        return 1

    print("Smoke test passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
