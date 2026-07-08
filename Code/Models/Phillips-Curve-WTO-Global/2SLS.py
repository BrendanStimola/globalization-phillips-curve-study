import numpy as np
import pandas as pd
from linearmodels.iv import IV2SLS

"""
Instrumental Variables Estimation (2SLS)

Purpose:
    Estimates the Phillips Curve relationship using
    instrumental variable methods.

Method:
    Two-Stage Least Squares (2SLS)

Package:
    linearmodels.iv

Purpose:
    Address potential endogeneity concerns in the model.
"""

# -----------------------------
# LOAD + PREP DATA
# -----------------------------

panel = pd.read_csv(
    "C:/phillips_project/data/processed/processed_panel_data.csv"
)

panel["Lagged_Inflation_Rate"] = panel.groupby("Countries")["Inflation_Rate"].shift(1)
panel = panel.dropna()

# -----------------------------
# SPLIT SAMPLES
# -----------------------------

pre = panel[panel["Year"] < 2001].copy()
post = panel[panel["Year"] >= 2001].copy()

# -----------------------------
# IV FUNCTION
# -----------------------------

def run_iv(data):
    model = IV2SLS(
        dependent=data["Inflation_Rate"],
        exog=None,
        endog=data[["Unemployment_Rate", "Trade_GDP"]],
        instruments=data[
            [
                "Unemployment_Rate_Lag",
                "Trade_GDP_Lag",
                "LFPR",
                "Lagged_Inflation_Rate",
                "Tariff_Rate"
            ]
        ]
    )
    return model.fit(
        cov_type="clustered",
        clusters=data["Countries"]
    )

# -----------------------------
# ESTIMATE MODELS
# -----------------------------

pre_res = run_iv(pre)
post_res = run_iv(post)

pre_beta = pre_res.params["Unemployment_Rate"]
post_beta = post_res.params["Unemployment_Rate"]

print("\nPRE-2001 RESULTS")
print(pre_res.summary)

print("\nPOST-2001 RESULTS")
print(post_res.summary)

# -----------------------------
# WILD CLUSTER BOOTSTRAP
# -----------------------------

def wild_cluster_bootstrap(data, res, B=999):

    yhat = np.asarray(res.fitted_values).flatten()
    uhat = np.asarray(res.resids).flatten()

    clusters = data["Countries"].values
    unique_clusters = np.unique(clusters)

    boot_betas = []

    for b in range(B):

        # Rademacher weights
        weights = {
            g: np.random.choice([-1, 1])
            for g in unique_clusters
        }

        # bootstrap residuals
        u_star = np.array([
            uhat[i] * weights[clusters[i]]
            for i in range(len(data))
        ])

        # bootstrap dependent variable
        y_star = yhat + u_star

        try:
            iv_star = IV2SLS(
                dependent=y_star,
                exog=None,
                endog=data[
                    ["Unemployment_Rate", "Trade_GDP"]
                ],
                instruments=data[
                    [
                        "Unemployment_Rate_Lag",
                        "Trade_GDP_Lag",
                        "LFPR",
                        "Lagged_Inflation_Rate",
                        "Tariff_Rate"
                    ]
                ]
            )

            res_star = iv_star.fit()

            boot_betas.append(
                res_star.params["Unemployment_Rate"]
            )

        except:
            continue

    return np.array(boot_betas)

# -----------------------------
# RUN BOOTSTRAP
# -----------------------------

B = 999

pre_boot = wild_cluster_bootstrap(pre, pre_res, B=B)
post_boot = wild_cluster_bootstrap(post, post_res, B=B)

# -----------------------------
# CONFIDENCE INTERVALS
# -----------------------------

pre_ci = np.percentile(pre_boot, [2.5, 97.5])
post_ci = np.percentile(post_boot, [2.5, 97.5])

# -----------------------------
# OUTPUT
# -----------------------------

print("\n========================")
print("PRE-2001")
print("========================")
print("Beta:", pre_beta)
print("95% CI:", pre_ci)
print("Significant (0 excluded):", not (pre_ci[0] <= 0 <= pre_ci[1]))

print("\n========================")
print("POST-2001")
print("========================")
print("========================")
print("Beta:", post_beta)
print("95% CI:", post_ci)
print("Significant (0 excluded):", not (post_ci[0] <= 0 <= post_ci[1]))