def run_playbook(context, df):
    logs = []
    logs.append(f"Executing playbook for: {context}")
    logs.append(f"Record count: {len(df)}")

    if context == "FraudReview":
        logs.append("Validating fraud risk scoring...")
        logs.append("Checking high-risk transaction thresholds...")

    elif context == "CreditDecision":
        logs.append("Validating credit inputs and data completeness...")

    elif context == "AMLReport":
        logs.append("Checking AML flags, OFAC matches, lineage levels...")

    logs.append("Playbook successfully completed.")

    return {
        "status": "COMPLETED",
        "logs": logs
    }
