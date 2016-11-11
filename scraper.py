import urllib2
from bs4 import BeautifulSoup
import pandas as pd
import csv
import sys;

def get_column(key):
    column = list()
    with open('download.csv', 'rb') as csvfile:
        sites = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in sites:
            column.append(row[key]);

    return column

def get_unique_visitors(site):
    site = "http://www.siteworthtraffic.com/report/"+site;
    page = urllib2.urlopen(site);
    soup = BeautifulSoup(page, "html.parser");

    tables = soup.find_all('table');
    rightTable = tables[0];
    unique_visitors = '';
    for char in rightTable.findAll("tr")[0].get_text():
        if char.isdigit():
            unique_visitors+=char;
    try:
        return int(unique_visitors);
    except ValueError:
        return 0;


domains = get_column('Domain')
Unique_Visitors = list();
for row in domains:
    visitors = get_unique_visitors(row);
    Unique_Visitors.append(visitors);
    print(visitors);
d = {'Site':get_column('Site'), 'Domain':domains,
        'Rank':get_column('rank'), 'Unique_Visitors':Unique_Visitors,
         'Type':get_column('Type'), 'Country':get_column('Principal country')}
df = pd.DataFrame.from_dict(d);
df.to_csv('ranked_domains.csv');
