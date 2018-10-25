import scrapy
import os
import csv
import re
class USPTOSpider(scrapy.Spider):
    name = "uspto"
    
    def __init__(self, filename=None):
        if filename:
            with open(filename, 'r') as f:
                self.uspto_urls = [url.strip() for url in f.readlines()]


    def start_requests(self):         
        for url in self.uspto_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        patent_title = "N/A"
        patent_num = "N/A"
        patent_abstract = "N/A"
        patent_date = "N/A"
        patent_filed_date = "N/A"
        patent_assignee = "N/A"
        patent_full_assignee = "N/A"
        patent_international_class = "N/A"
        obtained_patent_filed_date = False
        
        try:
            patent_title = re.sub(' +',' ',response.xpath('/html/body/font/text()').extract()[0].rstrip().replace('\n', ' '))
        except:
            pass
        try:
            patent_abstract = re.sub(' +',' ',response.xpath ('/html/body/p[1]/text()').extract()[0].replace('\n', ' '))
        except:
            pass
        try:
            patent_num = response.xpath('/html/body/table[2]/tr[1]/td[2]//text()').extract()[0].rstrip()
        except:
            pass
        try:
            patent_date = response.xpath('/html/body/table[2]/tr[2]/td[2]/b//text()').extract()[0].lstrip().rstrip()
        except:
            pass
        try:
            temp_assignee_filed_header_list = response.xpath('/html/body/table/tr/th[@valign="top" and @align="left" and @width="10%"]//text()').extract()
            temp_assignee_filed_value_list = response.xpath('/html/body/table/tr/td[@align="left" and @width="90%"]//text()').extract()
            clean_temp_assignee_filed_header_list = list()
            clean_temp_assignee_filed_value_list = list()

            for item in temp_assignee_filed_header_list:
                temp_item =  re.sub(' +',' ',item.replace('\n', ' ').lstrip().rstrip())
                if temp_item:
                    clean_temp_assignee_filed_header_list.append(temp_item)
            for item in temp_assignee_filed_value_list:
                temp_item =  re.sub(' +',' ',item.replace('\n', ' ').lstrip().rstrip())
                if temp_item:
                    clean_temp_assignee_filed_value_list.append(temp_item)
            patent_filed_date_index_from_end =  clean_temp_assignee_filed_header_list.index("Filed:")-len(clean_temp_assignee_filed_header_list)
           
            patent_filed_date = clean_temp_assignee_filed_value_list[patent_filed_date_index_from_end]
            patent_assignee_index_from_end = clean_temp_assignee_filed_header_list.index("Assignee:")-len(clean_temp_assignee_filed_header_list)-3
            patent_assignee = clean_temp_assignee_filed_value_list[patent_assignee_index_from_end]
            patent_assignee_location = clean_temp_assignee_filed_value_list[patent_assignee_index_from_end+1].lstrip('(').rstrip(',')
           
        except:
            pass
        # can delete this once i know the filed, and assignee and assignee location work out.
        #try:
        #    if ((not obtained_patent_filed_date) and response.xpath('/html/body/table[3]/tr[5]/th//text()').extract()[0].rstrip()=="Filed:"):
        #        patent_filed_date = response.xpath('/html/body/table[3]/tr[5]/td/b//text()').extract()[0].rstrip()
         #       obtained_patent_filed_date = True
        #except:
        #    pass
        #try:
        #    patent_assignee = response.xpath('/html/body/table[3]/tr[3]/td/b[1]//text()').extract()[0].rstrip()
        #except:
        #    pass
        #try:
        #    temp_s = re.sub(' +',' ',' '.join(response.xpath('/html/body/table[3]/tr[3]/td//text()').extract()).replace('\n', ' ')).lstrip().rstrip()
        #    patent_assignee_location = temp_s[temp_s.find("(")+1:temp_s.find(")")].lstrip().rstrip()
        #except:
        #    pass
        
        try:
            temp_international_class_list = response.xpath('/html/body/table/tr/td[@align="right" and @valign="top" and @width="70%"]//text()').extract()
            clean_temp_international_class_list = list()        
            for item in temp_international_class_list:
                temp_item =  re.sub(' +',' ',item.replace('\n', ' ').replace('&nbsp', ' ').lstrip().rstrip())
                if temp_item:
                    clean_temp_international_class_list.append(temp_item)
            patent_international_class = ' '.join(clean_temp_international_class_list)
            #print patent_international_class
        except:
            pass

        #this grabs just the Current International Class row might need it again later
        #try:
        #    int_class_label_index = response.xpath('/html/body/table/tr/td[@align="left" and @valign="top" and @width="30%"]//text()').extract().index("Current International Class: ")
        #    patent_international_class_list = response.xpath('/html/body/table/tr/td[@align="right" and @valign="top" and @width="70%"]//text()').extract()
        #    temp_list = list()
        #    for item in patent_international_class_list:
        #        temp_item =  re.sub(' +',' ',item.replace('\n', ' ').replace('&nbsp', ' ').lstrip().rstrip())
        #        if temp_item:
        #            temp_list.append(temp_item)
        #    patent_international_class = temp_list[int_class_label_index]
        #except:
        #    pass

        profile_label = ['Number', 'Title', 'Date', 'FiledDate','Assignee','AssigneeLocation','InternationalClass', 'Abstract']
        profile_value = list()
        
        profile_value.append(patent_num)
        profile_value.append(patent_title)
        profile_value.append(patent_date)
        profile_value.append(patent_filed_date)
        profile_value.append(patent_assignee)
        profile_value.append(patent_assignee_location)
        profile_value.append(patent_international_class)
        profile_value.append(patent_abstract)
        
        #print patent_num

        if not os.path.exists('{}'.format("results")):
            os.makedirs("results")
        results_fullpath = '{}/{}'.format("results", "results.csv")

        #if not os.path.exists(results_fullpath):
        #    print "Saving in", results_fullpath
        #    with open(results_fullpath, 'w') as results_file:
        #        csv_writer = csv.writer(results_file, quoting=csv.QUOTE_ALL)
        #        csv_writer.writerow(profile_label)
        with open(results_fullpath, 'a+') as results_file:
            csv_writer = csv.writer(results_file, quoting=csv.QUOTE_ALL)
            try:
                csv_writer.writerow([x.encode('utf-8') for x in profile_value])
            except:
                pass

        #filename = 'quotes-%s.html' % page
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log('Saved file %s' % filename)


        # >>> response.xpath ('//span[@class="ProfileNav-value"]/text()').extract()
        # [u'1,232\n            ', u'834', u'1,215', u'4,897', u'1', u'More ']
        # >>> response.xpath ('//span[@class="ProfileNav-label"]/text()').extract()
        # [u'Tweets', u'Following', u'Followers', u'Likes', u'Lists', u'\xa0']
        # >>> for i in value[:4]:
        #...     print i.rsplit('\n',1)[0]
        #response.xpath ('//b[@class="u-linkComplex-target"]/text()').extract()
        #b class="u-linkComplex-target"

        #for filename in test-data/*.csv; do scrapy crawl twitter -a filename="$filename"; done
        #for filename in test-data/*.csv; do scrapy crawl twitter -a filename="$filename"; done
        #scrapy crawl twitter -a filename="data/xab.csv"
        # ROBOTSTXT_OBEY = False

