import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from viet_invoice_ai.fallback_parser import extract_with_rules


def main():
    text = (
        "CONG TY TNHH ABC\n"
        "So hoa don: HD-2026-0420\n"
        "Khach hang: Cong ty Co phan Minh An\n"
        "Tong cong: 1.500.000\n"
    )
    result = extract_with_rules(text)

    checks = {
        "invoice_number": "HD-2026-0420",
        "buyer": "Cong ty Co phan Minh An",
        "total_amount_vnd": 1500000,
    }
    for field, expected in checks.items():
        got = result.get(field)
        if got != expected:
            print(f"FAIL {field}: expected {expected!r}, got {got!r}")
            return 1

    print("Fallback casing test passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
