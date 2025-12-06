print("Analyzing Skincare Trends Through Sephora Review Data")
print("Members: Rithika Ravichandran, Duo Xu")

################################################
#######Reading & Preprocessing(cleaning) Data ##
################################################
'''
Python techniques used:
- 1 function for cleaning up columns 
- String Manipulation
- DataFrame filtration
'''
#your code starts here

import pandas as pd 
df_csv = pd.read_csv("product_info.csv.zip")

import matplotlib.pyplot as plt 

def clean_columns(df):
	df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
	return df

df_csv = clean_columns(df_csv)


#taking only skincare product reviews

skincare_df = df_csv[df_csv["primary_category"].str.lower() == "skincare"]
print("Skincare Products Loaded:", len(skincare_df))

################################################
#######Analysis 1 ##############################
################################################
'''
Python techniques used:
-2 for loop to iterate over skincare product records
-1 list (`ratings`) to collect rating values
-1 histogram to show rating distribution
'''
#your code starts here
ratings = []

for i in skincare_df.to_dict("records"):
    if i["rating"] == i["rating"]:
        ratings.append(i["rating"])
#rating distribution
plt.figure(figsize = (10,6))
plt.hist(ratings,bins = 10,edgecolor = 'black')
plt.title('Distribution of Skincare Product Ratings')
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.show()

#find perfect rated skincare products (rating = 5)
perfect_rated_products = []
for row in skincare_df.to_dict("records"):
    if row["rating"] == 5.0:
        product_name = row["product_name"]
        perfect_rated_products.append(product_name)
print("Skincare Products with Perfect Rating (5.0):")
for name in perfect_rated_products:
    print("-", name)


################################################
#######Analysis 2 ##############################
################################################
'''
Python techniques used:
- 1 function to calculate average price and rating 
- 1 dictionary to store brand-level data
- 1 scatter plot to show relationship between average price and average rating 
'''
#your code starts here

def brand_averages(data):
	brand_data = {}

	for row in data:
		brand = row["brand_name"]
		price = row["price_usd"]
		rating = row["rating"]

		if type(brand) == str and type(price) in [int, float] and type(rating) in [int, float]:
			if brand not in brand_data:
				brand_data[brand] = {"total_price": 0,"total_rating": 0, "count": 0}
			brand_data[brand]["total_price"] += price
			brand_data[brand]["total_rating"] += rating
			brand_data[brand]["count"] += 1

	brand_averages = {}

	for brand in brand_data:
		count = brand_data[brand]["count"]
		avg_price = brand_data[brand]["total_price"] / count
		avg_rating = brand_data[brand]["total_rating"] / count
		brand_averages[brand] = (avg_price, avg_rating)
	return brand_averages

brand_avg_data = brand_averages(skincare_df.to_dict("records"))

average_price = [price for price, rating in brand_avg_data.values()]
average_rating = [rating for price, rating in brand_avg_data.values()]


plt.figure(figsize=(10, 6))
plt.scatter(average_rating, average_price, alpha=0.5)
plt.title('Average Rating vs Average Price per Brand')
plt.xlabel('Average Rating')
plt.ylabel('Average Price')
plt.show()

################################################
#######Analysis 3 ##############################
################################################
'''
Python techniques used:
-1 dictionary to store ingredient counts
-1 for loop to extract first 10 ingredients and their counts
-1 pie chart to show ingredient distribution
'''
#your code starts here

ingredient_counts = {}
for row in skincare_df.to_dict("records"):
    if row["rating"] == 5.0:
        ingredients = row["ingredients"]
        if type(ingredients) == str:
            ingredient_list = ingredients.split(",")
            for i in ingredient_list:
                i = i.strip().lower()
                if i in ingredient_counts:
                    ingredient_counts[i] += 1
                else:
                    ingredient_counts[i] = 1

ingredient_names = []
ingredient_values = []
count = 0
for i in ingredient_counts:
    if count < 10:
        ingredient_names.append(i)
        ingredient_values.append(ingredient_counts[i])
        count += 1

plt.figure(figsize=(10, 5))
plt.pie(ingredient_values,labels = ingredient_names, autopct = '%1.1f%%')
plt.title('First 10 Ingredients in Perfect-Rated Skincare Products Distribution')
plt.show()

