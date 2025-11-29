import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# ---- CONFIG ----
NUM_ROWS = 3000
START_DATE = datetime(2025, 1, 1)
END_DATE   = datetime(2025, 3, 31)

# Ensure output directory exists
os.makedirs("data", exist_ok=True)

# Generate random dates in quarter
def random_dates(start, end, n):
    delta = end - start
    return [start + timedelta(days=random.randint(0, delta.days)) for _ in range(n)]

# Generate data
np.random.seed(42)

df = pd.DataFrame({
    "transaction_id": range(1, NUM_ROWS + 1),

    # Quality score realistic: 60–100
    "quality_score": np.random.normal(88, 10, NUM_ROWS).clip(50, 100),

    # Lineage confidence realistic: 50–100
    "lineage_confidence": np.random.normal(85, 12, NUM_ROWS).clip(40, 100),

    # Risk score: skewed so ~12% high risk
"risk_score": np.random.choice(
    list(range(0, 100)),
    size=NUM_ROWS,
    p=[0.006]*80 + [0.02]*10 + [0.032]*10   # corrected to sum to 1.00
),

    # AML / OFAC flags: low but realistic
    "aml_flag": np.random.choice([0, 1], size=NUM_ROWS, p=[0.92, 0.08]),
    "ofac_flag": np.random.choice([0, 1], size=NUM_ROWS, p=[0.97, 0.03]),

    # Quarter transaction dates
    "transaction_date": random_dates(START_DATE, END_DATE, NUM_ROWS)
})

# Save CSV
output_path = "data/quarter_dataset.csv"
df.to_csv(output_path, index=False)

print(f"\nGenerated dataset saved to: {output_path}\n")
print(df.head())
print(df.describe())
