#!/usr/bin/env python3
import sys
import re
import operator
import csv

#Open file and return a list of lines. Not safe for large files.
def parse_lines(file_location):
	with open(file_location, "r") as file:
		return file.readlines()

#Takes a list of files and returns a list of match objects based on the search string.
def tokenize(lines):
	token_list = []
	for line in lines:
		tokens =  re.search(r"ticky: (ERROR|INFO)([\w ]*)\[?#?\d?\d?\d?\d?\]? \((.*)\)", line)
		if tokens is not None:
			token_list.append(tokens)
	return(token_list)

#Takes a list of items and returns a dictionary with each unique item as a key and the appearance count as value.
def count_list_to_dict(list):
	count_dict = dict()
	for item in list:
		count_dict[item] = count_dict.get(item, 0) + 1
	return count_dict

#Takes a token list and returns a sorted list with headers ready to be converted to .csv of errors by count.
def count_errors(token_list):
	error_list = []
	for token in token_list:
		if token[1] == "ERROR":
			error_list.append(token[2].strip())
	error_count = count_list_to_dict(error_list)
	sorted_errors = sorted(error_count.items(), key = operator.itemgetter(1), reverse=True)
	sorted_errors = [("Error", "Count")] + sorted_errors

	return sorted_errors

#Creates a list of actions by user
def count_actions_by_user(token_list):
	user_list = {}
	for token in token_list:
		if token[3] not in user_list:
			user_list[token[3]] = [0,0]
		if token[1] == "INFO":
			user_list[token[3]][0] = user_list[token[3]][0] + 1
		if token[1] == "ERROR":
			user_list[token[3]][1] = user_list[token[3]][1] + 1
	sorted_actions = sorted(user_list.items())
	list_for_csv = [["User", "Info", "Error"]]
	for i in range(len(sorted_actions)):
		list_for_csv = list_for_csv + [[sorted_actions[i][0], sorted_actions[i][1][0], sorted_actions[i][1][1]]]
	return list_for_csv

#Writes out a .csv from a given list
def write_csv(file_name, contents):
	with open("{}.csv".format(file_name), "w") as file:
		writer = csv.writer(file)
		writer.writerows(contents)

#main
if __name__ == '__main__':
	lines = parse_lines(sys.argv[1])
	tokens = tokenize(lines)
	errors = count_errors(tokens)
	print("Overwriting Errors.csv")
	write_csv("Errors", errors)
	actions = count_actions_by_user(tokens)
	print("Overwriting Users.csv")
	write_csv("Users", actions)
