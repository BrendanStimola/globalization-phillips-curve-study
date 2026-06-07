from linearmodels import IV2SLS
import pandas as pd

panel = pd.read_csv('C:/phillips_project/Data/Processed/processed_panel_data.csv')

y = panel['Infation_Rate']