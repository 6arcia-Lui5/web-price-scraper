from bs4 import BeautifulSoup
import requests
import numpy as np
import csv
from datetime import datetime

EBAY_LINK = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw="
NEWEGG_LINK = "https://www.newegg.com/p/pl?d="

def get_user_request():
    item_name = input("What are you looking for today?\n")
    name_split = item_name.split()
    return name_split

def create_new_link(array, link):
    new_name = ""
    for word in array:
        new_name = new_name+word+"+"

    new_name = new_name[:-1]
    new_link = link + new_name
    return new_link

def get_prices_by_link(link):
    if (LINK.__contains__("ebay")):
        #gets source
        r = requests.get(link)
        #parse source
        page_parse = BeautifulSoup(r.text, 'html.parser')
        #find all list items from search results
        search_results = page_parse.find("ul", {"class":"srp-results"}).find_all("li", {"class": "s-item"})

        item_price = []

        for result in search_results:
            price_as_text = result.find("span", {"class":"s-item__price"}).text
            if "to" in price_as_text:
                continue
            price = float(price_as_text[1:].replace(",",""))
            item_price.append(price)
        return item_price
    """
    if (LINK.__contains__("newegg")):
        #gets source
        r = requests.get(link)
        #parse source
        page_parse = BeautifulSoup(r.text, 'html.parser')
        #find all list items from search results
        search_results = page_parse.find("div", {"class":"item-cells-wrap"}).find_all("div", {"class": "item-cell"})

        item_price = []

        for result in search_results:
            price_as_text = result.find("span", {"class":"current-price-label"}).text
            if "to" in price_as_text:
                continue
            price = float(price_as_text[1:].replace(",",""))
            item_price.append(price)
        return item_price

    """
    
def remove_outliers(prices, m=2):
    data = np.array(prices)
    return data[abs(data - np.mean(data)) < m * np.std(data)]

def get_average(prices):
    return np.mean(prices)

def save_to_file(prices):
    fields=["ebay",np.around(get_average(prices), 2),datetime.today().strftime("%B-%D-%Y")]
    with open('prices.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

if __name__ == "__main__":
    name_as_array = get_user_request()
    LINK = create_new_link(name_as_array, EBAY_LINK)
    ebay_prices = get_prices_by_link(LINK)
    prices_withoiut_outliers = remove_outliers(ebay_prices)
    print(get_average(prices_withoiut_outliers))
    save_to_file(ebay_prices)

    #LINK = create_new_link(name_as_array, NEWEGG_LINK)
    #new_egg_prices = get_prices_by_link(LINK)
    #prices_withoiut_outliers = remove_outliers(new_egg_prices)
    #save_to_file(new_egg_prices)
