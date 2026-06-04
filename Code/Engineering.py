import pandas as pd

# 1. Load data
panel = pd.read_csv("C:/phillips_project/data/processed_panel_data.csv")

# 2. Create inflation gap

panel["inflation_mean"] = panel.groupby("Countries")["Inflation_Rate"].transform("mean")

panel["Inflation_gap"] = panel["Inflation_Rate"] - panel["Inflation_mean"]

print(panel.head())