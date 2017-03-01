import csv
import bisect
import operator

tote_length = 45
tote_width = 30
tote_height = 35
tote_capacity = tote_length*tote_width*tote_height
sorted_tote_dimensions = [30, 35, 45]

#check if individual product fit into the tote. 
def is_fit(length, width, height, volume):
	sorted_product_dimensions = sorted([length, width, height])

	if all(i <= j for (i, j) in zip(sorted_product_dimensions, sorted_tote_dimensions)):
		return True
	else:
		return False

'''
This function helps to reduce the search range and running time drammatically. We find the possible max_no_products 
(maximum number of products) the tote can contain, which is equal to tote_capacity/min_volume (min_volume is the 
volume of the smallest-size product). We then shortlist only the product which has less than n other better products 
(n = max_no_products). The better criteria is defined as SMALLER VOLUME and HIGHER PRICE.
'''
def find_shortlist(items):
	items = sorted(items, key = operator.itemgetter('volume', 'price'))
	min_volume = items[0]['volume']
	max_no_products = tote_capacity/min_volume

	shortlist_items = []
	for item in items:
		no_better_products = 0
		for shortlist_item in shortlist_items:
			if item['price'] < shortlist_item['price']:
				no_better_products = no_better_products + 1

		if no_better_products < max_no_products:
			shortlist_items.append(item)

	return shortlist_items

#find optimal combination (max total prices) of products that can be put into the tote using dynamic programming
def find_optimal_product_combination(items):
	combinations = {tote_capacity: {'productIDs': (), 'total_price': 0, 'total_weight': 0}}
	sorted_combinations_keys = [tote_capacity] 
	optimal_combination = combinations[tote_capacity] 

	for i in range(0, len(items)):
		item_ID, item_price, item_volume, item_weight = items[i]['productID'], items[i]['price'], items[i]['volume'], items[i]['weight']

		for j in sorted_combinations_keys:
			v = j - item_volume

			if v >= 0:
				p = item_price + combinations[j]['total_price']
				w = item_weight + combinations[j]['total_weight']

				update = False
				if v not in combinations:
					bisect.insort(sorted_combinations_keys, v)
					update = True

				else:
					if p > combinations[v]['total_price'] or (p == combinations[v]['total_price'] and w < combinations[v]['total_weight']):
						update = True

				if update:
					IDs = combinations[j]['productIDs'] + (item_ID,)
					combinations[v] = {'productIDs': IDs, 'total_price': p, 'total_weight': w}					

					# update best combination of product
					if p > optimal_combination['total_price'] or (p == optimal_combination['total_price'] and w < optimal_combination['total_weight']):
						optimal_combination = combinations[v]
					
	return optimal_combination

#read data from the csv file and get the list of items
items = []
with open('products.csv', 'rb') as f:
	reader = csv.reader(f)
	for row in reader:
		data = [int(s) for s in row]
		productID, price, length, width, height, weight = data
		volume = length*width*height

		if is_fit(length, width, height, volume):
			item = {'productID': productID, 'price': price, 'volume': volume, 'weight': weight}
			items.append(item)

#reduce the search range and find best product combination using dynamic programming
shortlist_items = find_shortlist(items)
optimal_combination = find_optimal_product_combination(shortlist_items)

#calculate the sum of product IDs of all the products 
sum_IDs = 0
for ID in optimal_combination['productIDs']:
	sum_IDs = sum_IDs + ID
print(sum_IDs)