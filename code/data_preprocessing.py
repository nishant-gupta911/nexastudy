"""
Data Preprocessing Utilities — NexaStudy
Author: Nishant Gupta | Reg: 23FE10CDS00506 | MUJ Batch F
"""

import pandas as pd
import numpy as np
from pathlib import Path


def load_dataset(path: str) -> pd.DataFrame:
    """Load CSV or Excel dataset from given path."""
    p = Path(path)
    if p.suffix == ".csv":
        return pd.read_csv(p)
    elif p.suffix in (".xlsx", ".xls"):
        return pd.read_excel(p)
    raise ValueError(f"Unsupported file type: {p.suffix}")


def drop_high_null_columns(df: pd.DataFrame, threshold: float = 0.4) -> pd.DataFrame:
    """Drop columns with more than `threshold` fraction of nulls."""
    null_frac = df.isnull().mean()
    to_drop = null_frac[null_frac > threshold].index.tolist()
    print(f"Dropping {len(to_drop)} columns: {to_drop}")
    return df.drop(columns=to_drop)


def impute_numeric(df: pd.DataFrame, strategy: str = "median") -> pd.DataFrame:
    """Impute missing numeric values with mean or median."""
    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        if df[col].isnull().any():
            fill_val = df[col].median() if strategy == "median" else df[col].mean()
            df[col] = df[col].fillna(fill_val)
    return df


def encode_categoricals(df: pd.DataFrame) -> pd.DataFrame:
    """Label-encode all object columns."""
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = le.fit_transform(df[col].astype(str))
    return df


def split_features_target(df: pd.DataFrame, target_col: str):
    """Split DataFrame into features X and target y."""
    X = df.drop(columns=[target_col])
    y = df[target_col]
    return X, y
