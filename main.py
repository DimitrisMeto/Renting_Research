from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

chrome_driver_path = "/Users/dimitris/Development/chromedriver"
GOOGLE_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSfwV6JY7kEg2o3VLGYMsUIjTf4FfI8FCxzRfxZP_nQKkXwA4A/viewform?usp=sf_link"
URL = "https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.63039626074219%2C%22east%22%3A-122.23626173925781%2C%22south%22%3A37.61609832720608%2C%22north%22%3A37.93414253184545%7D%2C%22mapZoom%22%3A11%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"

HEADERS = {
    "Accept-Language": "en-GB,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15"
}

response = requests.get(url=URL, headers=HEADERS).text
soup = BeautifulSoup(response, "html.parser")


listings = soup.select(".ListItem-c11n-8-85-1__sc-10e22w8-0 a")
# print(listings)
# print(len(listings))

links = []

for listing in listings:
    href = listing["href"]
    # print(href)

    if "https" not in href:
        links.append(f"https://www.zillow.com/{href}")
    else:
        links.append(href)


final_links = links[::2]

prices = soup.select(".ListItem-c11n-8-85-1__sc-10e22w8-0 div.bqsBln span")
new_prices = [price.get_text().split("+")[0] for price in prices]
# print(prices)
# print(new_prices)

addresses = soup.select(".ListItem-c11n-8-85-1__sc-10e22w8-0 a address")
new_addresses = [address.get_text() for address in addresses]
print(new_addresses)

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

chrome_driver = webdriver.Chrome(service=Service(chrome_driver_path, options=options))

for n in range(len(final_links)):
    chrome_driver.get(GOOGLE_FORM)

    time.sleep(2)
    inputs = chrome_driver.find_elements(By.CSS_SELECTOR, "div.Xb9hP input")
    address_input = inputs[0]
    price_input = inputs[1]
    link_input = inputs[2]
    submit_button = chrome_driver.find_element(By.CSS_SELECTOR, "div.Y5sE8d")

    address_input.send_keys(new_addresses[n])
    price_input.send_keys(new_prices[n])
    link_input.send_keys(final_links[n])
    submit_button.click()
