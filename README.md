
# ARXIV CRAWLER

This code is a crawler for arxiv.org written in python3 and based on [scrapy](https://scrapy.org/).
It retrieves all results of an advanced arxiv search, easily saved in .csv (or .json) format.

## DISCLAIMER 

This code is written for practice only, to learn how to use scrapy to recursively parse an advanced arxiv search. It *should not be used*, as explained in the [arxiv.org guidelines](https://arxiv.org/help/robots). Running it will likely result in you ip being blocked from the arxiv.
To download arxiv metadata, you can refer to the [arxiv API](https://arxiv.org/help/api/index)



## Description

This code allows to fetch all arrive metadata available via the [arxiv advanced search](https://arxiv.org/search/advanced). See the section "Output" for a more detailed description of the fields available. 
An example output can be found in the /output folder with a jupiter notebook to visualise data. Here’s an example:

![Example output](https://github.com/Mik3M4n/arxiv_crawler/blob/master/arxiv_ML_query.png)

Note that scrapy launches asynchronous requests, so the data should be then sorted manually, as done in the notebook.


### Prerequisites

python3 and scrapy

```
pip install scrapy
```


## Running 

Clone the repo, go to the main directory and run:


```
scrapy crawl arxiv -a search_query=<arxiv_search_query> -a field=<field> -a date_from=<from_date> -a to_date=<to_date> -o <output_file>
```

* - a specifies the input parameters
* - o specifies the output file if you want to save your data (e.g. my_query.csv)


Example of valid parameters and format:

* <arxiv_search_query>: machine\ learning
* < field >: the field where to look for (ex: 'all', 'ti', 'abs')
* <from_date>/<to_date>:  2018-09-13
* <output_file>: output/my_search.csv


Mandatory parameters:
* search_query : must be a valid string. See the [arxiv documentation](https://arxiv.org/help/api/user-manual#_query_interface) for the syntax of advanced queries, booleans, phrases etc.

Other:
* field : if not specified, it is automatically set to 'all'
* date_from/ date_to : if not provided, the search is automatically set to 'all_dates'. If specified, they must be both specified in the format described above




For example, the image above and the example output in /output are the result of the following query:
```
scrapy crawl arxiv -a search_query=machine\ learning -a date_from = 2018-09-01 date_to=2018-09-13 -o output/ML_all.csv
```




## Output fields

The output fields (names and order) are specified in items.py

The code fetches the following fields (names should be quite self-explanatory):
- "ID" 
- "date"
- "title"
- "author"
- "link"
- "journal"
- "comments"
- "primary_cat"
- "all_cat"
- "abstract"



## To do

* As of now, the query is on all the arxiv fields. The input can easily be adapted to search in specific subfields (e.g : phys , cs.AI , …)

