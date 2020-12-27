#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import collections
import operator
""" This is a collection of scripts used to clean up malformed patent data. USPTO data is extremely messy and therefore needs several customized cleanup functions
Note that this is more of a data exploration file and therefore has a lot of hard-coded filenames. For demo only.
"""

def fix_malformed_locations():
    '''malformed_1: Location is CA, malformed_2: Location is ), malformed_3: Assignee malformed '''
    malformed_count_1=0
    malformed_count_2=0
    malformed_count_3=0
    full_count=0
    clean_count=0
    row_header = ["Number","Title","Date","FiledDate","Assignee","Location","Class","Abstract"]
    with open('patent_data.csv', 'rU') as read_file:
        csv_reader = csv.reader(read_file, delimiter=',', quotechar='"')
        for row in csv_reader:
            full_count+=1
            row_dict = dict(zip(row_header, row))     
            if row_dict['Location'] == "CA":                
                malformed_count_1+=1
                with open('malformed_1.csv', 'a+') as write_file:
                    csv_writer = csv.writer(write_file, quoting=csv.QUOTE_ALL)
                    csv_writer.writerow(row)                    
            elif row_dict['Location'] == ")":            
                malformed_count_2+=1
                with open('malformed_2.csv', 'a+') as write_file:
                    csv_writer = csv.writer(write_file, quoting=csv.QUOTE_ALL)
                    csv_writer.writerow(row)
            elif row_dict['Assignee'] == ")":                
                malformed_count_3+=1
                with open('malformed_3.csv', 'a+') as write_file:
                    csv_writer = csv.writer(write_file, quoting=csv.QUOTE_ALL)
                    csv_writer.writerow(row)
            else:
                clean_count+=1
                with open('clean.csv', 'a+') as write_file:
                    csv_writer = csv.writer(write_file, quoting=csv.QUOTE_ALL)
                    csv_writer.writerow(row)

        print malformed_count_1, malformed_count_2, malformed_count_3, clean_count, full_count

def fix_malformed_date():
    '''malformed_B1: rows where Date has an asterisk, malformed B2: rows where location is unknown'''
    malformed_count_B1 = 0
    malformed_count_B2 = 0
    full_count=0
    clean_count=0
    row_header = ["Number","Title","Date","FiledDate","Assignee","Location","Class","Abstract"]
    with open('patent_data_w_header_3.csv', 'rU') as read_file:
        csv_reader = csv.reader(read_file, delimiter=',', quotechar='"')
        for row in csv_reader:
            full_count+=1
            row_dict = dict(zip(row_header, row))
            if row_dict['Date'].startswith("*"):                
                malformed_count_B1 += 1
                with open('malformed_B1.csv', 'a+') as write_file:
                    csv_writer = csv.writer(write_file, quoting=csv.QUOTE_ALL)
                    csv_writer.writerow(row)                    
            elif row_dict['Location'] == "":
                malformed_count_B2 += 1
                with open('malformed_B2.csv', 'a+') as write_file:
                    csv_writer = csv.writer(write_file, quoting=csv.QUOTE_ALL)
                    csv_writer.writerow(row)
            else:
                clean_count+=1
                with open('clean_B.csv', 'a+') as write_file:
                    csv_writer = csv.writer(write_file, quoting=csv.QUOTE_ALL)
                    csv_writer.writerow(row)
           
        print malformed_count_B1, malformed_count_B2, clean_count, full_count    

def print_patents_with_unknown_locations():
    '''prints out assignee column of the patents with unknown locations'''
    
    assignee_set = set ()

    with open('malformed_B2a.csv', 'rU') as read_file:
        csv_reader = csv.reader(read_file, delimiter=',', quotechar='"')
        for row in csv_reader:
            assignee_set.add(row[4])
    for item in assignee_set:
        print item

def guess_unknown_location():
    '''Checks the ~2500 assignees with unknown locations against the assignees with known locations and returns the most frequent one'''
    with open('unknown_assignees', 'rU') as read_file:
        unknown_assignees = read_file.read().splitlines()
    
    assignee_dict = collections.defaultdict(dict)
    for assignee in unknown_assignees:
        assignee_dict[assignee] = {}
    with open('clean_B01.csv', 'rU') as read_file:
        csv_reader = csv.reader(read_file, delimiter=',', quotechar='"')
        for row in csv_reader:
            if row[4] in unknown_assignees:
                if row[5] not in assignee_dict[row[4]]:
                    assignee_dict[row[4]][row[5]] = 1
                else:
                    current_count = assignee_dict[row[4]][row[5]]
                    assignee_dict[row[4]][row[5]] = 1 + current_count
    would_be_fixed = 0
    with open('malformed_B2a.csv', 'rU') as read_file:
        csv_reader = csv.reader(read_file, delimiter=',', quotechar='"')
        for row in csv_reader:
            if row[4] in assignee_dict:
                if len(assignee_dict[row[4]]):
                    would_be_fixed += 1
    print "Would be fixed ", would_be_fixed
    
    fixed_counts = 0 
    still_broken_count = 0
    no_choice_count = 0
    for key in assignee_dict:
        if assignee_dict[key]:
            if len(assignee_dict[key]) == 1:
                no_choice_count += 1
                print no_choice_count,key, assignee_dict[key]
                with open('no_choice_assignees.csv', 'a+') as write_file:
                    csv_writer = csv.writer(write_file, quoting=csv.QUOTE_ALL)
                    csv_writer.writerow([key,next(iter(assignee_dict[key]))]) 
            else:
                fixed_counts += 1
        else:
            still_broken_count += 1
    print "No choice: ",no_choice_count, "Fixed: ",fixed_counts," StillBroken: ",still_broken_count, " len: ",len(unknown_assignees)

def generate_location_frequency_dict():
    '''Checks the entire list assignees with known locations and compiles a frequency dictionary'''
    with open('known_assignees', 'rU') as read_file:
        known_assignees = read_file.read().splitlines()
    
    assignee_dict = collections.defaultdict(dict)
    for assignee in known_assignees:
        assignee_dict[assignee] = {}
    with open('clean_B01.csv', 'rU') as read_file:
        csv_reader = csv.reader(read_file, delimiter=',', quotechar='"')
        for row in csv_reader:
            if row[4] in known_assignees:
                if row[5] not in assignee_dict[row[4]]:
                    assignee_dict[row[4]][row[5]] = 1
                else:
                    current_count = assignee_dict[row[4]][row[5]]
                    assignee_dict[row[4]][row[5]] = 1 + current_count
    
    fixed_counts = 0 
    still_broken_count = 0
    no_choice_count = 0
    for key in assignee_dict:
        if assignee_dict[key]:
            if len(assignee_dict[key]) == 1:
                no_choice_count += 1
            else:
                fixed_counts += 1
            print key, assignee_dict[key]
        else:
            still_broken_count += 1
    print "No choice: ",no_choice_count, "Fixed: ",fixed_counts," StillBroken: ",still_broken_count, " len: ",len(known_assignees)

def create_all_assignees():
    '''Checks the entire list of assignees and compiles a frequency dictionary, excluding empties'''
    
    assignee_set = set ()

    with open('patent_C.csv', 'rU') as read_file:
        csv_reader = csv.reader(read_file, delimiter=',', quotechar='"')
        for row in csv_reader:
            assignee_set.add(row[4])
    for item in assignee_set:
        print item

def create_dictionary_of_assignee_locations():
    with open('all_assignees', 'rU') as read_file:
        all_assignees = read_file.read().splitlines()
    assignee_dict = collections.defaultdict(dict)
    for assignee in all_assignees:
        assignee_dict[assignee] = {}
    with open('patent_C.csv', 'rU') as read_file:
        csv_reader = csv.reader(read_file, delimiter=',', quotechar='"')
        for row in csv_reader:
            if row[4] in all_assignees:
                if row[5]:
                    if row[5] not in assignee_dict[row[4]]:
                        assignee_dict[row[4]][row[5]] = 1
                    else:
                        current_count = assignee_dict[row[4]][row[5]]
                        assignee_dict[row[4]][row[5]] = 1 + current_count
    for key in assignee_dict:
        print key, assignee_dict[key] 
    

def main():
    create_dictionary_of_assignee_locations()
main()
