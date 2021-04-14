import requests # pip install requests
from bs4 import BeautifulSoup as bs # pip install beautifulsoup4
import pandas as pd # pip install pandas
import string
import sys
from difflib import SequenceMatcher

def find_fighter(fighter:str, fightersDF:pd.DataFrame) -> str:
    
    """
    For a given fighter name, find the fighter UFC stats page link.
    If there's a small error, find the closest fighter name and send back its link.
    Else, send back an error message.

    Arguments : 

    fighter -- name of the searched fighter (ex : Michael Bisping)
    fightersDF -- DataFrame of every fighter and a link to scrap to get their fights.

    """

    try:
        link = fightersDF.loc[fightersDF['First Name'].str.upper() + " " + fightersDF['Last Name'].str.upper() == fighter.upper()].Link.values[0]
    except:
        closest_fighters = find_close_fighter(fighter,fightersDF)
        if len(closest_fighters == 1) :
            link = closest_fighters.Link.values[0]
        else:
            link = errorMessage

    return link

def compare_names(df:pd.DataFrame, col1:str, col2:str, fighter:str) -> SequenceMatcher:
    return SequenceMatcher(None, df[col1].upper()+" "+df[col2].upper(),fighter.upper()).ratio()

def find_close_fighter(fighter:str, fightersDF:pd.DataFrame) -> pd.DataFrame:
    fightersDF["comp"] = fightersDF.apply(compare_names,args=("First Name","Last Name",fighter),axis=1)
    return fightersDF.loc[fightersDF["comp"]>0.85]

def scrap_fighter(link:str) -> pd.DataFrame:

    """
    For a given link, scrap the webpage and return a DataFrame of every fights.

    Arguments : 

    link -- link to scrap
    
    """
    r = requests.get(link)
    soup = bs(r.content,features="html.parser")
    parsed_fighs = soup.find_all("a",attrs={"class":"b-link b-link_style_black"},text=True)
    all_infos = [str(element.get_text()).strip() for element in parsed_fighs]
    divided_infos = [all_infos[x:x+3] for x in range(0, len(all_infos),3)]
    df = pd.DataFrame.from_records(divided_infos,columns=["Fighter 1","Fighter 2","Event"])
    return df

if __name__ == "__main__":

    fighter = sys.argv[1] # Get fighter to search from an argument passed in command line call
    
    if len(sys.argv)>=3:
        one_by_one = sys.argv[2]
    else:
        one_by_one=""

    errorMessage = "There might be an error in the fighter name and we're not sure about his real identity! Please verify spelling."
    
    # Read DF
    fightersDF = pd.read_csv('fighters.csv',sep=";")

    # Get the fighter's link
    link = find_fighter(fighter, fightersDF)
    
    if link != errorMessage :
        # Scrap the link and get his fights
        fightsDF = scrap_fighter(link)
        # If the one by one mode isn't activated, print the full career.
        if one_by_one == "":
            print(fightsDF)
        # If the one by one mode is activated, print one fight each time the user press enter
        else:
            print("You are in the one by one mode ! Press enter after each fight displayed to see the following one. \n")
            fight_count = len(fightsDF)
            for i in range(fight_count):
                if i==0:
                    print(fightsDF.loc[[fight_count-1-i]])
                else:
                    print(fightsDF.loc[[fight_count-1-i]].to_string(header=False))
                input("")
            print("You made it to end !")

    else : 
        print(errorMessage)



