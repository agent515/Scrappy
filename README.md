# Scrappy

A web-scraper that parses through flipkart web-site based on the user's search query.
Then fetches the important product details and saves them in the `<search-query>.csv` file in SearchResults folder by default.
<hr>

## How to Run Scrappy

**Clone the repositories**<br>
`git clone https://github.com/agent515/Scrappy.git`

**Install the dependencies**<br>
`pip install -r requirements.txt`

**Download Chrome Webdriver**<br>
[chromedriver](https://chromedriver.chromium.org/downloads)
> **_NOTE:_**  Make sure version of chromedriver is higher than Google Chrome's version. If unsure download the latest webdriver version and update the Chrome browser.
Update the path of executable or binary file in webdriver.Chrome() [web-scraping-flipkart.py](/web-scraping-flipkart.py), if required.

**Finally, Run the file**<br>
> python web-scraping-flipkart.py [OPTIONS]

### Example

_Pairs of Shoes are never enough.. So, let's find our options on flipkart_

![](/images/search.png =500x)

![](/images/search-result.png =500x)

![](/images/csvGeneratedFile.PNG =250x)

![](/images/csvFile.PNG =750x)

### options
> -a : about the util<br>
> -h : help<br>
> -l : limit option setting the maximum no. of pages to parse. Default is 10.<br>
> -p : print the product details in the CLI. Default is False.<br>

## Future Scope
1. Extending support for other shopping sites like amazon, myntra, etc.
2. Recommending the the best products from all the sites.
3. GUI

:sparkles: Happy Scraping!! :octocat:
