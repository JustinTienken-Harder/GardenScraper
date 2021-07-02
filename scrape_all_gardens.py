from time import sleep
import json 
import warnings
import requests
from bs4 import BeautifulSoup, Comment

  
def process_jgarden_html_v2(soup, URL=None):
    if isinstance(soup, str):
      URL = soup
      page = requests.get(soup)
      soup = BeautifulSoup(page.content, 'html.parser')
    hmmm = soup.find_all(string = lambda text: isinstance(text, Comment) and str(text) == ' begin inner table ')
    actual = hmmm[1].next.next
    table_rows = actual.find_all("tr")
    table_data = [x.find_all("td") for x in table_rows]
    weird_reshape = table_data[2:-1]
    scraped_values = dict((x[0].get_text(strip=True), x[1].get_text(strip=True)) for x in weird_reshape)
    lat_long_tuple = [x for x in scraped_values.items() if "Latitude" in x[0]]
    if len(lat_long_tuple) > 1:
        warnings.warn(f"There are multiple lat/longs in the dictionary for: {URL}")
    elif len(lat_long_tuple) == 0:
        warnings.warn(f"There are no Lat/Long coordinates in the dictionary for: {URL}")
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


base_json_new = dict()
for i in range(1,663):
    sleep(0.5)
    print(i)
    if i <10:
      url = 'http://www.jgarden.org/gardens.asp?ID=00'+str(i)
    elif i >= 10 and i < 100:
      url = 'http://www.jgarden.org/gardens.asp?ID=0'+str(i)
    else:
      url = 'http://www.jgarden.org/gardens.asp?ID='+str(i)
    ID = url[-3:]
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
      identifier_new, data_new = process_jgarden_html_v2(soup, url)
    except Exception as e:
      with open("failed_urls_new.txt", "a") as f:
        print("failure")
        f.write(url+"\n")
      continue

    if identifier_new in base_json_new:
      warnings.warn(f'Looks like you got a duplicate name, dummy: {url}')
      identifier_new = ID
    base_json_new[identifier_new] = data_new


with open("world_gardens_pretty_new.json", "w") as file:
  json.dump(base_json_new, file, indent=4)