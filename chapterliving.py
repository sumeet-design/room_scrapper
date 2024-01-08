from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select 
from faker import Faker 
import time
import csv


# saving data into csv file 

def scrape_data () :
    details_dict = {}
    fake = Faker('en_GB')
    data = {}
    data['login'] = {}  # {login :{ firys name :  , last_name},
    data['booking'] = {}
    data['login']['first_name'] = fake.first_name()
    data['login']['last_name'] = fake.last_name()
    data['login']['email'] = fake.email()
    data['login']['password'] = fake.password()
    data['login']['phone'] = fake.phone_number()[3:]
    # Initialize the Chrome driver
    driver = webdriver.Chrome()
    # Go to the webpage
    driver.get('https://www.chapter-living.com/booking/')
    # Find the dropdown menu and select the option
    dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'BookingAvailabilityForm_Residence')))
    d = Select(dropdown)
    for option in d.options:
        if option.text == 'CHAPTER KINGS CROSS':
            # print("yeee")
            option.click()
            break
    # Find the date input fields and fill them in
    time.sleep(2)
    from_date = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'BookingAvailabilityForm_BookingPeriod')))
    d = Select(from_date)
    for option2 in d.options:
        if option2.text == 'SEP 24 - AUG 25 (51 WEEKS)':
            # print("yeee2")
            option2.click()
            break
    driver.execute_script("window.scrollBy(0, 300)")
    time.sleep(2)
    # Submit the form
    get_ensuite = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'filter-room-type-ensuite')))
    get_ensuite.click()
    time.sleep(4)
    driver.execute_script("window.scrollBy(0, 600)")  # scrolls down by 500 pixels
    # Wait for the results page to load and get the room details
    room_details = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME , 'room-list-selection')))
    room_details.click()
    time.sleep(2)
    driver.execute_script("window.scrollBy(0, 1100)")
    time.sleep(2)
    cookie_accept = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'pc_banner_accept_all')))
    cookie_accept.click()
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
    # sus_clear_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sus-clear')))
    # print("lenght of sus",len(sus_clear_elements))
    # for element in sus_clear_elements :
    #     element_data = element.text.splitlines()
    #     data['booking'][element_data[0]] = element_data[1]
    #     print("this is data",data)
    #driver.quit()
    #return data
    # details_dict = {}
    
    #details_container = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'sus-unit-space-details')))
    details_containers = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sus-unit-space-details')))
    count = 0
    # Creating a list to store dictionaries of details for each element
    all_details = []
    # Iterate through each 'sus-unit-space-details' element
    for details_container in details_containers:
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
                space_status_details.append({"Space": space, "Status": status})
        #space = details_container.find_element(By.XPATH, ".//h6[text()='Unit Spaces']/following-sibling::table//td[3]").text
        #status = details_container.find_element(By.XPATH, ".//h6[text()='Unit Spaces']/following-sibling::table//td[4]").text
        payment_options = [option.text for option in details_container.find_elements(By.CSS_SELECTOR, ".payment-option-container ul.radio-group-list li span.value")]

        # Create a dictionary with the extracted details for each element
        details_dict = {
            "Space Value": space_value,
            "Building": building,
            "Rent": rent,
            "Deposit": deposit,
            "Amenities": amenities,
            # "Unit Spaces": unit_spaces,
            "Unit Spaces": space_status_details,
            #"Space": space,
            #"Status": status,
            "Payment Options": payment_options
        }
        all_details.append(details_dict)
        count = count + 1
        
    #print("this full dic details_dic",all_details)
    # combined_data = {
    #     "Signup Details": signup_details,
    #     "Unit Space Details": all_details  # All details collected from 'sus-unit-space-details' elements
    # }
    data['booking']['Unit Space Details'] =  all_details
# Print or use the dictionary as needed
    # print(detials_dict)
    return data

# my_data = scrape_data()
# print(my_data)