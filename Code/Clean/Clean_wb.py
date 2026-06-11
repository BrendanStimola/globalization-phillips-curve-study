import pandas as pd
import wbgapi as wb

country_list = {
    "USA": "United States",
    "CAN": "Canada",
    "GBR": "United Kingdom",
    "DEU": "Germany",
    "FRA": "France",
    "ITA": "Italy",
    "ESP": "Spain",
    "NLD": "Netherlands",
    "JPN": "Japan",
    "KOR": "South Korea",
    "AUS": "Australia",
    "MEX": "Mexico",
    "VNM": "Vietnam",
    "SGP": "Singapore"
}

codes = list(country_list.keys())
names = list(country_list.values())

trade = wb.data.DataFrame('NE.TRD.GNFS.ZS', economy=codes, time=range(1990, 2025))
inflation = wb.data.DataFrame('FP.CPI.TOTL.ZG', economy=codes, time=range(1990, 2025))
unemployment = wb.data.DataFrame('SL.UEM.TOTL.ZS', economy=codes, time=range(1990, 2025))
LFPR = wb.data.DataFrame('SL.TLF.CACT.ZS', economy=codes, time=range(1990, 2025))
tariff = wb.data.DataFrame('TM.TAX.MRCH.WM.AR.ZS', economy=codes, time=range(1990, 2025))

trade = trade.reset_index()
inflation = inflation.reset_index()
unemployment = unemployment.reset_index()
LFPR = LFPR.reset_index()
tariff = tariff.reset_index()

trade = trade.melt(
    id_vars='economy',
    var_name='Year',
    value_name='Trade_GDP'
)
inflation = inflation.melt(
    id_vars='economy',
    var_name='Year',
    value_name='Inflation_Rate'
)
unemployment = unemployment.melt(
    id_vars='economy',
    var_name='Year',
    value_name='Unemployment_Rate'
)
LFPR = LFPR.melt(
    id_vars='economy',
    var_name='Year',
    value_name='LFPR'
)
tariff = tariff.melt(
    id_vars='economy',
    var_name='Year',
    value_name='Tariff_Rate'
)

trade['Year'] = trade['Year'].str.replace('YR', '').astype(int)
unemployment['Year'] = unemployment['Year'].str.replace('YR', '').astype(int)
inflation['Year'] = inflation['Year'].str.replace('YR', '').astype(int)
LFPR['Year'] = LFPR['Year'].str.replace('YR', '').astype(int)
tariff['Year'] = tariff['Year'].str.replace('YR', '').astype(int)

panel = trade.merge(inflation, on=['economy', 'Year'], how='left').merge(unemployment, on=['economy', 'Year'], how='left').merge(LFPR, on=['economy', 'Year'], how='left').merge(tariff, on=['economy', 'Year'], how='left')

panel = panel.sort_values(['economy', 'Year'])

panel['Unemployment_Rate_Lag'] = (
    panel.groupby('economy')['Unemployment_Rate']
         .shift(1)
)

panel['Trade_GDP_Lag'] = (
    panel.groupby('economy')['Trade_GDP']
         .shift(1)
)

panel['Inflation_Lagged'] = (
    panel.groupby('economy')['Inflation_Rate']
    .shift(1)
)

panel['economy'] = panel['economy'].map(country_list)
panel['POST_WTO'] = (panel['Year'] >= 2001).astype(int)
panel['Interaction'] = panel['POST_WTO'] * panel['Unemployment_Rate'] * panel['Trade_GDP']

panel = panel.rename(columns={'economy': 'Countries', 'time': 'Year', 'NE.TRD.GNFS.ZS': 'Trade_GDP_Percentage', 
'FP.CPI.TOTL.ZG': 'Inflation_Rate', 'SL.UEM.TOTL.ZS': 'Unemployment_Rate', 'Unemployment_Rate_Lag': 'Unemployment_Rate_Lag', 'SL.TLF.CACT.ZS': 'LFPR',
'Trade_GDP_Lag': 'Trade_GDP_Lag', 'TM.TAX.MRCH.WM.AR.ZS': 'Tariff_Rate', 'Inflation_Lagged': 'Inflation_Lagged'})

panel.to_csv('panel_data.csv', index=False)

panel = panel.dropna(subset=['Unemployment_Rate'])
panel = panel.dropna(subset=['Unemployment_Rate_Lag'])
panel = panel.dropna(subset=['Trade_GDP_Lag'])
panel = panel.dropna(subset=['Tariff_Rate'])
panel = panel.dropna(subset=['Inflation_Lagged'])

panel = panel.reset_index(drop=True)

print(panel.head())

panel.to_csv("C:/phillips_project/data/processed/processed_panel_data.csv", index=False)
