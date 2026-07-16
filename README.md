# InsightAI API

<p align="center">
  <a href="https://superuser47.github.io/cortex-wave10-status/">
    <img src="https://img.shields.io/badge/Wave%2010-Certified-00d4aa?style=for-the-badge&labelColor=1a1a2e" alt="Wave 10 Certified">
  </a>
</p>

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

## Links

| Resource | Description |
|----------|-------------|
| [Black Mirror Dashboard](https://superuser47.github.io/black-mirror-dashboard/) | 4 Live AI Engines — Anomaly Shield, InsightAI, Pattern Scout, Data Oracle |
| [DeepSeek CORS PoC](https://superuser47.github.io/deepseek-cors-poc/) | CORS bypass proof-of-concept for DeepSeek API |
| [CORTEX Wave 10 Status](https://superuser47.github.io/cortex-wave10-status/) | Wave 10 module status dashboard |

---

### Wave 10 Certified (2026-07-17)
Integrated with [Black Mirror Dashboard](https://superuser47.github.io/black-mirror-dashboard/) — 4 Live AI Engines
[CORTEX 37 Modules](https://superuser47.github.io/cortex-wave10-status/) | [DeepSeek CORS PoC](https://superuser47.github.io/deepseek-cors-poc/)

## Get Instant Access

[Buy Now — $29/month](https://gumroad.com/l/insightai) | [Free Trial](https://superuser47.github.io/insightai-api/)

Or use our [Black Mirror Dashboard](https://superuser47.github.io/black-mirror-dashboard/) for free analysis.

---

<p align="center">
  <sub>Wave 10 Certified — Part of the <a href="https://github.com/superuser47/black-mirror-dashboard">Black Mirror Ecosystem</a></sub>
</p>
