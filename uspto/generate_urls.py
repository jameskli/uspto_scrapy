#!/usr/bin/env python
import csv
def main():
""" Generate urls to visit using spider"""
    URL_STRING1 = 'http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r='
    URL_STRING2 = '&f=G&l=50&d=PTXT&s1=CA.ASCO.&p='
    TOTAL_PATENTS = 89523
   
    URL_STRING3 = '&OS=ACN/CA&RS=ACN/CA'
    for i in range(TOTAL_PATENTS):
        row_num = i + 1
        page_num = i // 50 + 1
        print URL_STRING1 + str(row_num) + URL_STRING2 + str(page_num) + URL_STRING3

main()