import requests # pip install requests
from bs4 import BeautifulSoup as bs # pip install beautifulsoup4
import pandas as pd # pip install pandas
import string
import sys
from difflib import SequenceMatcher

def find_fighter(fighter,fightersDF):
    
    try:
        link = fightersDF.loc[fightersDF['First Name'].str.upper() + " " + fightersDF['Last Name'].str.upper() == fighter.upper()].Link.values[0]
    except:
        closest_fighters = find_close_fighter(fighter,fightersDF)
        if len(closest_fighters == 1) :
            link = closest_fighters.Link.values[0]
        else:
            link = "There might be an error in the fighter name and we're not sure about his real identity! Please verify spelling."

    return link

def compare_names(df, col1, col2,fighter):
    return SequenceMatcher(None, df[col1].upper()+" "+df[col2].upper(),fighter.upper()).ratio()

def find_close_fighter(fighter,fightersDF):
    fightersDF["comp"] = fightersDF.apply(compare_names,args=("First Name","Last Name",fighter),axis=1)
    return fightersDF.loc[fightersDF["comp"]>0.85]

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



