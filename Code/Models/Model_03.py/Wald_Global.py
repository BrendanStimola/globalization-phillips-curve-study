import numpy as np
import pandas as pd
import statsmodels.api as sm

# =========================================================
# 1. DATA PREPARATION
# =========================================================

panel = pd.read_csv("C:/phillips_project/data/processed/processed_panel_data.csv")

# Create post-2001 dummy (WTO break)
panel["u_post"] = panel["Unemployment_Rate"] * panel["POST_WTO"]

panel = panel.dropna(subset=["Inflation_Rate"])
# =========================================================
# 2. MODEL 1 (FULL STRUCTURAL PHILLIPS CURVE)
# =========================================================

X = panel[[
    "Unemployment_Rate",
    "Trade_GDP",
    "Interaction",
    "u_post"
]]

X = sm.add_constant(X)
y = panel["Inflation_Rate"]

# =========================================================
# 3. ESTIMATE MODEL WITH HAC (NEW KEY STEP)
# =========================================================

model = sm.OLS(y, X).fit(cov_kwds={"maxlags": 1, "cov_type": "HAC"})

print(model.summary2())

# =========================================================
# 4. WALD TESTS
# =========================================================

# (A) Test slope change only (Phillips Curve change)
wald_slope = model.t_test("u_post = 0")
print("\nWald test (slope change - u_post = 0):")
print(wald_slope)

# (B) Test full structural break (level + slope change)
wald_full = model.f_test("""
u_post = 0
""")

print("\nWald test (full structural break):")
print(wald_full)

# =========================================================
# 5. SIMPLE INTERPRETATION HELPER
# =========================================================

if wald_full.pvalue < 0.05:
    print("\nResult: Evidence of structural break after 2001")
else:
    print("\nResult: No statistically significant structural break detected")