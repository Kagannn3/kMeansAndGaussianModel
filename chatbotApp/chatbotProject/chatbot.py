import requests
# This modulle allows you to send HTTP requests using Python.
#In this context, it is used to fetch data from a website 
from bs4 import BeautifulSoup
#BeautifulSoup is a Python library for parsing HTML and XML documents.
#It makes it easy to extract specific information from web pages.
import re
#The re module provides regular expression matching operations.
#We will use it for basic text processing 

def fetch_info():
    url = 'https://www.wikipedia.org/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = [headline.text for headline in soup.find_all('h2')]
    return headlines

def tokenize(text):
    return re.findall(r'\w+', text.lower())
# \w+ uses a regular expression to find all sequences of word characters (letters, digits and underscores).
#The re.findall function returns a list of all matches. 
#We converted the text to lowercase.



