# evaluate_combined.py

from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score


def evaluate_combined_system(
    model,
    rule_engine,
    X_test,
    transactions,
    y_test,
    combine_function
):
    """
    Evaluate hybrid fraud detection system.
    """

    final_predictions = []
    final_scores = []

    for i in range(len(X_test)):

        # ML part
        ml_prob = model.predict_proba([X_test[i]])[0][1]

        # Rule part
        rule_result = rule_engine(transactions[i])
        rule_score = rule_result["total_risk_score"] / 100

        # Combine
        combined_score = combine_function(ml_prob, rule_score)

        final_scores.append(combined_score)
        final_predictions.append(int(combined_score >= 0.5))

    precision = precision_score(y_test, final_predictions)
    recall = recall_score(y_test, final_predictions)
    f1 = f1_score(y_test, final_predictions)
    roc_auc = roc_auc_score(y_test, final_scores)

    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "roc_auc": round(roc_auc, 4)
    }