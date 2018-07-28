#!/usr/bin/python
import os

# Finds the file of properties and returns a list of values read from the file
def read_file_into_list(file_name):
	# If file not found, returns an empty list
	if not os.path.isfile(file_name):
		values = []
	else:
		# Read the file into list and remove any empty values
		with open(file_name, "r") as f:
		values = f.read()
		values = values.split("\n")
		values = list(filter(None, values))
	return values

# Write a list into a file
def write_list_into_file(list, file_name):
	with open(file_name, "w") as f:
		for item in list:
			f.write(item + "\n")
