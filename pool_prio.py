import csv
import getopt
import sys
import argparse
import random

pitch_list = []

class product: 
	def __init__(self, name, funded, actual):
		self.name = name
		self.funded = funded
		self.actual = 1.0 * actual

	def pitch(self):
		self.actual = self.actual + 0.5
		pitch_list.append(self.name)	

	def prio(self):
        # added the random thing to not allow initial ordering of products withion the file to determine the pitching order if prios are equal
		return (1.0 * (self.funded - self.actual) / self.funded) + (random.random() * 0.01)
		

	def __str__(self):
		return "Product [name={}, funded={}, actual={}, prio={}]".format(self.name, self.funded, self.actual, self.prio())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--products')
    parser.add_argument('-n', '--newbees')
    args = parser.parse_args()
    products = []
    newbees = []
    if (not args.products) or (not args.newbees):
        print "Usage: {} -p[products.csv] -n[newbees.csv]".format(__file__)
        exit(2)
    try:
        with open(args.products , "r") as product_file:
            reader = csv.reader(product_file, delimiter=',', quotechar='"')
            for line in reader:
                products.append(product(line[0], int(line[1]), int(line[2])))
    except IOError:
        print "Could not open product file: {}.".format(args.products, sys.exc_info())    
        exit(2)
    try:
        with open(args.newbees , "r") as newbee_file:
            reader = csv.reader(newbee_file, delimiter=',', quotechar='"')
            for line in reader:
                newbees.append(line[0])
    except IOError:
        print "Could not open newbees file: {}.".format(args.newbees)    
        exit(2)

    if len(newbees) > 0:
        for i in range(0, (len(newbees) * 2) + 5):
            products_allowed_to_pitch = [product for product in products if product.funded > product.actual]
            sorted_products = sorted(products_allowed_to_pitch, key=lambda product: -product.prio())
            if len(sorted_products) > 0:
                sorted_products[0].pitch()

    print pitch_list
