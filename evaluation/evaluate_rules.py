# evaluate_rules.py


def evaluate_rule_engine(rule_engine, transactions, true_labels):
    """
    Evaluate rule engine performance.
    """

    predictions = []

    for txn in transactions:
        result = rule_engine(txn)
        predictions.append(int(result["is_fraud"]))

    from sklearn.metrics import precision_score, recall_score, f1_score

    precision = precision_score(true_labels, predictions)
    recall = recall_score(true_labels, predictions)
    f1 = f1_score(true_labels, predictions)

    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4)
    }