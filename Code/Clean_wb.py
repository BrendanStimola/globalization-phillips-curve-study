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

trade = trade.reset_index()
inflation = inflation.reset_index()
unemployment = unemployment.reset_index()

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


trade['Year'] = trade['Year'].str.replace('YR', '').astype(int)
unemployment['Year'] = unemployment['Year'].str.replace('YR', '').astype(int)
inflation['Year'] = inflation['Year'].str.replace('YR', '').astype(int)


panel = trade.merge(inflation, on=['economy', 'Year'], how='left').merge(unemployment, on=['economy', 'Year'], how='left')

panel['economy'] = panel['economy'].map(country_list)
panel['POST_WTO'] = (panel['Year'] >= 2001).astype(int)
panel['Interaction'] = panel['POST_WTO'] * panel['Unemployment_Rate'] * panel['Trade_GDP']

panel = panel.rename(columns={'economy': 'Countries', 'time': 'Year', 'NE.TRD.GNFS.ZS': 'Trade_GDP_Percentage', 'FP.CPI.TOTL.ZG': 'Inflation_Rate', 'SL.UEM.TOTL.ZS': 'Unemployment_Rate'})

panel.to_csv('panel_data.csv', index=False)

panel = panel.dropna(subset=['Unemployment_Rate'])
panel = panel.sort_values(by=['Countries', 'Year'])

panel = panel.reset_index(drop=True)

print(panel.head())

panel.to_csv("C:/phillips_project/data/processed/processed_panel_data.csv", index=False)