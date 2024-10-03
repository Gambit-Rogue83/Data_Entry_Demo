from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import time


GOOGLE_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSeOESpu9kb9k9poBDxtgLY0PtIbDyBlvQ1_YBeSCCkM6KNpjw/viewform?usp=sf_link"

ZILLOW_CLONE_SITE = "https://appbrewery.github.io/Zillow-Clone/"

response = requests.get(ZILLOW_CLONE_SITE)

soup = BeautifulSoup(response.text, "html.parser")

# Property Links
property_links = soup.find_all(name="a", class_="StyledPropertyCardDataArea-anchor")
links = [link['href'] for link in property_links]


# Property Rental Price
property_prices = soup.find_all(name="span", class_="PropertyCardWrapper__StyledPriceLine")
rent = [price.getText().replace("/mo", "").split("+")[0] for price in property_prices if "$" in price.text]


# Property Address
property_locations = soup.find_all(name="address")
rental_addresses = [address.getText().replace(" | ", "").strip() for address in property_locations]

# GOOGLE FORM AUTOMATION

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

for n in range(len(links)):
    driver.get(GOOGLE_FORM)
    time.sleep(2)
    address = driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input")
    price = driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input")
    link = driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input")

    button = driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[3]/div[1]/div[1]/div")

    address.send_keys(rental_addresses[n])
    price.send_keys(rent[n])
    link.send_keys(links[n])
    button.click()








