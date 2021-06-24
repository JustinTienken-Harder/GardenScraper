from bs4 import BeautifulSoup
import requests

def match_class(target):                                                        
    def do_match(tag):                                                          
        classes = tag.get('class', [])                                          
        return all(c in classes for c in target)                                
    return do_match


URL = 'http://www.jgarden.org/gardens.asp?ID=306'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
spaghetti = soup.find_all(match_class(["smallText"]))[1]
table = spaghetti.tr

