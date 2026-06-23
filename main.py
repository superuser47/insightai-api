"""
InsightAI API — Find hidden patterns in your data
The world's first cross-domain pattern detection API
"""
import math
import random
import time
import json
import hashlib
from collections import defaultdict
from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="InsightAI API",
    description="Find hidden patterns in your data with AI",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ═══ MODELS ═══

class DataPoint(BaseModel):
    value: float
    label: Optional[str] = None
    timestamp: Optional[float] = None
    category: Optional[str] = None

class AnalyzeRequest(BaseModel):
    data: List[DataPoint]
    domain: Optional[str] = "general"
    depth: int = 3

class Insight(BaseModel):
    type: str
    description: str
    confidence: float
    details: dict = {}

class AnalyzeResponse(BaseModel):
    insights: List[Insight]
    anomalies: List[dict]
    correlations: List[dict]
    summary: dict
    processing_time_ms: float


# ═══ ENGINE ═══

class InsightEngine:
    """The core pattern detection engine"""

    def analyze(self, data: List[DataPoint], domain: str, depth: int) -> dict:
        values = [d.value for d in data]
        labels = [d.label or f"point_{i}" for i, d in enumerate(data)]

        insights = []
        anomalies = []
        correlations = []

        # 1. Statistical Analysis
        if len(values) >= 2:
            mean = sum(values) / len(values)
            variance = sum((v - mean) ** 2 for v in values) / len(values)
            std = math.sqrt(variance) if variance > 0 else 1e-8

            insights.append(Insight(
                type="statistical",
                description=f"Dataset has mean={mean:.3f}, std={std:.3f}, range=[{min(values):.3f}, {max(values):.3f}]",
                confidence=0.95,
                details={"mean": mean, "std": std, "min": min(values), "max": max(values)},
            ))

            # Anomaly detection
            for i, v in enumerate(values):
                z_score = abs(v - mean) / std
                if z_score > 2:
                    anomalies.append({
                        "index": i,
                        "value": v,
                        "z_score": round(z_score, 3),
                        "label": labels[i],
                        "severity": "high" if z_score > 3 else "medium",
                    })

        # 2. Trend Detection
        if len(values) >= 5:
            x_mean = (len(values) - 1) / 2
            y_mean = sum(values) / len(values)
            numerator = sum((i - x_mean) * (v - y_mean) for i, v in enumerate(values))
            denominator = sum((i - x_mean) ** 2 for i in range(len(values)))
            slope = numerator / denominator if denominator > 0 else 0

            trend = "increasing" if slope > 0.01 else "decreasing" if slope < -0.01 else "stable"
            insights.append(Insight(
                type="trend",
                description=f"Data shows {trend} trend (slope={slope:.4f})",
                confidence=0.8 if abs(slope) > 0.05 else 0.5,
                details={"slope": slope, "trend": trend},
            ))

        # 3. Distribution Analysis
        if len(values) >= 10:
            sorted_vals = sorted(values)
            n = len(sorted_vals)
            q1 = sorted_vals[n // 4]
            q3 = sorted_vals[3 * n // 4]
            iqr = q3 - q1

            skewness = 0
            if len(values) > 2:
                mean = sum(values) / len(values)
                std = (sum((v - mean) ** 2 for v in values) / len(values)) ** 0.5
                if std > 0:
                    skewness = sum(((v - mean) / std) ** 3 for v in values) / len(values)

            insights.append(Insight(
                type="distribution",
                description=f"Distribution skewness={skewness:.3f}, IQR={iqr:.3f}",
                confidence=0.7,
                details={"skewness": skewness, "iqr": iqr, "q1": q1, "q3": q3},
            ))

        # 4. Pattern Detection
        if len(values) >= 10:
            # Check for periodicity
            autocorr = []
            for lag in range(1, min(len(values) // 2, 20)):
                n = len(values) - lag
                if n > 0:
                    mean = sum(values) / len(values)
                    num = sum((values[i] - mean) * (values[i + lag] - mean) for i in range(n))
                    den = sum((v - mean) ** 2 for v in values)
                    corr = num / den if den > 0 else 0
                    autocorr.append((lag, corr))

            if autocorr:
                best_lag, best_corr = max(autocorr, key=lambda x: abs(x[1]))
                if abs(best_corr) > 0.3:
                    insights.append(Insight(
                        type="pattern",
                        description=f"Periodic pattern detected with period={best_lag}, correlation={best_corr:.3f}",
                        confidence=abs(best_corr),
                        details={"period": best_lag, "correlation": best_corr},
                    ))

        # 5. Cross-category Analysis
        categories = defaultdict(list)
        for d in data:
            cat = d.category or "default"
            categories[cat].append(d.value)

        if len(categories) > 1:
            cat_names = list(categories.keys())
            for i in range(len(cat_names)):
                for j in range(i + 1, len(cat_names)):
                    c1 = categories[cat_names[i]]
                    c2 = categories[cat_names[j]]
                    if len(c1) > 1 and len(c2) > 1:
                        # Point-biserial correlation approximation
                        mean1 = sum(c1) / len(c1)
                        mean2 = sum(c2) / len(c2)
                        diff = abs(mean1 - mean2)
                        pooled_std = math.sqrt(
                            (sum((v - mean1) ** 2 for v in c1) + sum((v - mean2) ** 2 for v in c2))
                            / (len(c1) + len(c2) - 2)
                        ) if len(c1) + len(c2) > 2 else 1e-8

                        effect_size = diff / pooled_std if pooled_std > 0 else 0
                        if effect_size > 0.5:
                            correlations.append({
                                "category1": cat_names[i],
                                "category2": cat_names[j],
                                "effect_size": round(effect_size, 3),
                                "mean1": round(mean1, 3),
                                "mean2": round(mean2, 3),
                                "significance": "high" if effect_size > 0.8 else "medium",
                            })

        # Summary
        summary = {
            "data_points": len(data),
            "unique_categories": len(categories),
            "insights_count": len(insights),
            "anomalies_count": len(anomalies),
            "correlations_count": len(correlations),
            "domain": domain,
            "depth": depth,
        }

        return {
            "insights": insights,
            "anomalies": anomalies,
            "correlations": correlations,
            "summary": summary,
        }


engine = InsightEngine()


# ═══ ENDPOINTS ═══

@app.get("/")
async def root():
    return {
        "name": "InsightAI API",
        "version": "1.0.0",
        "description": "Find hidden patterns in your data with AI",
        "docs": "/docs",
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": time.time()}

@app.post("/api/v1/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    start = time.time()

    if not request.data:
        raise HTTPException(status_code=400, detail="No data provided")

    if len(request.data) > 10000:
        raise HTTPException(status_code=400, detail="Maximum 10,000 data points")

    result = engine.analyze(request.data, request.domain, request.depth)
    elapsed = (time.time() - start) * 1000

    return AnalyzeResponse(
        insights=result["insights"],
        anomalies=result["anomalies"],
        correlations=result["correlations"],
        summary=result["summary"],
        processing_time_ms=round(elapsed, 2),
    )

@app.get("/api/v1/plans")
async def get_plans():
    return {
        "plans": {
            "free": {"price": 0, "calls": 100, "features": ["Basic analysis"]},
            "starter": {"price": 29, "calls": 1000, "features": ["Advanced analysis", "Anomalies"]},
            "pro": {"price": 99, "calls": 10000, "features": ["Cross-domain", "Predictions"]},
            "enterprise": {"price": 499, "calls": -1, "features": ["Unlimited", "Custom models"]},
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
