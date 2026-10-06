# Model Training Notebook

## Experiment Log

| Experiment | Model | Accuracy | F1-Score | Notes |
|------------|-------|----------|----------|-------|
| Baseline | Logistic Regression | 0.76 | 0.74 | TF-IDF features |
| v2 | Random Forest | 0.83 | 0.81 | + feature engineering |
| v3 | XGBoost | 0.87 | 0.86 | tuned hyperparams |
| v4 | Sentence Transformers | 0.91 | 0.90 | semantic embeddings |

## Best Model
- **Model:** Sentence Transformers + XGBoost head
- **Accuracy:** 91%
- **Saved to:** `models/best_model.pkl`
