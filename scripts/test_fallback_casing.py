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

    # Statutory date & alternate total label tests
    statutory_text = (
        "CONG TY CO PHAN SAO KIM\n"
        "Ma so thue: 0312345678\n"
        "So hoa don: HD-2026-9999\n"
        "Khach hang: Nguyen Van A\n"
        "Noi dung: Tu van chuyen doi so\n"
        "Ngay 15 thang 04 nam 2026\n"
        "Tong tien: 25.000.000 VND\n"
    )
    statutory_result = extract_with_rules(statutory_text)
    if statutory_result.get("date") != "15 thang 04 nam 2026":
        print(f"FAIL statutory date: expected '15 thang 04 nam 2026', got {statutory_result.get('date')!r}")
        return 1
    if statutory_result.get("total_amount_vnd") != 25000000:
        print(f"FAIL statutory total: expected 25000000, got {statutory_result.get('total_amount_vnd')!r}")
        return 1

    iso_text = (
        "CONG TY TNHH LOGISTICS\n"
        "Ma so thue: 0312345678\n"
        "So hoa don: HD-2026-0001\n"
        "Khach hang: Cong ty Alpha\n"
        "Noi dung: Cuoc van chuyen\n"
        "Date: 2026-04-15\n"
        "Thanh tien: 10.500.000 VND\n"
    )
    iso_result = extract_with_rules(iso_text)
    if iso_result.get("date") != "2026-04-15":
        print(f"FAIL iso date: expected '2026-04-15', got {iso_result.get('date')!r}")
        return 1
    if iso_result.get("total_amount_vnd") != 10500000:
        print(f"FAIL iso total: expected 10500000, got {iso_result.get('total_amount_vnd')!r}")
        return 1

    header_text = (
        "HÓA ĐƠN GIÁ TRỊ GIA TĂNG\n"
        "(Bản thể hiện của hóa đơn điện tử)\n"
        "Công ty Cổ phần Công nghệ Minh Lê\n"
        "Ma so thue: 0312345678\n"
        "So hoa don: HD-2026-0042\n"
        "Ngay: 27.11.2026\n"
        "Khach hang: Nguyen Van A\n"
        "Noi dung: Dich vu phan mem\n"
        "Tong cong: 1.000.000 VND\n"
    )
    header_result = extract_with_rules(header_text)
    if header_result.get("vendor") != "Công ty Cổ phần Công nghệ Minh Lê":
        print(f"FAIL vendor skip header: expected 'Công ty Cổ phần Công nghệ Minh Lê', got {header_result.get('vendor')!r}")
        return 1
    if header_result.get("date") != "27.11.2026":
        print(f"FAIL dot date: expected '27.11.2026', got {header_result.get('date')!r}")
        return 1

    template_header_text = (
        "Mẫu số: 1/001\n"
        "Ký hiệu: 1C26TML\n"
        "HÓA ĐƠN GIÁ TRỊ GIA TĂNG\n"
        "(Bản thể hiện của hóa đơn điện tử)\n"
        "Đơn vị bán hàng: Công ty Cổ phần Công nghệ Sao Việt\n"
        "Mã số thuế: 0101234567 - 001\n"
        "Số hóa đơn: HD-2026-0042\n"
        "Ngày: 28/11/2026\n"
        "Khách hàng: Nguyen Van A\n"
        "Nội dung: Dich vu phan mem\n"
        "Tổng cộng: 1.000.000 VND\n"
    )
    template_result = extract_with_rules(template_header_text)
    if template_result.get("vendor") != "Công ty Cổ phần Công nghệ Sao Việt":
        print(f"FAIL vendor skip template/serial: expected 'Công ty Cổ phần Công nghệ Sao Việt', got {template_result.get('vendor')!r}")
        return 1
    if template_result.get("tax_code") != "0101234567 - 001":
        print(f"FAIL spaced branch tax code: expected '0101234567 - 001', got {template_result.get('tax_code')!r}")
        return 1

    tax13_text = (
        "Công ty TNHH Viễn Thông\n"
        "Mã số thuế: 0101234567890\n"
        "Số hóa đơn: HD-2026-0099\n"
        "Ngày: 28/11/2026\n"
        "Khách hàng: Nguyen Van A\n"
        "Nội dung: Cuoc vien thong\n"
        "Tổng cộng: 500.000 VND\n"
    )
    tax13_result = extract_with_rules(tax13_text)
    if tax13_result.get("tax_code") != "0101234567890":
        print(f"FAIL 13-digit tax code: expected '0101234567890', got {tax13_result.get('tax_code')!r}")
        return 1

    print("Fallback casing test passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
