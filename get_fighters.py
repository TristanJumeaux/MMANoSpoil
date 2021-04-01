import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import string


def main():

    # Get Links of all pages to scrap
    #links = generate_links()[0]
    links = ["http://ufcstats.com/statistics/fighters?char=a&page=all","http://ufcstats.com/statistics/fighters?char=b&page=all"]
    fighters=[]
    # Scrap all pages and get names
    fighters = [fighter for link in links for fighter in scrap_link(link) if fighter != "Empty"] 

    return fighters

def generate_links():
    return["http://ufcstats.com/statistics/fighters?char={}&page=all".format(caracter) for caracter in list(string.ascii_lowercase)]
     
def scrap_link(link):
    r = requests.get(link)
    soup = bs(r.content,features="html.parser")
    parsed_fighters = soup.find_all("tr",attrs={"class":"b-statistics__table-row"}) # Get all fighters informations
    parsed_fighters_attributes = [fighter.find_all("a",attrs={"class":"b-link b-link_style_black"},text=True) for fighter in parsed_fighters] # Create a list of list of fighter first names, last names and surname
    return get_names(parsed_fighters_attributes)

def get_names(parsed_fighters_attributes):
    names = []
    name = "" 

    for fighter in parsed_fighters_attributes:
        name=""
        index = 0
        if len(fighter)> 0:
            for attribute in fighter:
                index+=1
                if index < 3 : 
                    name+=attribute.get_text().strip()+" "
            names.append(name.strip())
        else:
            names.append("Empty")

    return names

res = main()
print(res)

