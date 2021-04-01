# MMANoSpoil

As a MMA fan, I love to watch fights during my free time. 

What I especially like to do is to chose a fighter and watch all his fights from the start to the end of his career.

However, the platform that I use to do this, the UFC fight pass, doesn't offer this feature.
When you search for a fighter, you just have all his fights without any particular order or temporality.

Hence, I decided to build this little project ! 

# Goal 

This is how I would like it to work : 

* Type in a fighter name
* Get the list of his fight from oldest to newest

# How

In order to do that, we need to get datas : 

* List of fighters ?
* List of fight for each fighters ?

In the past, I used to play with the ESPN API which offers various services about data and sports.
Unfortunately, even though they are now closely attached to the UFC, they do not offer any API.
Consequently, I was thinking about using BeautifulSoup in order to webscrap some webpages that contains these informations.

To begin with, what I plan to do is to create a dataset that lists fighters and a link to a webpage containing their fights (by webscraping an index of fighters).
Then, the user will type in a fighter name, if it matches, we scrap the link and get back fights.
If there isn't any match, we will use a string comparison method (not fixed yet but I was thinking about Levenshtein) and send back the closest name in case of a typing error.

# Progress

Here we go ! Work has been started.
