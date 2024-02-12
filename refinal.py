import json
from faker import Faker
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import pandas as pd
from selenium.common.exceptions import InvalidSessionIdException
from selenium.common.exceptions import NoSuchElementException
import traceback





def scrape_data(chapter_property, chapter_time):
    print("I am started scraping successfully.......")
    fake = Faker('en_GB')

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    # Create Chrome WebDriver options
    chrome_options = Options()

    # Add the user-agent string to the options
    chrome_options.add_argument(f'user-agent={user_agent}')

    # Initialize Chrome WebDriver with the options
    driver = webdriver.Chrome(options=chrome_options)
    #driver = webdriver.Chrome()

    try:
        driver.get('https://www.chapter-living.com/booking/')

        dropdown_residence = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'BookingAvailabilityForm_Residence'))
        )
        select_residence = Select(dropdown_residence)
        select_residence.select_by_visible_text(chapter_property)

        time.sleep(3)

        dropdown_period = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'BookingAvailabilityForm_BookingPeriod'))
        )
        select_period = Select(dropdown_period)
        select_period.select_by_visible_text(chapter_time)

        time.sleep(3)

        # Get page source after selecting options
        page_source = driver.page_source

        # Use BeautifulSoup to parse the page source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find all room divs
        room_divs = soup.find_all('div', class_='col-12 col-md-6 sp-room-wrapper')

        results = []
        apply_driver = []
        for room_div in room_divs:
            print("I am inside room div")
            # Scrape data from room div
            property_name = room_div.find(class_='property').get_text(strip=True)
            room_type = room_div.find(class_='display-4').strong.get_text(strip=True)
            description = room_div.find(class_='description').get_text(strip=True)
            pricing_range = room_div.find(class_='pricing').strong.get_text(strip=True)
            image_list = []
            image_urls = room_div.find('img')['src'] #tied chaning here
            #for image_url in image_urls:
             #   image_list.append(image_url)

            #adding category filed also
            
            category = room_type.split()[-1]

            apply_button = driver.find_element(By.CSS_SELECTOR, 'a.btn.has-bg.btn-black.ms-auto.room-list-selection')
            apply_button.click()
            print("Apply button runs successfully...")
    except :
        pass

if __name__ == "__main__":
    property_chapters = ['CHAPTER ALDGATE', 'CHAPTER EALING', 'CHAPTER HIGHBURY', 'CHAPTER HIGHBURY II', 'CHAPTER ISLINGTON', 'CHAPTER KINGS CROSS', 'CHAPTER LEWISHAM', 'CHAPTER OLD STREET', 'CHAPTER PORTOBELLO', 'CHAPTER SOUTH BANK', 'CHAPTER SPITALFIELDS', 'CHAPTER WESTMINSTER', 'CHAPTER WHITE CITY']
    periods = ['SEP 24 - AUG 25 (51 WEEKS)','SEP 24 - JUL 25 (44 WEEKS)']

    all_results = []

    for period in periods:
        
        results = scrape_data('CHAPTER WHITE CITY', period)
        #all_results.extend(results)

    print("Finall data is here................................................")    
    # Convert the results to JSON
    json_results = json.dumps(all_results, indent=4)
    print(json_results)