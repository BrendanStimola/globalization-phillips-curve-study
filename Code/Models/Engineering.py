import pandas as pd
import pyfixest as fe

"""
Feature Engineering

Purpose:
    Creates inflation gap for each country.

Created Variables:
    - inflation_gap: Difference between actual inflation rate and mean inflation rate for each country.
    - inflation_mean: Mean inflation rate for each country.
"""

# 1. Load data
panel = pd.read_csv("C:/phillips_project/data/processed/processed_panel_data.csv")

# 2. Create inflation gap

panel["Inflation_mean"] = panel.groupby("Countries")["Inflation_Rate"].transform("mean")

panel["Inflation_gap"] = panel["Inflation_Rate"] - panel["Inflation_mean"]

print(panel.head())

print("Starting fixed effects regression...")

model = fe.feols(
    "Inflation_Rate ~ Interaction + Trade_GDP + Unemployment_Rate | Countries + Year",
    data=panel
)

print("Model fitted. Summary:")

print(model.summary())