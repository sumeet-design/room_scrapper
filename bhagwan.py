from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import json

CHAPTERS = ['CHAPTER ALDGATE']
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

    # Setting up Chrome WebDriver options
    opt = webdriver.ChromeOptions()
    # opt.add_argument("--enable-javascript")
    # opt.add_argument("--enable-cookies")
    # opt.add_argument("--disable-blink-features=AutomationControlled")
    # opt.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
   # prefs = {"profile.default_content_setting_values.notifications": 2,#
        #    "profile.default_content_setting_values.geolocation": 2}
    #opt.add_experimental_option("prefs", prefs)
    #opt.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
    opt.add_argument("user-data-dir=C://Users//91738//AppData//Local//Google//Chrome//chapter_living")

    driver = webdriver.Chrome(options=opt)
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
        filenames = ['chapterEaling1.txt', 'chapterEaling2.txt'] 
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
                
                #wait = WebDriverWait(driver, 10)
                #buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button.btn.quick-view')))
                #print('the buttons are : ', buttons)
                # for button in buttons:
                #     print('will click on ', button)
                #     count = 1
                #     #try:
                #     time.sleep(6)
                #     # Use ActionChains to move to the element and click on it
                #     actions = ActionChains(driver)
                #     time.sleep(1)
                #     actions.move_to_element(button).click().perform()
                    
                #     time.sleep(2)
                #     info = get_modal_info(driver)
                    #print('info: ', info)
                    #print("view button clicked successfully")

                    # closing this because I already have in get_modal_info
                    # time.sleep(1)
                    # driver.execute_script("document.querySelector('button.btn-close').click();")
                    # time.sleep(1)
                # get links
                print('will look for this file: ', filenames[i])
                links = get_link_from_file(filenames[i])
                for link in links:
                    try:
                        # now working for apply click button
                        # Find and click the "Apply" button using JavaScript
                        time.sleep(2)
                        # Find and click the "Apply" button using JavaScript
                        #apply_button = driver.find_element(By.CSS_SELECTOR, 'a.room-list-selection')
                        driver = webdriver.Chrome()
                        driver.maximize_window()  # Maximize the window
                        # get link from file
                        driver.get(link)
                        #driver.execute_script("arguments[0].click();", apply_button)
                        #driver.get()
                        time.sleep(2)  # Wait for the page to load after clicking "Apply"
                        #print("Apply button clicked successfully")


                        
                        #addding login functionality here....


                        time.sleep(2)
                        driver.execute_script("window.scrollBy(0, 1100)")
                        time.sleep(2)
                        try:
                            cookie_accept = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'pc_banner_accept_all')))
                            cookie_accept.click()
                        except:
                            print("Cookie is not availabe")
                        # Close the browser
                        first_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'applicant_first_name')))
                        first_name.send_keys(data['login']['first_name'])
                        last_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'applicant_last_name')))
                        last_name.send_keys(data['login']['last_name'])
                        phone_number = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'phone_numbers[0][phone_number]-base')))
                        phone_number.send_keys(data['login']['phone'])
                        email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'applicant_username')))
                        email.send_keys(data['login']['email'])
                        password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'applicant_password')))
                        password.send_keys(data['login']['password'])
                        confirm_password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'applicant_password_confirm')))
                        confirm_password.send_keys(data['login']['password'])
                        agg_to_terms = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'agrees_to_terms')))
                        agg_to_terms.click()
                        time.sleep(2)
                        driver.execute_script("window.scrollBy(0, 100)") 
                        submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'create-app-btn')))
                        submit_button.click()
                        i_agree = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'js-confirm')))
                        i_agree.click()
                        driver.execute_script("window.scrollBy(0, 1000)") 
                        #print("Login details entered successfully......")

                        #scrolling to get  element .....
                        # Scroll to the bottom of the page
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        details_containers = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sus-unit-space-details')))
                        count = 0
                        #scraping floorPlan map url
                        floorplan_link = driver.find_element(By.CSS_SELECTOR, 'div[style="margin-bottom: 20px"] a')

                        
                        floorplan_url = floorplan_link.get_attribute('href')
                        print('will try to get floor plan link =.............> ', floorplan_url)
                        # Creating a list to store dictionaries of details for each element
                        all_details = []
                        # Iterate through each 'sus-unit-space-details' element
                        for details_container in details_containers:
                            print('*********details container: *****', details_container)
                            space_value = details_container.find_element(By.XPATH, ".//h6").text

                            building = details_container.find_element(By.XPATH, ".//dd[preceding-sibling::dt[text()='Building']]").text
                            rent = details_container.find_element(By.XPATH, ".//dd[preceding-sibling::dt[text()='Rent']]").text
                            deposit = details_container.find_element(By.XPATH, ".//dd[preceding-sibling::dt[text()='Deposit']]").text
                            amenities = details_container.find_element(By.XPATH, ".//dd[preceding-sibling::dt[text()='Amenities']]").text
                            # unit_spaces = details_container.find_element(By.XPATH, ".//h6[text()='Unit Spaces']/following-sibling::table//td[2]").text
                            unit_spaces_element = details_container.find_element(By.XPATH, ".//h6[text()='Unit Spaces']/following-sibling::table")
                        
                            # Extract space and status details from the 'Unit Spaces' table
                            
                            space_status_details = []
                            rows = unit_spaces_element.find_elements(By.TAG_NAME, 'tr')

                            for row in rows:
                                cells = row.find_elements(By.TAG_NAME, 'td')
                                if len(cells) == 3:  # Ensure the row contains necessary data (3 cells)
                                    space = cells[1].text.strip()
                                    status = cells[2].text.strip()
                                    space_status_details.append({"space": space, "status": status})
                            #space = details_container.find_element(By.XPATH, ".//h6[text()='Unit Spaces']/following-sibling::table//td[3]").text
                            #status = details_container.find_element(By.XPATH, ".//h6[text()='Unit Spaces']/following-sibling::table//td[4]").text
                            payment_options = [option.text for option in details_container.find_elements(By.CSS_SELECTOR, ".payment-option-container ul.radio-group-list li span.value")]

                            # Create a dictionary with the extracted details for each element
                            details_dict = {
                                #"Space Value": space_value,
                                "building": building,
                                "rent": rent,
                                "deposit": deposit,
                                "amenities": amenities,
                                # "Unit Spaces": unit_spaces,
                                "unitSpaces": space_status_details,
                                #"Space": space,
                                #"Status": status,
                                "paymentPlanOption": payment_options
                            }
                            print("This is detail dic",)
                            all_details.append(details_dict)
                        #print("All details",all_details)

                        #combining to final data format
                        info['floorPlanUrl'] = floorplan_url
                        info['apartments'] = all_details
                        print(f"Full Property level data of Chapter{chapter_name}")
                        #driver.back()
                        # Navigate back using keyboard shortcut (Alt + Left Arrow)
                        #driver.find_element(By.TAG_NAME,'body').send_keys(Keys.ALT + Keys.LEFT)
                        
                        time.sleep(5)
                        # driver.back()
                        
                        # Press Alt + Left Arrow to go back
                        driver.back()
                        # driver.execute_script("window.history.go(-1)")
                        # #print("Stuck in loading page -1..........")

                        time.sleep(2)
                        # Press Alt + Left Arrow to go back
                        driver.back()
                        
                        # driver.execute_script("window.history.go(-1)")
                            
                        #time.sleep(5)
                        #print("Stuck in loading page..........")
                        time.sleep(2)
                        #driver.back()
                        print("Successfully completed Scraping  ....")
                    except Exception as click_error:
                        print("Error clicking on button:", click_error)
            except Exception as error:
                print(error)
                                    
                        #     # Scroll to the top of the page
                        #     driver.execute_script("window.scrollTo(0, 0);")
                        #     time.sleep(1)  # Wait for scrolling to complete

                        # driver.quit()

    #saving complete data to json
    file_path = "chapterAldgate.json"
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)   
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
        'galleryLink': image_links,
        'roomName': name,
        'price': price_range,
        'description': description,
        'features': features
        #'duration': duration
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
    with open(filename, 'r') as eye:
        lines = eye.readlines()
    links = [line.rstrip('\n') for line in lines]


    return links 

scrape_data()
