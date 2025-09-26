# Technical Notes

The project uses two extraction paths:

1. **Ollama extraction** for flexible local AI parsing.
2. **Regex fallback extraction** for predictable offline demos.

## Field Strategy

The target JSON schema is intentionally small:

```json
{
  "vendor": "string",
  "tax_code": "string",
  "invoice_number": "string",
  "date": "string",
  "buyer": "string",
  "description": "string",
  "total_amount_vnd": 0,
  "confidence": 0.0
}
```

This keeps the output easy to inspect, validate, and export to accounting tools later.
