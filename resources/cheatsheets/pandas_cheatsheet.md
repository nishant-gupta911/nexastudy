# Pandas Quick Reference

```python
import pandas as pd

# Load
df = pd.read_csv("file.csv")

# Explore
df.head(), df.shape, df.info(), df.describe()
df.isnull().sum()

# Select
df["col"], df[["a","b"]], df.iloc[0:5], df.loc[df["col"] > 0]

# Transform
df["new"] = df["a"] + df["b"]
df.groupby("col").agg({"val": "mean"})
df.merge(df2, on="key", how="left")

# Clean
df.dropna(), df.fillna(0), df.drop_duplicates()
df["col"] = df["col"].astype(int)
```
