import pandas as pd

df = pd.read_csv('data/WA_Fn-UseC_-HR-Employee-Attrition.csv')

print("=== Dimensions ===")
print(df.shape)

print("\n=== Taux d'attrition ===")
print(df['Attrition'].value_counts())
print(f"=> {df['Attrition'].value_counts(normalize=True)['Yes']*100:.1f}% des employés ont quitté")

print("\n=== Aperçu des colonnes ===")
print(df.dtypes)
