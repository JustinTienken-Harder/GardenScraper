from bs4 import BeautifulSoup
from bs4.element import NavigableString
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
url = spaghetti.tr.a.get_text(strip=True)
url = table.b.next.next.a.get_text(strip = True)
all_b = spaghetti.find_all("b")
the_tag_filter = {2,4,12}
tags = [x.next.get_text(strip=True) for index, x in enumerate(all_b) if index not in the_tag_filter and not isinstance(x, NavigableString)]
['URL:', 'Name:', 'Alternate Name:', 
'Address:', 'Mailing Address:', 'City:',
 'State:', 'Postal Code:', 'Country:',
 'Latitude/Longitude:', 'Weather:', 'Phone:',
  'Fax:', 'E-Mail:', 'Contact:', 'Designer(s):', 
  'Contruction Date:', 'Public/Private:', 'Hours:', 
  'Admission:', 'Added to JGarden:', 'Last Updated:', 
  'JGarden Description:']
next_filter = {0, 2, 4, 12} #11
