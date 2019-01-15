#!/usr/bin/env python
import csv
def main_1 ():
    URL_STRING1 = 'http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r='
    
    URL_STRING3 = '&f=G&l=50&d=PTXT&s1=CA.ASCO.&p='

    #TOTAL_PATENTS = 89523
    TOTAL_PATENTS = 1094
   
    URL_STRING5 = '&OS=ACN/CA&RS=ACN/CA'
    for i in range(TOTAL_PATENTS):
        row_num = i + 1
        page_num = i // 50 + 1
        print URL_STRING1 + str(row_num) + URL_STRING3 + str(page_num) + URL_STRING5

def main_2 ():
    URL_STRING1 = 'http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=1&f=G&l=50&co1=AND&d=PTXT&s1='
    URL_STRING3 = '.PN.'

    with open('malformed_B1.csv', 'rU') as read_file:
        csv_reader = csv.reader(read_file, delimiter=',', quotechar='"')
        for row in csv_reader:
            print URL_STRING1 + row[0]  + URL_STRING3
main_1()