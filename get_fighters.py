import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import string
import sys
from typing import List


def generate_links() -> List[str]:
    """
    Generate a list with a link to scrap for every letter of the alphabet.
    """
    return ["http://ufcstats.com/statistics/fighters?char={}&page=all".format(caracter) for caracter in list(string.ascii_lowercase)]
     
def scrap_link(link:str):
    r = requests.get(link)
    soup = bs(r.content,features="html.parser")
    parsed_fighters = soup.find_all("tr",attrs={"class":"b-statistics__table-row"}) # Get all fighters informations
    parsed_fighters_attributes = [fighter.find_all("a",attrs={"class":"b-link b-link_style_black"},text=True) for fighter in parsed_fighters] # Create a list of list of fighter first names, last names and surname
    return get_names(parsed_fighters_attributes)

def get_names(parsed_fighters_attributes) -> List[str]:

    """
    Take the html content of a page listing every fighters with a last name starting by a specific letter. 
    Ex: HTML page listing every fighter with a last name starting by A.
    Returns a list of every fighter and their link to personal webpages.
    """

    names = []
    name = "" 

    for fighter in parsed_fighters_attributes:
        name=""
        index = 0
        if len(fighter)> 0:
            for attribute in fighter:
                index+=1
                if index < 3 : 
                    name+=attribute.get_text().strip()+"|"
            name+=fighter[0]['href']+""
            names.append(name.strip())
        else:
            names.append("Empty")

    return names


if __name__ == "__main__":

     # Get Links of all pages to scrap
    links = generate_links()

    # Scrap all pages and get names
    fighters = []
    fighters = [fighter.split('|') for link in links for fighter in scrap_link(link) if fighter != "Empty"] 

    # Create DF from result and returns it
    fightersDF = pd.DataFrame.from_records(fighters,columns=["First Name","Last Name","Link"])
    
    fightersDF.to_csv('fighters.csv',index=False,sep=";")

    print(" Done ! Everything went perfect. You can now search for fighters. ")