def combine_explanations(ml_explanation, rule_explanation, ml_weight=0.6, rule_weight=0.4):
    ml_prob = ml_explanation.get("probability", 0)
    rule_score = rule_explanation.get("total_risk_score", 0)

    # Normalize rule score
    normalized_rule_score = min(rule_score / 100, 1.0)

    # Weighted final score
    final_score = (ml_prob * ml_weight) + (normalized_rule_score * rule_weight)
    fraud_decision = final_score >= 0.5

    # Determine the primary driver of the decision
    if ml_prob * ml_weight > normalized_rule_score * rule_weight:
        primary_driver = "Machine Learning Model"
    else:
        primary_driver = "Rule Engine"

    return {
        "final_fraud_decision": fraud_decision,
        "final_risk_score": round(final_score, 4),
        "primary_driver": primary_driver,
        "details": {
            "ml_impact": round(ml_prob * ml_weight, 4),
            "rule_impact": round(normalized_rule_score * rule_weight, 4)
        },
        "ml_features": ml_explanation.get("top_features", []),
        "triggered_rules": rule_explanation.get("triggered_rules", [])
    }
