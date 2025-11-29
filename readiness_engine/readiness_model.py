import pandas as pd
from dataclasses import dataclass

@dataclass
class ReadinessResult:
    context: str
    readiness_score: float
    status: str
    issues: list

def compute_readiness_for_batch(df: pd.DataFrame, context: str) -> ReadinessResult:
    issues = []
    score = 100.0

    avg_quality = df["quality_score"].mean()
    avg_lineage = df["lineage_confidence"].mean()

    if avg_quality < 85:
        issues.append(f"Average quality_score below threshold: {avg_quality:.1f}")
        score -= 15

    if avg_lineage < 80:
        issues.append(f"Average lineage_confidence below threshold: {avg_lineage:.1f}")
        score -= 15

    if context == "FraudReview":
        if (df["risk_score"] > 80).sum() == 0:
            issues.append("No high-risk transactions found.")
            score -= 10

    elif context == "CreditDecision":
        low_quality = df["quality_score"] < 70
        if low_quality.sum() > 0:
            issues.append(f"{low_quality.sum()} records have very low quality.")
            score -= 10

    elif context == "AMLReport":
        if (df["aml_flag"] == 1).sum() == 0:
            issues.append("No AML-flagged transactions found.")
            score -= 10

        if (df["ofac_flag"] == 1).sum() > 0 and avg_lineage < 85:
            issues.append("OFAC matches found but lineage is weak.")
            score -= 10

    score = max(0, min(100, score))
    status = "READY" if score >= 85 else "CONDITIONAL" if score >= 70 else "NOT_READY"

    return ReadinessResult(
        context=context,
        readiness_score=score,
        status=status,
        issues=issues
    )
