# InsightAI API

Find hidden patterns in your data with AI.

## What it does

InsightAI analyzes your business data and discovers:
- Hidden patterns and trends
- Statistical anomalies
- Cross-category correlations
- Periodic behavior

## Quick Start

```bash
# Install
pip install -r requirements.txt

# Run
uvicorn main:app --reload

# Test
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"data": [{"value": 10}, {"value": 15}, {"value": 12}, {"value": 18}, {"value": 25}]}'
```

## API

### POST /api/v1/analyze

**Request:**
```json
{
  "data": [
    {"value": 10, "label": "day1", "category": "sales"},
    {"value": 15, "label": "day2", "category": "sales"},
    {"value": 12, "label": "day3", "category": "marketing"}
  ],
  "domain": "business",
  "depth": 3
}
```

**Response:**
```json
{
  "insights": [...],
  "anomalies": [...],
  "correlations": [...],
  "summary": {...},
  "processing_time_ms": 1.23
}
```

## Pricing

| Plan | Price | API Calls |
|------|-------|-----------|
| Free | $0/mo | 100 |
| Starter | $29/mo | 1,000 |
| Pro | $99/mo | 10,000 |
| Enterprise | $499/mo | Unlimited |

## Deploy

```bash
# Docker
docker build -t insightai .
docker run -p 8000:8000 insightai

# Render.com
# Just connect your GitHub repo
```

## License

MIT
