import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, '..', 'data', 'cleaned_openrent.csv') 

df = pd.read_csv(data_path)  

print(df.head())

plt.figure(figsize=(8, 5))
sns.histplot(df['rent'], kde=True, bins=30)
plt.title('Distribution of Rent Prices')
plt.xlabel('Rent (£)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig(os.path.join(base_dir, '..', 'plots', 'rent_distribution.png'))
plt.show()

plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x='squareft', y='rent')
plt.title('Rent vs. Square Footage')
plt.xlabel('Square Footage')
plt.ylabel('Rent (£)')
plt.tight_layout()
plt.savefig(os.path.join(base_dir, '..', 'plots', 'rent_vs_squareft.png'))
plt.show()

if 'postcode_area' in df.columns:
    avg_rent = df.groupby('postcode_area')['rent'].mean().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=avg_rent.index, y=avg_rent.values)
    plt.title('Average Rent by Postcode Area')
    plt.xlabel('Postcode Area')
    plt.ylabel('Average Rent (£)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(base_dir, '..', 'plots', 'avg_rent_by_postcode.png'))
    plt.show()
