import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from viet_invoice_ai.fallback_parser import extract_with_rules


def main():
    text = (
        "CONG TY TNHH ABC\n"
        "Ma so thue: 0101234567-001\n"
        "So hoa don: HD-2026-0420\n"
        "Khach hang: Cong ty Co phan Minh An\n"
        "Tong cong: 1.500.000\n"
    )
    result = extract_with_rules(text)

    checks = {
        "tax_code": "0101234567-001",
        "invoice_number": "HD-2026-0420",
        "buyer": "Cong ty Co phan Minh An",
        "total_amount_vnd": 1500000,
    }
    for field, expected in checks.items():
        got = result.get(field)
        if got != expected:
            print(f"FAIL {field}: expected {expected!r}, got {got!r}")
            return 1

    zero_text = (
        "CONG TY TNHH ABC\n"
        "Ma so thue: 0101234567\n"
        "So hoa don: HD-001\n"
        "Khach hang: Cong ty XYZ\n"
        "Noi dung: Bao hanh mien phi\n"
        "Ngay: 01/09/2026\n"
        "Tong cong: 0 VND\n"
    )
    zero_result = extract_with_rules(zero_text)
    if zero_result.get("total_amount_vnd") != 0 or zero_result.get("confidence") != 1.0:
        print(f"FAIL zero_result: total={zero_result.get('total_amount_vnd')}, confidence={zero_result.get('confidence')}")
        return 1

    print("Fallback casing test passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
