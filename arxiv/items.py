# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from datetime import datetime


def date_strip(date_str):  
    """
    Converts date as found in arXiv to datetime.
    Example: ' Thu, 6 Sep 2018 09:39:44 GMT  (4024kb,D)' --> 2018-09-06 09:39:44
    """
    stripped_date = date_str[0].split('GMT', 1)[0].strip(' ')
    return datetime.strptime(stripped_date,  '%a, %d %b %Y %H:%M:%S')



class ArxivItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    ID = scrapy.Field() 
    date = scrapy.Field(output_processor = date_strip ) 
    title = scrapy.Field() 
    author = scrapy.Field() 
    link = scrapy.Field() 
    journal = scrapy.Field() 
    comments = scrapy.Field() 
    primary_cat = scrapy.Field() 
    all_cat = scrapy.Field() 
    abstract = scrapy.Field() 