import pandas as pd
import statsmodels.api as sm
import numpy as np

"""
Global Phillips Curve Model with Lagged Inflation

Purpose:
    Estimates whether globalization changes the relationship
    between unemployment and inflation.

Model Includes:
    - Unemployment rate
    - Trade openness
    - Unemployment × Trade interaction
    - Lagged inflation

Method:
    OLS regression with HAC standard errors.

Goal:
    Test whether trade openness alters the slope
    of the Phillips Curve.
"""

panel = pd.read_csv("C:/phillips_project/data/processed/processed_panel_data.csv")

def inputs():
  print("OLS regression model (1954-2026)")
  while True:
    try:
      input_1 = int(input("Enter start year: (From 1954 to 2025)"))
      if input_1 < 1954 or input_1 > 2025:
        print("Invalid date. Start year must be between 1954 and 2025. Please retry.")
      else:
        break
    except ValueError:
      print("Invalid input. Please enter a number for the start year. Please retry.")

  while True:
    try:
      input_2 = int(input("Enter end year: (From 1955 to 2026)"))
      if input_2 > 2026 or input_2 < input_1:
        print("Invalid date. End year must be between 1955 and 2026, and not before start year. Please retry.")
      else:
        break
    except ValueError:
      print("Invalid input. Please enter a number for the end year. Please retry.")

  return input_1, input_2

input_1, input_2 = inputs()

panel = panel[panel["Year"].between(input_1, input_2)]

X = panel[["Unemployment_Rate","Trade_GDP", "Interaction", "Inflation_Lagged"]]
X = sm.add_constant(X)

y = panel["Inflation_Rate"]

model = sm.OLS(y, X).fit(
    cov_type="HAC",
    cov_kwds={"maxlags": 2}
)
print(model.summary())