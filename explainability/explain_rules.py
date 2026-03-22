def explain_rule_engine(rule_results):
    explanation = {
        "total_risk_score": rule_results.get("total_risk_score", 0),
        "fraud_decision": rule_results.get("is_fraud", False),
        "triggered_rules": [],
        "summary": ""
    }

    rules = rule_results.get("triggered_rules", [])
    
    for rule in rules:
        explanation["triggered_rules"].append({
            "rule_name": rule["rule"],
            "risk_score": rule["score"],
            "impact": classify_impact(rule["score"])
        })

    # Generate a natural language summary
    if rules:
        rule_names = [r["rule"] for r in rules]
        explanation["summary"] = f"Flagged due to: {', '.join(rule_names)}."
    else:
        explanation["summary"] = "No suspicious rules triggered."

    return explanation

def classify_impact(score):
    if score >= 40: return "🔴 High Impact"
    elif score >= 20: return "🟡 Medium Impact"
    return "🟢 Low Impact"
