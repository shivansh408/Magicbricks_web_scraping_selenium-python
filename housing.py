from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Install Browser driver before running the code
driver = webdriver.Firefox()

# Url on which web scraping has to be done
url = "https://www.magicbricks.com/property-for-sale/residential-real-estate?&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName=Mumbai"
driver.get(url)
parentGUID = driver.current_window_handle

a_price = []
a_headline = []
a_super_area = []
a_floor = []
a_society = []

def scroll(driver, timeout, t):
    scroll_pause_time = timeout
    scroll_times = t

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    for k in range(scroll_times):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If heights are the same it will exit the function
            break
        last_height = new_height

try:
    scroll(driver, 5, 334)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "[@class='autosuggest-overlay show']"))).click()
    card = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "mb-srp__card")))
    time.sleep(5)
    for i in range(20):
        card[i].click()
        allGUID = driver.window_handles
        for guid in allGUID:
            if guid != parentGUID:
                driver.switch_to.window(guid)
                # Price
                try:
                    price = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "mb-srp__card__price")))
                    a_price.append(price.text[2:])
                except:
                    a_price.append('NA')

                # Headline
                try:
                    headline = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "mb-srp__card--title")))
                    a_headline.append(headline.text)
                except:
                    a_headline.append('NA')

                # Super area
                try:
                    sa = driver.find_element_by_xpath("//*[contains(text(), 'Carpet area')]")
                    sa_n = driver.find_element_by_xpath("//*[contains(text(), 'Carpet area')]/following-sibling::div")
                    a_super_area.append(sa_n.text)
                except:
                    a_super_area.append("NA")

                # Floor
                try:
                    flr = driver.find_element_by_xpath("//*[contains(text(), 'Floor')]")
                    flr_n = driver.find_element_by_xpath("//*[contains(text(), 'Floor')]/following-sibling::div")
                    a_floor.append(flr_n.text)
                except:
                    a_floor.append("NA")

                try:
                    so = driver.find_element_by_xpath("//*[contains(text(), 'Society')]")
                    so_n = driver.find_element_by_xpath("//*[contains(text(), 'Society')]/following-sibling::div")
                    a_society.append(so_n.text)
                except:
                    a_society.append("NA")

                driver.close()
                driver.switch_to.window(parentGUID)

finally:
    driver.quit()

df = pd.DataFrame(list(
    zip(a_society, a_headline, a_super_area, a_floor, a_price)),
                  columns=['Project name', 'Specifications(BHK)', 'area', 'Floor', 'Value'])

unplan_magic_bricks_mumbai = df.to_csv('magicbrick_data.csv', index=False)