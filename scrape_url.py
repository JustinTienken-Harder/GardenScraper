from bs4 import BeautifulSoup
from bs4.element import NavigableString
import requests

def match_class(target):                                                        
    def do_match(tag):                                                          
        classes = tag.get('class', [])                                          
        return all(c in classes for c in target)                                
    return do_match


URL = 'http://www.jgarden.org/gardens.asp?ID=306'
URL2 = 'http://www.jgarden.org/gardens.asp?ID=308'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
spaghetti = soup.find_all(match_class(["smallText"]))[1]
url = spaghetti.tr.a.get_text(strip=True)
all_b = spaghetti.find_all("b")
if "URL" in all_b[0].text:
    filter = {2,4,12}
else:
    filter = {1,3,11}
tags = [x.get_text(strip=True) for index, x in enumerate(all_b) if index not in filter]
values = [x.next.next.get_text(strip=True) for index, x in enumerate(all_b) if index not in filter]
scraped_values = dict(zip(tags, values))
tags_alt = [x.get_text(strip=True) for x in all_b if  not isinstance(x, NavigableString)]
tags = [x.get_text(strip=True) for index, x in enumerate(all_b) if index not in the_tag_filter and not isinstance(x, NavigableString)]
values = [x.next.next.get_text(strip=True) for index, x in enumerate(all_b) if index not in the_tag_filter]
