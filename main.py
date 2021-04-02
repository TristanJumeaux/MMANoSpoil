import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import string
import sys

def find_fighter(fighter,fightersDF):
    
    try:
        link = fightersDF.loc[fightersDF['First Name'].str.upper() + " " + fightersDF['Last Name'].str.upper() == fighter.upper()].Link.values[0]
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

if __name__ == "__main__":

    fighter = sys.argv[1]

    # Read DF
    fightersDF = pd.read_csv('fighters.csv',sep=";")

    # Get the fighter's link
    link = find_fighter(fighter, fightersDF)
    
    if link != "There must be an error in the figher name !" :
        # Scrap the link and get his fights
        fightsDF = scrap_fighter(link)
        print(fightsDF)

    else : 
        print("There was an error in the fighter name. Please correct !")


