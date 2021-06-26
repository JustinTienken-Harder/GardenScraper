import warnings 
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
def scrape_jgarden_url(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    spaghetti = soup.find_all(match_class(["smallText"]))[1]
    all_b = spaghetti.find_all("b")
    #If the first element has URL: in it, then we need this filter scheme
    if "URL" in all_b[0].text:
        filter = {2,4,12}
    else:
        filter = {1,3,11}
    # This gets all the attributes
    tags = [x.get_text(strip=True) for index, x in enumerate(all_b) if index not in filter]
    values = [x.next.next.get_text(strip=True) for index, x in enumerate(all_b) if index not in filter]
    scraped_values = dict(zip(tags, values))
    lat_long_tuple = [x for x in scraped_values.items() if "Latitude" in x[0]]
    if len(lat_long_tuple) > 1:
        warnings.warn(f"There are multiple lat/longs in the dictionary for: {URL}")
    else:
        lat_lon, values = lat_long_tuple[0]
        #Remove lat_lon k/v pair from dictionary.
        scraped_values.pop(lat_lon)
        #Make two keys
        lat, lon = lat_lon.split("/")
        lat += ':'
        # Now process the values
        lat_val, lon_val = values.replace("Find Gardens Nearby", "").replace(" ", "").split(";")
        lat_val = lat_val.replace('lat=', '')
        lon_val = lon_val.replace('long=', '')
        try:
            lat_val = float(lat_val)
            lon_val = float(lon_val)
        except Exception as e:
            warnings.warn(f"The lat/lon could not be converted to float for: {URL}")
        finally:
            scraped_values[lat] = lat_val
            scraped_values[lon] = lon_val
        try:
            identifier = scraped_values["Name:"]
        except Exception as e:
            identifier = URL[-3:]
            warnings.warn(f'There is no Name attribute for: {URL}')
            
    return identifier, scraped_values

if __name__ == "__main__":
    URL = 'http://www.jgarden.org/gardens.asp?ID=306'
    URL2 = 'http://www.jgarden.org/gardens.asp?ID=308'
    URL3 = 'http://www.jgarden.org/gardens.asp?ID=255'
    URL4 = 'http://www.jgarden.org/gardens.asp?ID=386'
    attributes = scrape_jgarden_url(URL3)
    for k, v in attributes.items():
        print(k, v)
        print(" ")
    attributes = scrape_jgarden_url(URL4)
    print("NEW GARDEN!")
    for k, v in attributes.items():
        print(k, v)
        print(" ")
