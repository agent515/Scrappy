from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.keys import Keys  # need to send keystrokes
import re
import sys, getopt

def main(argv):
    
    try:
        opts, args = getopt.getopt(argv, "ahpl:", ["limit=", "help"])
    except getopt.GetoptError:
        print("Either invalid option is used or none argument passed to the option which requires one.")

    printText = False
    limit = 10
    
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print("-a : about the util\n-h : help\n-l : limit option setting the maximum no. of pages to parse. Default is 10.\n-p : print the product details in the CLI. Default is False")
            sys.exit()
        elif opt in ("-l", "--limit"):
            limit = int(arg)
        elif opt == '-p':
            printText = True
        elif opt == '-a':
            print("A fun web-scraping utility which searches through Flipkart website and fetches important product details and \nsaves it to the .csv file in SearchResult folder.")
            sys.exit()

    """
        Initializing the webdriver for Google Chrome by providing the absolute path to the executable file in webdriver
    """
    driver = webdriver.Chrome(
        'C:\Program Files\chromedriver_win32\chromedriver.exe')

    siteUrl = "https://www.flipkart.com/"

    query = input("Searh: ")

    driver.get(siteUrl)

    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    search_box = driver.find_element_by_css_selector(".LM6RPg")
    search_box.clear()
    search_box.send_keys(query)
    button = driver.find_element_by_css_selector('.vh79eN')
    button.send_keys(Keys.ENTER)

    """
        In the search result, grid-layout and inner div classes are different for different categories..
        As of now, these are the grid_classes and their inner-classes which I've come across during testing electronic, grocery and clothing items
    """
    grid_classes = {
        '_3wU53n': {'itemName': '_3wU53n', 'specifications': 'tVe95H', 'price': '_1vC4OE _2rQ-NK', 'rating': 'hGSR34', 'imageUrl': '_3BTv9X', 'cmd' : "pd.DataFrame({'itemName': itemNameList, 'itemUrl': itemUrlList, 'specifications': specificationsList, 'price': priceList, 'imageUrl': imageUrlList, 'rating': ratingList})"},
        '_3liAhj': {'itemName': '_2cLu-l', 'specifications': '_1rcHFq', 'price': '_1vC4OE', 'rating': 'hGSR34', 'imageUrl': '_3BTv9X', 'cmd' : "pd.DataFrame({'itemName': itemNameList, 'itemUrl': itemUrlList, 'specifications': specificationsList,'price': priceList, 'imageUrl': imageUrlList, 'rating': ratingList})"},
        'IIdQZO _1SSAGr': {'brand': '_2B_pmu', 'itemName': '_2mylT6', 'price': '_1vC4OE', 'imageUrl': '_3togXc', 'cmd' : "pd.DataFrame({'itemName': itemNameList, 'brand': brandList, 'itemUrl' : itemUrlList, 'price' : priceList, 'imageUrl': imageUrlList})"}
    }

    grid_class = None

    url = driver.current_url
    driver.get(url)

    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    pageText = soup.find('div', attrs={'class': '_2zg3yZ'})
    
    if pageText:
        pageText = pageText.span.string
        m = re.findall(r'[-+]?\d*,\d+|\d+', pageText)
        currentPage = int(m[0].replace(',', ''))
        totalPages = int(m[1].replace(',', ''))
    else:
        currentPage = 1
        totalPages = 1

    while currentPage <= totalPages and currentPage <= limit:
        for div in soup.findAll('div', attrs={'class': '_3O0U0u'}):
            if div.find('div', attrs={'class': '_3wU53n'}):
                if not grid_class:
                    itemNameList = []
                    itemUrlList = []
                    specificationsList = []
                    priceList = []
                    ratingList = []
                    imageUrlList = []

                grid_class = '_3wU53n'
                itemUrl = siteUrl + div.a['href']
                itemName = div.find('div', attrs={'class': '_3wU53n'}).string
                specifications = [spec.string for spec in div.find_all(
                    'li', attrs={'class': 'tVe95H'})]
                price = div.find('div', attrs={'class': '_1vC4OE _2rQ-NK'}).string
                rating = div.find('div', attrs={'class': 'hGSR34'})
                if rating:
                    rating = rating.contents[0]
                else:
                    rating = None
                imageUrl = div.find('img', attrs={'class': '_1Nyybr'})['src']
                
                if printText:
                    print(f'{itemName}\n{itemUrl}\n{specifications}\n{price}\n{imageUrl}\n{rating}\n\n')

                itemNameList.append(itemName)
                itemUrlList.append(itemUrl)
                specificationsList.append(specifications)
                priceList.append(price)
                ratingList.append(rating)
                imageUrlList.append(imageUrl)

            else:
                if div.find('div', attrs={'class': '_3liAhj'}):
                    if not grid_class:
                        itemNameList = []
                        itemUrlList = []
                        specificationsList = []
                        priceList = []
                        ratingList = []
                        imageUrlList = []

                    grid_class = '_3liAhj'
                    for col in div.find_all('div', attrs={'class': '_3liAhj'}):
                        
                        itemUrl = siteUrl + col.a['href']
                        itemName = col.find('a', attrs={'class': '_2cLu-l'}).string
                        specifications = col.find(
                            'div', attrs={'class': '_1rcHFq'})
                        if specifications:
                            specifications = specifications.string.split(', ')
                        else:
                            specifications = []
                        price = col.find('div', attrs={'class': '_1vC4OE'}).contents[0]
                        rating = col.find('div', attrs={'class': 'hGSR34'})
                        if rating:
                            rating = rating.contents[0]
                        else:
                            rating = None
                        imageUrl = col.find('img', attrs={'class': '_1Nyybr'})['src']

                        if printText:
                            print(f'{itemName}\n{itemUrl}\n{specifications}\n{price}\n{imageUrl}\n{rating}\n\n')

                        itemNameList.append(itemName)
                        itemUrlList.append(itemUrl)
                        specificationsList.append(specifications)
                        priceList.append(price)
                        ratingList.append(rating)
                        imageUrlList.append(imageUrl)

                elif div.find('div', attrs={'class': 'IIdQZO _1SSAGr'}):
                    if not grid_class:
                        itemNameList = []
                        itemUrlList = []
                        brandList = []
                        priceList = []
                        imageUrlList = []
                    
                    grid_class = 'IIdQZO _1SSAGr'
                    for col in div.find_all('div', attrs={'class': 'IIdQZO _1SSAGr'}):
                
                        itemUrl = siteUrl + col.a['href']
                        itemName = col.find('a', attrs={'class': '_2mylT6'}).string
                        brand = col.find('div', attrs={'class': '_2B_pmu'}).string
                        price = col.find('div', attrs={'class': '_1vC4OE'}).string
                        imageUrl = col.find('img', attrs={'class': '_3togXc'})['src']

                        if printText:
                            print(f'{itemName}\n{brand}\n{itemUrl}\n{price}\n{imageUrl}\n\n')

                        itemNameList.append(itemName)
                        itemUrlList.append(itemUrl)
                        brandList.append(brand)
                        priceList.append(price)
                        imageUrlList.append(imageUrl)
        currentPage += 1
        if currentPage <=  totalPages:
            driver.get(url + '&page=' + str(currentPage))
            content = driver.page_source
            soup = BeautifulSoup(content, 'html.parser')

    df = eval(grid_classes[grid_class]['cmd'])
    df.to_csv('SearchResults/'+query+'.csv', index=False, encoding='utf-8')

if __name__ == "__main__":
    main(sys.argv[1:])