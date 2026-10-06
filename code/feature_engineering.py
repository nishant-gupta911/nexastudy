"""
Feature Engineering Utilities — NexaStudy
Author: Nishant Gupta | Reg: 23FE10CDS00506 | MUJ Batch F
"""

import pandas as pd
import numpy as np


def add_interaction_features(df: pd.DataFrame, col_a: str, col_b: str) -> pd.DataFrame:
    """Add multiplicative interaction feature between two columns."""
    df[f"{col_a}_x_{col_b}"] = df[col_a] * df[col_b]
    return df


def add_polynomial_features(df: pd.DataFrame, col: str, degree: int = 2) -> pd.DataFrame:
    """Add polynomial features for a numeric column."""
    for d in range(2, degree + 1):
        df[f"{col}^{d}"] = df[col] ** d
    return df


def bin_numeric(df: pd.DataFrame, col: str, bins: int = 5, labels=None) -> pd.DataFrame:
    """Bin a numeric column into equal-width buckets."""
    df[f"{col}_bin"] = pd.cut(df[col], bins=bins, labels=labels)
    return df


def log_transform(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Apply log1p transform to reduce skewness."""
    df[f"{col}_log"] = np.log1p(df[col].clip(lower=0))
    return df
