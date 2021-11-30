#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import pandas
import csv
import os.path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, ssl
import datetime


Actu = []
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

Product = ["Microsoft", "Malware"]
email_address = 'Who send mail ?'
email_password = 'Not good but always in preprod :) Sorry'
email_receiver = ('Who receive ?')
smtp_address = 'smtp.gmail.com'
smtp_port = 465

# on crée un e-mail
message = MIMEMultipart("alternative")
# on ajoute un sujet
message["Subject"] = "[Secoverview] News cyber du "+ datetime.date.today().__str__()
# un émetteur
message["From"] = email_address
# un destinataire
message["To"] = email_receiver

print(("""

   _____ ______ _____ ______      ________ _______      _______ ________          __
  / ____|  ____/ ____/ __ \ \    / /  ____|  __ \ \    / /_   _|  ____\ \        / /
 | (___ | |__ | |   | |  | \ \  / /| |__  | |__) \ \  / /  | | | |__   \ \  /\  / / 
  \___ \|  __|| |   | |  | |\ \/ / |  __| |  _  / \ \/ /   | | |  __|   \ \/  \/ /  
  ____) | |___| |___| |__| | \  /  | |____| | \ \  \  /   _| |_| |____   \  /\  /   
 |_____/|______\_____\____/   \/   |______|_|  \_\  \/   |_____|______|   \/  \/    


Edit by : xena22
https://github.com/xena22/secoverview
"""))

my_file = os.path.isfile("BDD.csv")
if my_file != 1:
    df = pandas.DataFrame(list())
    df.to_csv('BDD.csv')


# scraping function
def hackernews_rss(url):
    global article_list
    article_list = []
    fields = ['first', 'second', 'third']
    c = csv.writer(open("BDD.csv", "w"))
    c.writerow(fields)

    for i in url:
        r = requests.get(i)
        try:
            if r.status_code == 200:
                #print('The scraping job succeeded: ', r.status_code, "for", i)
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
            #else:
                #print('The scraping job failed: ', r.status_code, "for", i)

        except Exception as e:
            print('The scraping job failed. See exception: ')
            print(e)
            print (i)


def ReadData(Product):
    for row in article_list:
        try:
            for P in Product:
                if P in (row["title"]):
                    with open('résultat.csv', 'a', newline='', encoding='utf-8') as c:
                        writer = csv.writer(c)
                        writer.writerow([row["title"]])
                    print(
                        "-----------------------------------------------------------------------------------------------------------------------------------------")
                    print("| "+row["published"]+"\n| This news may interest you  : ", row["title"],
                            "\n|\n| If you want to know more : ", row["link"],"\n|")
                    Actu.append(("<p><strong>This news may interest you : </strong>" + row["title"] +
                                '<br />If you want to know more :<a href="' + row["link"]) + '">Website</a></p>')
        except :
                print("Error")

    if os.path.exists("sample.txt"):
        os.remove("sample.txt")
    with open("sample.txt", "a") as file_object:
        for i in Actu:
            file_object.write(i)

def Mail() :
    try :# on crée un texte et sa version HTML
        texte = '''
        Secoverview TEAM
        '''
        with open('sample.txt') as f:
            html = f.readlines().__str__()

        # on crée deux éléments MIMEText
        texte_mime = MIMEText(texte, 'plain')
        html_mime = MIMEText(html, 'html')

        # on attache ces deux éléments
        message.attach(texte_mime)
        message.attach(html_mime)

        # on crée la connexion
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_address, smtp_port, context=context) as server:
            # connexion au compte
            server.login(email_address, email_password)
            # envoi du mail
            server.sendmail(email_address, email_receiver, message.as_string())
    except :
        print ("Impossible d'envoyer le mail. Vérifiez les informations de connection")

hackernews_rss(listeRss)
print(
    "\n################################################# \n           Here is the analysis report \n################################################# \n")
print("Your search includes the following keywords :", Product, "\n \nHere is what I found for you :\n")
ReadData(Product)
Mail()

os.remove("sample.txt")

# open file in read mode
with open('résultat.csv', 'r',encoding='utf-8') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = csv.reader(read_obj)
    # Iterate over each row in the csv using reader object
    for i in csv_reader:
        for row in article_list :
            if i == row["title"] :
        # row variable is a list that represents a row in csv
                print(i)

input('\n Press ENTER to exit')


