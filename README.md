# Globalization and Structural Change in the Phillips Curve

## Overview

This project studies whether globalization has changed the relationship between unemployment and inflation in the United States. Using macroeconomic data from public sources, this research estimates Phillips Curve models incorporating trade openness, inflation persistence, and structural break tests.

## Research Question

Has globalization weakened the traditional relationship between unemployment and inflation?

## Repository Structure

```
├── Data/
│   ├── Raw/
│   └── Processed/
│
|
│
├── Code/
│   ├──clean/
|   |    └─── Clean.py
|   ├── Models/
│   |    ├── US-only/
|   |    |  ├─── Wald.py
|   |    |  └─── Base-US.py
│   |    ├── inflation-lagged-global/
|   |    |  └── Inflation-Lagged-Global.py
|   |    ├── Phillips-Curve-WTO-Global
|   |    |  ├── Wald_Global.py
|   |    |  └── 2SLS.py
│   |    └── Engineering.py
|   └── plots/
│   
│
│
└── Paper/
    ├── Main.tex
    ├── References.bib
    └── Figures/
```

## Data

The project uses publicly available macroeconomic datasets including:

- Consumer Price Index (CPI)
- Unemployment Rate
- Imports and Exports
- Gross Domestic Product (GDP)

## Methods

The analysis uses:

- Ordinary Least Squares (OLS)
- HAC (Newey-West) standard errors
- Interaction models
- Structural break tests using Wald statistics
- Two-Way Fixed Effects (2WFE)
- Two-Stage Least Squares (2SLS)
- Augmented Dickey-Fuller stationarity tests

## Main Findings

The analysis finds:

- A statistically significant negative relationship between unemployment and inflation.
- Strong inflation persistence through lagged inflation.
- Limited evidence that trade openness alone affects inflation.
- Evidence that globalization may influence the unemployment-inflation relationship through interaction effects.
- No statistically significant structural break after 2001 in the US, but a break globally.

## Running the Analysis

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the scripts inside the `Code/` directory.

## Requirements

Main Python packages:

- wbgapi
- pandas
- numpy
- statsmodels
- matplotlib
- scipy
- linearmodels
- pyfixest

## Paper

The full research paper is available in:

```
Paper/Main.tex
```

## Author

Brendan Stimola

Independent Research Project  
2026
