# Python3-Scrapy-Projects
Scrapy Projects i am working on under Python 3 - started April 2017.

This repository now includes examples of the python3 scrapy code i use in my projects.

They all follow the normal scrapy folder convention Projectname / Projectname / spiders The second folder contains items.py, pipelines.py an settings.py (i have made changes to the standard pipelines.py file and settings.py file because i use Windows10, as discussed below).  The spiders folder contains the programs i have included in this repository.  The items.py files can be deduced from the spiders files

Pipelines.py is the Scrapy Pipelines.py file which in my case allows the Spider to be run in the CMD window with the command <scrapy crawl spidername> and then adds text to the end of the name for the CSV file name but also because i use Windows10 it recreates the created CSV file to a new file without the alternate blank lines.  Don't forget to add the line <ITEM_PIPELINES = {'spidename.pipelines.CSVPipeline': 300 }> to the settings.py file!

Standardcode.py is the standard style of Scrapy code i use where i can

Selenium_example1.py is the Scrapy code i use where part of the webpage is dynamic(?) hence we need to use selenium and a button to create a new part of the same webpage needs to be pressed

Selenium_example2.py is the Scrape i use where i need to deploy selenium to press a button on a webpage to reveal more and then use the revealed links to open new webpages to scrap.

Selenium_example3.py is the same style as Selenium_example2.py
