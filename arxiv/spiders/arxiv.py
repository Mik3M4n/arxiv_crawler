import scrapy
from datetime import datetime, timedelta
import re
import time
from scrapy.loader import ItemLoader
from scrapy.http import FormRequest
from arxiv.items import ArxivItem



class ArxivSpider(scrapy.Spider):
    name = "arxiv"

    def __init__(self, search_query , field = 'all' , start = 0, \
                 date_from = '', date_to = '', filter_date = '', **kwargs):
        super().__init__(**kwargs)
        
        try:
            self.search_query_or = search_query
            if len(search_query.split(' '))>1:
                search_query = re.sub(' ', '+', search_query)
            self.search_query = '%22'+search_query+'%22'
        except NameError:
            raise ValueError('Please enter a valid search query.')
        
        if not date_from and not date_to:
            self.date_to = time.strftime('%Y-%m-%d')
            self.date_from =yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            self.filter_date='all_dates'
        else:
            self.date_to = date_to
            self.date_from = date_from
            self.filter_date = 'date_range'
        
        self.start = start
        self.field = field
        
        self.base_url = 'https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term='
        
        self.url = self.base_url+self.search_query+'&terms-0-field='+self.field+\
        '&classification-computer_science=y&classification-economics=y&classification-eess=y&classification-mathematics=y&classification-physics=y&classification-physics_archives=all&classification-q_biology=y&classification-q_finance=y&classification-statistics=y&date-filter_by='\
+self.filter_date\
+'&date-year=&date-from_date='\
+self.date_from\
+'&date-to_date='+self.date_to+'&date-date_type=submitted_date&abstracts=show&size=50&order=-announced_date_first'

        self.start_urls = [self.url]
        self.tot_papers = 0
        print('\n Url to scrape: \n %s \n ' %self.url)
        print('Date_from = %s \n ' %self.date_from)
        print('Date_to = %s \n ' %self.date_to)
        print('Filter_date = %s \n \n' %self.filter_date)


    def parse(self, response):
        
        for paper in response.css("li.arxiv-result"):
            
            self.tot_papers +=1
   
            new = ItemLoader(item=ArxivItem(),selector=paper)
            
            # 1. add fields that can be read directly from main page
            new.add_value('ID', paper.css("p.list-title a::text").extract_first().strip('arXiv:'))
            comments=paper.css('p.comments span::text').extract()
            if len(comments)>1:
                new.add_value('comments',comments[1] )            
            new.add_value('title', paper.css("p.title::text").extract_first().strip(' \n '))
            new.add_value('author', paper.css("p.authors").css("a::text").extract())
            new.add_value('primary_cat',  paper.css("span.tag::text").extract_first())
            new.add_value('abstract', (' ').join([sent if sent!=' ' else self.\
                                            search_query_or for sent in  paper.css("span.abstract-full::text").\
                                            extract()]).strip('\n '))           

            journal = paper.css("p.comments::text").extract()
            if len(journal)>0:
                new.add_value('journal', journal[-1].strip('\n'))
            
            # 2. add fields that have to be added following links 
            abs_page = paper.css("p.list-title a::attr(href)").extract_first()
            new.add_value('link', abs_page) # add link to abstract page
            yield scrapy.Request(abs_page, callback=self.parse_abs_page, dont_filter = True, meta={'item':new})            
  
        
        # 3. scrape next page until one exist
        next_page = response.xpath("//nav//a[contains(@class, pagination-next)]/@href").extract()[1]
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

        print('\n %s papers found .... ' %self.tot_papers)
  

    
    def parse_abs_page(self, response):
        """
        From arXiv abstract page, fetches: 
        - submisison date and time
        - all categories including cross-references
        """
        
        new = ItemLoader(item=ArxivItem(), response=response, parent=response.meta['item']) 
        
        # all arXiv categories
        other_cat_full_cont = response.css('td[class*=subjects]').extract()[0].split('</span>;')
        if len(other_cat_full_cont)>1:
            other_cats = other_cat_full_cont[1]
            other_cats_list = [x.strip('\(').strip('\)') for x in re.findall('\(.*?\)', other_cats)]
        else: other_cats_list = []
            
        main_cat = re.findall('\(.*?\)', response.css('div.metatable span::text').extract()[0])[0].strip('\(').strip('\)')
        all_cats =[main_cat]+other_cats_list
        new.add_value('all_cat', all_cats)
        
        # submission date
        new.add_value('date', response.css('div.submission-history::text').extract()[-2])
        
        yield new.load_item()
        
        