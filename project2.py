import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("NY-House-Dataset.csv")


#ANALYSIS PLOTS FROM HERE
#1 PLOT FOR THE HOUSE PRICES ( BOX PLOT - HARSHVARDHAN )
areas = {
    'New York County': 'Manhattan',
    'Kings County': 'Brooklyn',
    'Queens County': 'Queens',
    'Bronx County': 'The Bronx',
    'Richmond County': 'Staten Island'
}

df_clean = df[df['ADMINISTRATIVE_AREA_LEVEL_2'].isin(areas.keys())].copy()
df_clean['Borough'] = df_clean['ADMINISTRATIVE_AREA_LEVEL_2'].map(areas)
plt.figure(figsize=(12, 8))
sns.set_theme(style="whitegrid")

sns.boxenplot(
    data=df_clean, 
    x="PRICE", 
    y="Borough", 
    palette="coolwarm", 
    order=['Manhattan', 'Brooklyn', 'Queens', 'Staten Island', 'The Bronx']
)
plt.xscale('log')

plt.title('Price Distribution by Borough (Box Plot)', fontsize=16, fontweight='bold')
plt.xlabel('Price (Log Scale)')
plt.ylabel('')
plt.show()


#2 Scatter Plot

#3 BOX PLOT 2

#4 CORELATION PLOT

#5 REQUIRED INCOME

# Clean PRICE column (remove commas, $, text)
if df["PRICE"].dtype == "object":
    df["PRICE"] = (
        df["PRICE"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
df["PRICE"] = pd.to_numeric(df["PRICE"], errors="coerce")

df = df.dropna(subset=["PRICE", "LOCALITY"])


top_localities = df["LOCALITY"].value_counts().head(10).index
df_loc_top = df[df["LOCALITY"].isin(top_localities)]

interest_rate = 0.07       
loan_term = 30           
down_payment = 0.20      
max_ratio = 0.28         

monthly_rate = interest_rate / 12
n_payments = loan_term * 12

afford_data = []

for locality, group in df_loc_top.groupby("LOCALITY"):
    median_price = group["PRICE"].median()
    if pd.isna(median_price):
        continue

    loan_amount = median_price * (1 - down_payment)

    mortgage_payment = loan_amount * (
        (monthly_rate * (1 + monthly_rate) ** n_payments) /
        ((1 + monthly_rate) ** n_payments - 1)
    )

    required_annual_income = (mortgage_payment / max_ratio) * 12

    afford_data.append({
        "LOCALITY": locality,
        "MedianPrice": median_price,
        "RequiredAnnualIncome": required_annual_income
    })

aff_df = pd.DataFrame(afford_data)

plt.figure(figsize=(12, 6))
sns.barplot(
    data=aff_df.sort_values("RequiredAnnualIncome", ascending=False),
    x="LOCALITY",
    y="RequiredAnnualIncome"
)
plt.title("Annual Income Needed to Afford Median Home (Top 10 Localities)")
plt.xlabel("Locality")
plt.ylabel("Required Annual Income ($)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print("\nRequired Annual Income Only:\n")
print(aff_df["RequiredAnnualIncome"])
