import os
import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations, count
from collections import Counter

#### Merge data from each month into one CSV
path = "./Sales_Data"
files = [file for file in os.listdir(path) if not file.startswith('.')] # Ignore hidden files

all_months_data = pd.DataFrame()

for file in files:
    current_data = pd.read_csv(path+"/"+file)
    all_months_data = pd.concat([all_months_data, current_data])

all_months_data.to_csv("all_data.csv", index=False)

#### Read in updated dataframe
all_data = pd.read_csv("all_data.csv")
#print(all_data.head())

### Clean up the data!
# Drop rows on NAN
nan_df = all_data[all_data.isna().any(axis=1)]
all_data = all_data.dropna(how='all')

##### Get rid of text in order date column
all_data = all_data[all_data['Order Date'].str[0:2]!='Or']
#print(all_data.head())


#### Make columns correct type
all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])

### Augment data with additional columns
#### Add month column
all_data['Month'] = all_data['Order Date'].str[0:2]
all_data['Month'] = all_data['Month'].astype('int32')
#print(all_data.head())

#### Add City column
def get_city(address):
    return address.split(",")[1].strip(" ")

def get_state(address):
    return address.split(",")[2].split(" ")[1]

all_data['City'] = all_data['Purchase Address'].apply(lambda x: f"{get_city(x)}  ({get_state(x)})")
#print(all_data.head())

#### Add Sales column
all_data['Sales'] = all_data['Quantity Ordered'].astype('int') * all_data['Price Each'].astype('float')


## Data Exploration!
#### Question 1: What was the best month for sales? How much was earned that month?
results1 =all_data.groupby(['Month']).sum()
months = range(1,13)
plt.bar(months,results1.groupby(['Month']).sum()['Sales'])
plt.xticks(months)
plt.ylabel('Sales in USD ($)')
plt.xlabel('Month number')
plt.show()


#### Question 2: What city sold the most product?
results2 = all_data.groupby(['City']).sum()
#cities = all_data ['City'].unique()
cities = [city for city, df in all_data.groupby('City')]
plt.bar(cities, results2['Sales'])
plt.xticks(cities, rotation='vertical', size = 8)
labels, location = plt. yticks()
plt.yticks(labels, (labels/1000000). astype(int)) #Scoling in million USD
plt.ylabel('Sales in million USD')
plt.xlabel('City Name')
plt.show()

"""

#### Question 3: What time should we display advertisements to maximize likelihood of customer's buying product?
#Create new column in date-time Object (DTO)
all_data['Order_Date_DTO'] = pd.to_datetime(all_data['Order Date'])
#Extraction the hours dato
all_data['Hour'] = all_data['Order_Date_DTO'].dt.hour
#Ptotting
results3 = all_data.groupby(['Hour'])['Quantity Ordered'].count()
hours = [hour for hour, df in all_data.groupby("Hour")]

plt.plot(hours, results3)
plt.xticks(hours)
plt.xlabel ('Hour')
plt.ylabel ('Number of Orders')
plt.grid()
plt.show()

"""
#### Question 4: What products are most often sold together?
#Make a new dataframe to seperate the dupticoted vatues of Order 10
new_all = all_data[all_data['Order ID'].duplicated(keep=False)]
#Jotning few products with the same Order ID into the same Line.
new_all['Product_Bundle'] = new_all.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
#Dropping the dupticote volues
df2 = new_all[['Order ID', 'Product_Bundle']].drop_duplicates()
count = Counter ()
for row in df2['Product_Bundle']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list, 2)))

for key,value in count.most_common(10):
    print(key, value)
"""


#### What product sold the most? Why do you think it sold the most?
product_group = all_data.groupby('Product')
quantity_ordered = product_group.sum()['Quantity Ordered']
#print(product_group.head(10))
keys = [pair for pair, df in product_group]
plt.bar(keys, quantity_ordered)
plt.xticks(keys, rotation='vertical', size=8)
plt.show()



