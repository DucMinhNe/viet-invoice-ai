import re


PATTERNS = {
    "tax_code": r"(?:ma so thue|mst|tax code)\s*[:\-]?\s*([0-9]{10,13})",
    "invoice_number": r"(?:so hoa don|invoice no|invoice number)\s*[:\-]?\s*([A-Z0-9\-]+)",
    "date": r"(?:ngay|date)\s*[:\-]?\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})",
    "buyer": r"(?:khach hang|buyer)\s*[:\-]?\s*(.+)",
    "description": r"(?:noi dung|description)\s*[:\-]?\s*(.+)",
    "total_amount_vnd": r"(?:tong cong|tong thanh toan|total)\s*[:\-]?\s*([0-9\., ]+)",
}


def normalize(text):
    replacements = str.maketrans({
        "Đ": "D", "đ": "d",
        "á": "a", "à": "a", "ả": "a", "ã": "a", "ạ": "a",
        "ă": "a", "ắ": "a", "ằ": "a", "ẳ": "a", "ẵ": "a", "ặ": "a",
        "â": "a", "ấ": "a", "ầ": "a", "ẩ": "a", "ẫ": "a", "ậ": "a",
        "é": "e", "è": "e", "ẻ": "e", "ẽ": "e", "ẹ": "e",
        "ê": "e", "ế": "e", "ề": "e", "ể": "e", "ễ": "e", "ệ": "e",
        "í": "i", "ì": "i", "ỉ": "i", "ĩ": "i", "ị": "i",
        "ó": "o", "ò": "o", "ỏ": "o", "õ": "o", "ọ": "o",
        "ô": "o", "ố": "o", "ồ": "o", "ổ": "o", "ỗ": "o", "ộ": "o",
        "ơ": "o", "ớ": "o", "ờ": "o", "ở": "o", "ỡ": "o", "ợ": "o",
        "ú": "u", "ù": "u", "ủ": "u", "ũ": "u", "ụ": "u",
        "ư": "u", "ứ": "u", "ừ": "u", "ử": "u", "ữ": "u", "ự": "u",
        "ý": "y", "ỳ": "y", "ỷ": "y", "ỹ": "y", "ỵ": "y",
    })
    return text.translate(replacements).lower()


def amount_to_int(value):
    digits = re.sub(r"[^0-9]", "", value or "")
    return int(digits) if digits else None


def extract_vendor(text):
    for line in text.splitlines():
        cleaned = line.strip()
        if cleaned and not cleaned.lower().startswith(("hoa don", "invoice")):
            return cleaned
    return None


def extract_with_rules(text):
    normalized = normalize(text)
    result = {
        "vendor": extract_vendor(text),
        "tax_code": None,
        "invoice_number": None,
        "date": None,
        "buyer": None,
        "description": None,
        "total_amount_vnd": None,
        "confidence": 0.0,
        "notes": "Extracted with regex fallback because local AI was unavailable.",
    }

    for key, pattern in PATTERNS.items():
        match = re.search(pattern, normalized, flags=re.I)
        if match:
            result[key] = match.group(1).strip()

    result["total_amount_vnd"] = amount_to_int(result["total_amount_vnd"])
    found = sum(1 for key, value in result.items() if key not in {"confidence", "notes"} and value)
    result["confidence"] = round(found / 7, 2)
    return result
