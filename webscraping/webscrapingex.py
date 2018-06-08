# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 10:42:02 2017

@author: rbabu
"""

import pandas as pd
import numpy as np
import requests
from requests import get
from bs4 import BeautifulSoup

class imdb(object):
    def getting_url(self):
      response = get('http://www.imdb.com/search/title?release_date=2017&sort=num_votes,desc&page=1')
      html_soup = BeautifulSoup(response.text, 'html.parser')
      return html_soup

    def movie_data(self):
      html_soup = self.getting_url()
      movie_containers =html_soup.find_all('div', class_ = 'lister-item mode-advanced')
      return movie_containers
    
    def columns_data(self):
        movie_containers = self.movie_data()  
        years=[]
        length=[]
        genres=[]
        imdb_scores=[]
        meta_scores=[]
        names =[]
        for i in range(0,len(movie_containers)):
            title= movie_containers[i].h3.a.text
            names.append(title)
            year=movie_containers[i].h3.find('span', class_ = 'lister-item-year text-muted unbold').text
            years.append(year)
            len_=movie_containers[i].p.find('span',class_="runtime").text
            length.append(len_)
            genre=movie_containers[i].p.find('span',class_="genre").text
            genres.append(genre)
            imdb=movie_containers[i].strong.text
            imdb_scores.append(imdb)
            meta= movie_containers[i].find('span',class_="metascore favorable")
            if meta is not None:
                metatext = meta.get_text(strip=True)
                meta_scores.append(metatext)
            else:
                meta_scores.append('None')
        return names,years,length,genres,imdb_scores,meta_scores
    
    
def main():
     imdbObj = imdb() 
     titles,years,length,genres,imdb_scores,meta_scores = imdbObj.columns_data()
     print(titles)
     df=pd.DataFrame.from_dict(dict ({"movie-name":titles,"release_year":years,"time":length,"imdb":imdb_scores,"metascore":meta_scores}))

main()
