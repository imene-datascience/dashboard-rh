import pandas as pd
import numpy as np

df = pd.read_csv('C:/Users/imene/dashboard-rh/data/WA_Fn-UseC_-HR-Employee-Attrition.csv')

# ── Nettoyage de base ──
df['Attrition_Num'] = (df['Attrition'] == 'Yes').astype(int)
df.drop(['EmployeeCount', 'Over18', 'StandardHours'], axis=1, inplace=True, errors='ignore')

# ── Tranches d'âge ──
df['TrancheAge'] = pd.cut(
    df['Age'],
    bins=[17, 25, 35, 45, 60],
    labels=['18-25', '26-35', '36-45', '46-60'],
    include_lowest=True
)
df['TrancheAge_Ordre'] = df['TrancheAge'].astype(str).map(
    {'18-25': 1, '26-35': 2, '36-45': 3, '46-60': 4}
).astype('Int64')

# ── Séniorité ──
df['Seniority'] = pd.cut(
    df['YearsAtCompany'],
    bins=[-1, 2, 5, 10, np.inf],
    labels=['Nouveau', 'Junior', 'Confirmé', 'Senior'],
    include_lowest=True
)
df['Seniority_Ordre'] = df['Seniority'].astype(str).map(
    {'Nouveau': 1, 'Junior': 2, 'Confirmé': 3, 'Senior': 4}
).astype('Int64')

# ── Score de risque multi-facteurs ──
df['ScoreRisque'] = (
    (df['OverTime'] == 'Yes').astype(int) * 2 +
    (df['JobSatisfaction'] <= 2).astype(int) * 2 +
    (df['YearsAtCompany'] <= 2).astype(int) * 1 +
    (df['WorkLifeBalance'] <= 2).astype(int) * 2 +
    (df['MonthlyIncome'] < df['MonthlyIncome'].quantile(0.25)).astype(int) * 1
)

df['RisqueAttrition'] = pd.cut(
    df['ScoreRisque'],
    bins=[-1, 1, 4, 10],
    labels=['Faible', 'Moyen', 'Élevé'],
    include_lowest=True
)

# ── Vérifications ──
print("\n=== TrancheAge_Ordre ===")
print(df[['Age', 'TrancheAge', 'TrancheAge_Ordre']].head(10))
print("\n=== Seniority_Ordre ===")
print(df[['YearsAtCompany', 'Seniority', 'Seniority_Ordre']].head(10))
print("\n=== Distribution RisqueAttrition ===")
print(df['RisqueAttrition'].value_counts())

# ── Export ──
df.to_csv('C:/Users/imene/dashboard-rh/data/hr_clean.csv', index=False)
print(f"\n✅ Nettoyage terminé : {df.shape[0]} lignes, {df.shape[1]} colonnes")