#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import pandas
import csv
import os.path

Actu=[]
listeRss = ["https://cyware.com/allnews/feed",
            "https://www.cshub.com/rss/categories/attacks",
            'https://www.schneier.com/feed/atom/',
            'https://www.cshub.com/rss/categories/threat-defense',
            'https://www.cshub.com/rss/categories/malware',
            'https://www.fortiguard.com/rss/ir.xml',
            'https://nakedsecurity.sophos.com/feed/',
            'https://www.techrepublic.com/rssfeeds/topic/security/?feedType=rssfeeds',
            'https://www.cert.ssi.gouv.fr/feed/',
            'https://us-cert.cisa.gov/ncas/all.xml',
            'https://www.zataz.com/feed/']

Product = ["Debian", "Cisco", "Linux", "Ransomware", "attaque"]

print (("""

   _____ ______ _____ ______      ________ _______      _______ ________          __
  / ____|  ____/ ____/ __ \ \    / /  ____|  __ \ \    / /_   _|  ____\ \        / /
 | (___ | |__ | |   | |  | \ \  / /| |__  | |__) \ \  / /  | | | |__   \ \  /\  / / 
  \___ \|  __|| |   | |  | |\ \/ / |  __| |  _  / \ \/ /   | | |  __|   \ \/  \/ /  
  ____) | |___| |___| |__| | \  /  | |____| | \ \  \  /   _| |_| |____   \  /\  /   
 |_____/|______\_____\____/   \/   |______|_|  \_\  \/   |_____|______|   \/  \/    
                                                                                    
                                                                                    
Edit by : xena22
"""))

class bcolors:
    OK = '\033[92m'  # GREEN
    WARNING = '\033[93m'  # YELLOW
    FAIL = '\033[91m'  # RED
    RESET = '\033[0m'  # RESET COLOR
    GRAS = '\033[1m'  # texte en gras
    UNDERLINE = '\x1B[4m'  # Souligner

my_file = os.path.isfile("BDD.csv")
if my_file != 1 :
    df = pandas.DataFrame(list())
    df.to_csv('BDD.csv')

# scraping function
def hackernews_rss(url):
    article_list = []
    fields = ['first', 'second', 'third']
    c = csv.writer(open("BDD.csv", "w"))
    c.writerow(fields)

    for i in url:

        r = requests.get(i)

        try:

            if r.status_code == 200 :
                print(bcolors.OK + 'The scraping job succeeded: ', r.status_code, "for", i + bcolors.RESET)
                soup = BeautifulSoup(r.content, features='xml')

                articles = soup.findAll('item')

                for a in articles:
                    title = a.find('title').text
                    link = a.find('link').text
                    published = a.find('pubDate').text
                    article = {
                        'title': title,
                        'link': link,
                        'published': published,
                    }
                    article_list.append(article)
                    c.writerow([title, published, link])
            else :
                print(bcolors.FAIL + 'The scraping job failed: ', r.status_code, "for", i + bcolors.RESET)

        except Exception as e:
            print('The scraping job failed. See exception: ')
            print(e)

def ReadData(Product):
    cr = csv.reader(open("BDD.csv", "r"))
    for row in cr:
        for i in row:
            try:
                for P in Product:
                    if P in i:
                        print ("-----------------------------------------------------------------------------------------------------------------------------------------")
                        print("| " + bcolors.FAIL + "This news may interest you  | " + bcolors.RESET, i,
                              "\n| If you want to know more |", row[2])
                        Actu.append(("This news may interest you : "+ i +
                              "If you want to know more :" + row[2]))
            except Exception as e:
                print("Error")


hackernews_rss(listeRss)
print(
    "\n################################################# \n           Here is the analysis report \n################################################# \n")
print("Your search includes the following keywords :", Product, "\n \nHere is what I found for you :\n")
ReadData(Product)
#for i in Actu :
#    print (i)

input('\n Press ENTER to exit')
