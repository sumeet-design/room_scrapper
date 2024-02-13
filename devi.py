from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import json

CHAPTERS = ['CHAPTER HIGHBURY']
PERIODS = ['SEP 24 - AUG 25 (51 WEEKS)', 'SEP 24 - JUL 25 (44 WEEKS)']

def scrape_data():
    
    #opt = webdriver.ChromeOptions()

    #opt.add_argument("user-data-dir=C://Users//91738//AppData//Local//Google//Chrome//chapter_living")

    driver = webdriver.Chrome()
    driver.maximize_window()  # Maximize the window
    driver.get('https://www.chapter-living.com/booking/')
    
    # Accept all cookies if the "Accept All Cookies" button is present
    time.sleep(4)
    try:
        accept_all_cookies_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
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
        for i, period_name in enumerate(PERIODS):
            for period_option in dropdown_periods.find_elements(By.TAG_NAME, 'option'):
                if period_option.text.strip() == period_name:
                    duration = period_name
                    print("Selecting period:", period_name)
                    period_option.click()
                    time.sleep(2)  # Just for demonstration, you may remove this
                    break
            try:
                print('i am trying for quick view.........', period_option.text)
                
                wait = WebDriverWait(driver, 10)
                buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button.btn.quick-view')))
                key = f'{chapter_option.text}-{period_option.text}'
                combine_info = {key: []}
                for button in buttons[:2]:
                    print('will click on ', button)
                    #try:
                    time.sleep(6)
                    # Use ActionChains to move to the element and click on it
                    actions = ActionChains(driver)
                    time.sleep(1)
                    actions.move_to_element(button).click().perform()
                    
                    time.sleep(2)
                    info = get_modal_info(driver)
                    print("view button clicked successfully")
                    #updating info dic with duration
                    info['duration'] = duration
                    combine_info[key].append(info)
                print('the combined info is ', combine_info)
                write_to_file(dictionary=combine_info, filename=f'{key}.quick_view.json')
                    
                # get links
                #print('will look for this file: ', filenames[i])
                #links = get_link_from_file(filenames[i])
                #combined_apartment = []
               #Combine all data 
                        
                #combine_details(combine_info,combined_apartment, filename=f'{chapter_option.text}-{period_option.text}')
                #return combine_details
            
            
            except Exception as error:
                print(error)
                                    
    
    
    print("Data saved Successfully......................................")         
def get_modal_info(driver):
    print('will start the function......... <--------')
    time.sleep(2)
    wait = WebDriverWait(driver, 10)
    name_element = wait.until(EC.presence_of_element_located((By.ID, 'apartmentModal-name')))
    room_type_element = wait.until(EC.presence_of_element_located((By.ID, 'apartmentModal-room')))
    price_range_element = wait.until(EC.presence_of_element_located((By.ID, 'apartmentModal-price')))
    description_element = wait.until(EC.presence_of_element_located((By.ID, 'apartmentModal-description')))
    features_list_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'features-list')))
    #features_list_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'features-list mb-3')))

    name = name_element.text.strip()
    room_type = room_type_element.find_element(By.TAG_NAME, 'strong').text.strip()
    price_range = price_range_element.find_element(By.TAG_NAME, 'strong').text.strip()
    description = description_element.text.strip()
    features = [li.text.strip() for li in features_list_element.find_elements(By.TAG_NAME, 'li')]

    

    carousel = wait.until(EC.presence_of_element_located((By.ID, 'apartmentModal-gallery')))
    image_elements = carousel.find_elements(By.XPATH, './/img')
    image_links = [img.get_attribute('src') for img in image_elements]
    info = {
        'galleryLink': image_links,
        'roomName': name,
        'price': price_range,
        'description': description,
        'features': features,
        # 'duration': duration,
        
    }
    # Find the close button and click on it
    # close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn-close')))
    # close_button.click()
    time.sleep(2)
    driver.execute_script("document.querySelector('button.btn-close').click();")
    time.sleep(1)
    return info

def get_link_from_file(chapter_period):
    filename = 'chapterEaling1.txt'
    with open(chapter_period, 'r') as eye:
        lines = eye.readlines()
    links = [line.rstrip('\n') for line in lines]


    return links 

def write_to_file(dictionary, filename):
    print('writing to file....')
    with open(filename, 'w') as fp:
        json.dump(dictionary, fp)


def combine_details(quick_view_data,apply_button_data, filename):
    combined_data = {'QuickView': quick_view_data, 'ApplyData': apply_button_data}
    with open(filename, 'w') as fp:
        json.dump(combined_data, fp)
    return combined_data
    if len(quick_view_data)== len(apply_button_data):
        print("Data is consistant and we are good to go..")
        for i in range(len(quick_view_data)):
            room_data = quick_view_data[i]
            apply_data = apply_button_data[i]

            room_data['apartment'] = apply_data
        return quick_view_data
    else:
        return "Data is incosistant"

property_data = scrape_data()
# Serialize property_data with custom serialization function
# serialized_data = json.dumps(property_data)
#saving complete data to json
print("this is property data",property_data)
file_path = "chapterHighbury.json"
json_results = json.dumps(property_data,indent=4)
file_path_t = "chapterHighbury.txt"
with open(file_path_t, 'w') as text_file:
    text_file.write(property_data)
with open(file_path, 'w') as json_file:
    json_file.write(json_results)   
print("File Saved Successfully.........")