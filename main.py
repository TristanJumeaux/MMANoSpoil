import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

r = requests.get("http://ufcstats.com/fighter-details/2b93ebd9f5417ad2")

soup = bs(r.content,features="html.parser")

parsed_fighs = soup.find_all("a",attrs={"class":"b-link b-link_style_black"},text=True)

all_infos = [str(element.get_text()).strip() for element in parsed_fighs]

divided_infos = [all_infos[x:x+3] for x in range(0, len(all_infos),3)]

df = pd.DataFrame.from_records(divided_infos,columns=["Fighter 1","Fighter 2","Event"])

print(df)


