import os
os.system('pip install cryptography pymysql')

import pandas as pd
import pymysql
from sqlalchemy import create_engine, text

# Creation de la base
conn_temp = pymysql.connect(host='localhost', user='root', password='Imene12345@')
conn_temp.cursor().execute('CREATE DATABASE IF NOT EXISTS hr_dashboard')
conn_temp.close()

# Connexion
engine = create_engine('mysql+pymysql://root:Imene12345%40@localhost/hr_dashboard')

# Chargement CSV
df = pd.read_csv('C:/Users/imene/dashboard-rh/data/hr_clean.csv')

# Tables
df.to_sql('faits_employes', engine, if_exists='replace', index=False)
print("Table faits_employes chargee :", len(df), "lignes")

dim_dept = df[['Department', 'JobRole']].drop_duplicates().reset_index(drop=True)
dim_dept['dept_id'] = dim_dept.index + 1
dim_dept.to_sql('dim_departement', engine, if_exists='replace', index=False)
print("Table dim_departement chargee :", len(dim_dept), "lignes")

dim_sat = df[['JobSatisfaction', 'EnvironmentSatisfaction', 'WorkLifeBalance']].drop_duplicates().reset_index(drop=True)
dim_sat.to_sql('dim_satisfaction', engine, if_exists='replace', index=False)
print("Table dim_satisfaction chargee :", len(dim_sat), "lignes")

dim_age = df[['TrancheAge', 'Seniority']].drop_duplicates().reset_index(drop=True)
dim_age.to_sql('dim_age', engine, if_exists='replace', index=False)
print("Table dim_age chargee :", len(dim_age), "lignes")

# Requetes analytiques
with engine.connect() as conn:

    print("\n=== Attrition par departement ===")
    result = conn.execute(text("""
        SELECT Department,
               COUNT(*) as nb_employes,
               ROUND(AVG(Attrition_Num)*100, 1) as taux_attrition_pct,
               ROUND(AVG(MonthlyIncome), 0) as salaire_moyen
        FROM faits_employes
        GROUP BY Department
        ORDER BY taux_attrition_pct DESC
    """))
    for row in result:
        print(f"  {row[0]} | {row[1]} employes | attrition {row[2]}% | salaire {row[3]}")

    print("\n=== Top 5 postes a risque ===")
    result = conn.execute(text("""
        SELECT JobRole,
               COUNT(*) as nb,
               ROUND(AVG(Attrition_Num)*100, 1) as taux_pct
        FROM faits_employes
        GROUP BY JobRole
        ORDER BY taux_pct DESC
        LIMIT 5
    """))
    for row in result:
        print(f"  {row[0]} | {row[2]}%")

    print("\n=== Attrition par tranche age ===")
    result = conn.execute(text("""
        SELECT TrancheAge,
               COUNT(*) as nb,
               ROUND(AVG(Attrition_Num)*100, 1) as taux_pct
        FROM faits_employes
        GROUP BY TrancheAge
        ORDER BY taux_pct DESC
    """))
    for row in result:
        print(f"  {row[0]} | {row[1]} employes | attrition {row[2]}%")

    print("\n=== Attrition par niveau de risque ===")
    result = conn.execute(text("""
        SELECT RisqueAttrition,
               COUNT(*) as nb,
               ROUND(AVG(Attrition_Num)*100, 1) as taux_pct
        FROM faits_employes
        GROUP BY RisqueAttrition
        ORDER BY taux_pct DESC
    """))
    for row in result:
        print(f"  {row[0]} | {row[1]} employes | attrition {row[2]}%")

    print("\n=== Salaire moyen par seniorite ===")
    result = conn.execute(text("""
        SELECT Seniority,
               COUNT(*) as nb,
               ROUND(AVG(MonthlyIncome), 0) as salaire_moyen,
               ROUND(AVG(Attrition_Num)*100, 1) as taux_attrition
        FROM faits_employes
        GROUP BY Seniority
        ORDER BY salaire_moyen ASC
    """))
    for row in result:
        print(f"  {row[0]} | {row[1]} emp. | salaire {row[2]} | attrition {row[3]}%")

print("\nBase MySQL hr_dashboard prete !")