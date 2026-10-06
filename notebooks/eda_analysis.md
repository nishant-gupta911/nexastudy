# EDA Analysis Notebook

> **Note:** Full notebook is in `eda_analysis.ipynb` — this is the markdown summary.

## Dataset
- Source: Kaggle public dataset
- Shape: (10,000 rows × 15 columns)

## Key Findings
- Target variable is moderately imbalanced (60/40 split)
- 3 features have >20% missing values → imputed with median
- Strong correlation between `study_hours` and `score` (r=0.82)

## Visualizations
- Distribution plots for all numerical features
- Heatmap of feature correlations
- Boxplots for outlier detection
