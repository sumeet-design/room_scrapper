from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
from selenium.webdriver.common.action_chains import ActionChains
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
    driver.maximize_window()  # Maximize the window
    driver.get('https://www.chapter-living.com/booking/')
    
    # Accept all cookies if the "Accept All Cookies" button is present
    try:
        accept_all_cookies_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
        accept_all_cookies_btn.click()
        print("Accepted all cookies.")
    except Exception as e:
        print("No 'Accept All Cookies' button found or unable to accept all cookies:", e)
    
    for chapter_name in CHAPTERS:
        print("Selecting chapter:", chapter_name)
        dropdown_chapters = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'BookingAvailabilityForm_Residence')))
        dropdown_chapters.click()
        
        for chapter_option in dropdown_chapters.find_elements(By.TAG_NAME, 'option'):
            if chapter_option.text.strip() == chapter_name:
                chapter_option.click()
                break
        time.sleep(2)  # Just for demonstration, you may remove this
        
        dropdown_periods = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'BookingAvailabilityForm_BookingPeriod')))
        dropdown_periods.click()
        
        for period_name in PERIODS:
            for period_option in dropdown_periods.find_elements(By.TAG_NAME, 'option'):
                if period_option.text.strip() == period_name:
                    print("Selecting period:", period_name)
                    period_option.click()
                    time.sleep(2)  # Just for demonstration, you may remove this
                    break
            try:
                print('i am trying for quick view.........', period_option.text)
                
                wait = WebDriverWait(driver, 10)
                buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button.btn.quick-view')))
                print('the buttons are : ', buttons)
                for button in buttons:
                    print('will click on ', button)
                    try:
                        # Use ActionChains to move to the element and click on it
                        actions = ActionChains(driver)
                        actions.move_to_element(button).click().perform()
                        
                        time.sleep(2)
                        info = get_modal_info(driver)
                        print('info: ', info)
                        print("view button clicked successfully")
                    except Exception as click_error:
                        print("Error clicking on button:", click_error)
            except Exception as error:
                print(error)
                
        # Scroll to the top of the page
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)  # Wait for scrolling to complete

    driver.quit()


def get_modal_info(driver):
    print('will start the function......... <--------')
    wait = WebDriverWait(driver, 10)
    name_element = wait.until(EC.presence_of_element_located((By.ID, 'apartmentModal-name')))
    room_type_element = wait.until(EC.presence_of_element_located((By.ID, 'apartmentModal-room')))
    price_range_element = wait.until(EC.presence_of_element_located((By.ID, 'apartmentModal-price')))
    description_element = wait.until(EC.presence_of_element_located((By.ID, 'apartmentModal-description')))
    features_list_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'features-list')))

    name = name_element.text.strip()
    room_type = room_type_element.find_element(By.TAG_NAME, 'strong').text.strip()
    price_range = price_range_element.find_element(By.TAG_NAME, 'strong').text.strip()
    description = description_element.text.strip()
    features = [li.text.strip() for li in features_list_element.find_elements(By.TAG_NAME, 'li')]

    print("Apartment Details:")
    print("Name:", name)
    print("Room Type:", room_type)
    print("Price Range:", price_range)
    print("Description:", description)
    print("Features:", features)
    print()

    carousel = wait.until(EC.presence_of_element_located((By.ID, 'apartmentModal-gallery')))
    image_elements = carousel.find_elements(By.XPATH, './/img')
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
