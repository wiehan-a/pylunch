import csv

with open("restaurants.csv") as f:
	data = csv.reader(f, delimiter=';', quotechar='\"')
	skip = True

	with open("restaurants.yaml", "w") as f:
		for row in data:
			if skip:
				skip = False
				continue
			f.write('''
- model: specials.restaurant
  fields:
    name: "%s"
    description: "%s"
    phone_number: "%s"
    location: "%s, %s"
    address: "%s"
    url: "%s"
''' % (row[1], row[-2], row[-3], row[3], row[2], row[-4], row[-1]))

