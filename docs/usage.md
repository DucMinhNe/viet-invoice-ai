# Usage Guide

VietInvoice AI expects text that has already been extracted from a PDF, scan, or OCR pipeline.

## Fallback Mode

Fallback mode is useful for demos and environments without Ollama.

```bash
python3 main.py data/sample_invoice.txt --fallback-only
```

## Local AI Mode

Local AI mode asks an installed Ollama model to extract fields as JSON.

```bash
ollama serve
ollama pull llama3.2
python3 main.py data/sample_invoice.txt
```

## Recommended Input

The parser works best when the input contains clear labels such as:

- `Ma so thue`
- `So hoa don`
- `Ngay`
- `Khach hang`
- `Noi dung`
- `Tong cong`
