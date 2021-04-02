import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import string

def main(fighter):

    # Read DF
    fightersDF = pd.read_csv('fighters.csv',sep=";")

    # Get the fighter's link
    link = find_fighter(fighter, fightersDF)
    
    # Scrap the link and get his fights
    fightsDF = scrap_fighter(link)

    return fightsDF

def find_fighter(fighter,fightersDF):
    
    try:
        link = fightersDF.loc[fightersDF['First Name'] + " " + fightersDF['Last Name'] == fighter].Link.values[0]
    except:
        link = "There must be an error in the figher name !"

    return link
    

def scrap_fighter(link):

    r = requests.get(link)
    soup = bs(r.content,features="html.parser")
    parsed_fighs = soup.find_all("a",attrs={"class":"b-link b-link_style_black"},text=True)
    all_infos = [str(element.get_text()).strip() for element in parsed_fighs]
    divided_infos = [all_infos[x:x+3] for x in range(0, len(all_infos),3)]
    df = pd.DataFrame.from_records(divided_infos,columns=["Fighter 1","Fighter 2","Event"])
    return df

print(main("Charles Oliveira"))