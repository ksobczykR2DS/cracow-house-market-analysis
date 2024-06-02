import pandas as pd

file_path = 'model_results.csv'
results_df = pd.read_csv(file_path)

numeric_columns = ['MAE', 'RMSE', 'R2', 'Measure_10%', 'Measure_20%']
results_df[numeric_columns] = results_df[numeric_columns].round(4)

model_names = {
    'LR': 'Linear Regression (LR)',
    'DT': 'Decision Tree (DT)',
    'GBM': 'Gradient Boosting Machine (GBM)',
    'LGB': 'LightGBM (LGB)',
    'RF': 'Random Forest (RF)',
    'XGB': 'XGBoost (XGB)',
    'CBR': 'CatBoost Regressor (CBR)',
    'Super Model (Average of GBM, LGB, XGB, CBR)': 'Super GB Model',
    'Weighted Super-GB (Optimized Weights of XGB, LGB, GBM)': 'Weighted Super-GB'
}

# Zamiana nazw modeli
results_df['Model'] = results_df['Model'].map(model_names)

# Sortowanie według wartości R2
results_df = results_df.sort_values(by='R2')

# Znalezienie najlepszych wyników dla każdej metryki
best_mae = results_df['MAE'].min()
best_rmse = results_df['RMSE'].min()
best_r2 = results_df['R2'].max()
best_measure_10 = results_df['Measure_10%'].max()
best_measure_20 = results_df['Measure_20%'].max()

# Pogrubienie najlepszych wyników
def highlight_best(value, best_value):
    return f"\\textbf{{{value}}}" if value == best_value else f"{value}"

# Obliczenie średnich wartości metryk dla modeli wzmacniania gradientowego (GBM, LGB, XGB, CBR)
gb_models = ['Gradient Boosting Machine (GBM)', 'LightGBM (LGB)', 'XGBoost (XGB)', 'CatBoost Regressor (CBR)']
mean_values = results_df[results_df['Model'].isin(gb_models)][numeric_columns].mean()

# Tworzenie wiersza z średnimi wartościami metryk
mean_row = pd.DataFrame({
    'Model': ['Mean (GB models)'],
    'MAE': [mean_values['MAE']],
    'RMSE': [mean_values['RMSE']],
    'R2': [mean_values['R2']],
    'Measure_10%': [mean_values['Measure_10%']],
    'Measure_20%': [mean_values['Measure_20%']]
})

results_df['MAE'] = results_df['MAE'].apply(lambda x: highlight_best(x, best_mae))
results_df['RMSE'] = results_df['RMSE'].apply(lambda x: highlight_best(x, best_rmse))
results_df['R2'] = results_df['R2'].apply(lambda x: highlight_best(x, best_r2))
results_df['Measure_10%'] = results_df['Measure_10%'].apply(lambda x: highlight_best(x, best_measure_10))
results_df['Measure_20%'] = results_df['Measure_20%'].apply(lambda x: highlight_best(x, best_measure_20))

# Dodanie wiersza do DataFrame
results_df = pd.concat([results_df, mean_row], ignore_index=True)

# Generowanie tabeli w formacie LaTeX
latex_table = results_df.to_latex(index=False, escape=False)

# Zapisanie tabeli LaTeX do pliku
with open('model_results_table.tex', 'w') as f:
    f.write(latex_table)

print(latex_table)
