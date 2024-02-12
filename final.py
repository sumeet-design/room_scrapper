from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from faker import Faker
import time

CHAPTERS = ['CHAPTER ALDGATE', 'CHAPTER EALING']
PERIODS = ['SEP 24 - AUG 25 (51 WEEKS)', 'SEP 24 - JUL 25 (44 WEEKS)']

def scrape_data():
    fake = Faker('en_GB')
    data = {}
    data['login'] = {}
    data['booking'] = {}
    data['login']['first_name'] = fake.first_name()
    data['login']['last_name'] = fake.last_name()
    data['login']['email'] = fake.email()
    data['login']['password'] = fake.password()
    data['login']['phone'] = fake.phone_number()[3:]
    driver = webdriver.Chrome()
    driver.get('https://www.chapter-living.com/booking/')
    
    for chapter_name in CHAPTERS:
        print("Selecting chapter:", chapter_name)
        dropdown_chapters = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'BookingAvailabilityForm_Residence')))
        actions = ActionChains(driver)
        actions.move_to_element(dropdown_chapters).perform()
        driver.execute_script("arguments[0].click();", dropdown_chapters)
        
        chapter_options = dropdown_chapters.find_elements(By.TAG_NAME, 'option')
        for chapter_option in chapter_options:
            if chapter_option.text.strip() == chapter_name:
                chapter_option.click()
                break
        time.sleep(2)  # Just for demonstration, you may remove this
        
        dropdown_periods = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'BookingAvailabilityForm_BookingPeriod')))
        actions = ActionChains(driver)
        actions.move_to_element(dropdown_periods).perform()
        driver.execute_script("arguments[0].click();", dropdown_periods)
        
        period_options = dropdown_periods.find_elements(By.TAG_NAME, 'option')
        for period_name in PERIODS:
            for period_option in period_options:
                if period_option.text.strip() == period_name:
                    print("Selecting period:", period_name)
                    period_option.click()
                    time.sleep(2)  # Just for demonstration, you may remove this
                    break

                try:
                    print('i am trying for quick fiew.........', period_option.text)
                    
                    # driver.execute_script("window.scrollBy(0, 600)")
                    # Wait for the relevant elements to load
                    wait = WebDriverWait(driver, 10)
                    # Find all buttons with class 'btn quick-view'
                    buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button.btn.quick-view')))
                    print('the buttons are : ', buttons)
                    # Click on each button
                    for button in buttons:
                        print('will click on ', button)
                        driver.execute_script("arguments[0].scrollIntoView(true);", button)
                        # button.click()
                        driver.execute_script("arguments[0].click();", button)
                        time.sleep(2)
                        info = get_modal_info(driver)
                        print('info: ', info)
                        # scrape (to be written)
                        
                
                # pass
                except Exception as error:
                    print(error)

        time.sleep(2)  # Just for demonstration, you may remove this

    driver.quit()


def get_modal_info(driver):
        
    # Load the webpage
    # driver.get("URL_OF_THE_PAGE")

    # Wait for the relevant elements to load
    print('will start the function......... <--------')
    wait = WebDriverWait(driver, 10)

    # Find the apartment details
    name_element = wait.until(EC.presence_of_element_located((By.ID, 'apartmentModal-name')))
    room_type_element = wait.until(EC.presence_of_element_located((By.ID, 'apartmentModal-room')))
    price_range_element = wait.until(EC.presence_of_element_located((By.ID, 'apartmentModal-price')))
    description_element = wait.until(EC.presence_of_element_located((By.ID, 'apartmentModal-description')))
    features_list_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'features-list')))

    # Extract information
    name = name_element.text.strip()
    room_type = room_type_element.find_element(By.TAG_NAME, 'strong').text.strip()
    price_range = price_range_element.find_element(By.TAG_NAME, 'strong').text.strip()
    description = description_element.text.strip()
    features = [li.text.strip() for li in features_list_element.find_elements(By.TAG_NAME, 'li')]

    # Print the apartment details
    print("Apartment Details:")
    print("Name:", name)
    print("Room Type:", room_type)
    print("Price Range:", price_range)
    print("Description:", description)
    print("Features:", features)
    print()

    # Find the carousel
    carousel = wait.until(EC.presence_of_element_located((By.ID, 'apartmentModal-gallery')))

    # Find all image elements within the carousel
    image_elements = carousel.find_elements(By.XPATH, './/img')

    # Extract image links
    image_links = [img.get_attribute('src') for img in image_elements]
    info = {
        'images': image_links,
        'roomName': name,
        'price': price_range,
        'description': description,
        'features': features
    }
    return info

scrape_data()
