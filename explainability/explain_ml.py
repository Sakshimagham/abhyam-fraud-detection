import numpy as np
import shap

def explain_ml_prediction(model, feature_vector, feature_names, top_n=5):
    """
    Explains ML model prediction using SHAP values.
    """
    # 1. Get standard prediction & probability
    prediction = model.predict([feature_vector])[0]
    probability = model.predict_proba([feature_vector])[0][1]

    # 2. Use SHAP to explain the prediction
    # TreeExplainer is best for XGBoost/RandomForest; KernelExplainer for others
    try:
        explainer = shap.Explainer(model)
        shap_values = explainer.shap_values(np.array([feature_vector]))
        
        # Handling multi-class vs binary output (class 1 is usually the focus)
        if isinstance(shap_values, list):
            current_shap = shap_values[1][0] 
        else:
            current_shap = shap_values[0]

        # 3. Sort features by absolute SHAP value (contribution strength)
        top_indices = np.argsort(np.abs(current_shap))[::-1][:top_n]

        top_features = []
        for idx in top_indices:
            top_features.append({
                "feature": feature_names[idx],
                "shap_value": round(float(current_shap[idx]), 4),
                "value": float(feature_vector[idx])
            })

        return {
            "prediction": int(prediction),
            "probability": round(probability, 4),
            "top_features": top_features,
            "base_value": float(explainer.expected_value) if hasattr(explainer, 'expected_value') else None
        }

    except Exception as e:
        return {
            "prediction": int(prediction),
            "probability": round(probability, 4),
            "explanation": f"SHAP error: {str(e)}"
        }
