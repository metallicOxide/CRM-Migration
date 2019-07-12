import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pyautogui
import pandas as pd
import payload

LOGIN_URL = 'https://auzone1.nookal.com/v2.0/auth/login'
PROFILE_URL = 'https://auzone1.nookal.com/v2.0/clients/profile/1/'
ABS_URL = 'https://auzone1.nookal.com'

def login(driver):
    # driver object persists session
    driver.find_element_by_id('login-company').send_keys(payload.company)
    driver.find_element_by_id('login-email').send_keys(payload.email)
    driver.find_element_by_id('login-password').send_keys(payload.password)
    driver.find_element_by_class_name('button').click()
    # sleep for 10 second to ensure website loads
    time.sleep(10)

def read_client_ids():
	df = pd.read_excel ('client_ids.xlsx') # csv qill not work if we are trying to read by column name. Use .xlsx for now
	# Returns an array of client IDs
	return df['ClientID']

# finds complete url of notes given authenticated session and 
# patient url
def find_cases(driver, url):
    cases = []
    # driver.get(url) gets the url
    driver.get(url)
    # driver.page source gives you back the html source of web tab
    htmlSrc = driver.page_source
    soup = BeautifulSoup(htmlSrc, 'html.parser')
    # finds all div tags with id = 'submenu-clinical'
    div_tag = soup.find('div', attrs = {'id':'submenu-clinical'})
    # in beautiful soup, things like href = 'link'
    # will be saved as tuples where href is primiary key
    rel_url = div_tag.find_all("a")
    if rel_url[0].text == " Create New Case":
        return None
    # build complete url
    for url in rel_url:
        complete_url = ABS_URL + url['href']
        cases.append(complete_url)
    return cases

# counts number of Nookal notes given page source
def num_notes(src):
    soup = BeautifulSoup(src, 'html.parser')
    all_notes_html = soup.find_all('div', attrs = {'class':'clinical-history-note padding-small'})
    return len(all_notes_html)

def click_print(driver, url):
    driver.get(url)
    notes_count = num_notes(driver.page_source)
    print("Number of notes is: " + str(notes_count))
    if notes_count > 0:
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="clinical-history-footer"]/button[2]').click()
        time.sleep(2)
        driver.find_element_by_id('modal-continue').click()
    # time.sleep(2)
    # print("move yo mouse")
    # print(pyautogui.position())
    return notes_count

def save_to_file(wait_time, trail, id):
    save_path = "K:\lol"
    time.sleep(2)
    # print(pyautogui.position())

    # click print
    pyautogui.moveTo(x=1479, y=911, duration=0.25)
    pyautogui.click()
    time.sleep(2)

    # select printer
    pyautogui.moveTo(x=317, y=378, duration=0.25)
    pyautogui.click()
    time.sleep(0.3)
    pyautogui.moveTo(x=317, y=453, duration=0.25)
    pyautogui.click()
    time.sleep(wait_time)

    # press save button
    pyautogui.moveTo(x=326, y=295, duration=0.25)
    pyautogui.click()
    time.sleep(3)

    # change save name
    pyautogui.moveTo(x=209, y=857, duration=0.25)
    pyautogui.click()
    pyautogui.typewrite(str(id) + ".")
    time.sleep(1)
    if trail > 0:
        pyautogui.moveTo(x=1024, y=860, duration=0.25)
        pyautogui.click()
        pyautogui.typewrite(str(trail))

    # change save location
    pyautogui.moveTo(x=700, y=72, duration=0.25)
    pyautogui.click()
    time.sleep(2)
    pyautogui.typewrite(save_path)
    pyautogui.typewrite(["enter"])
    time.sleep(2)

    # save
    pyautogui.moveTo(x=1634, y=965, duration=0.25)
    pyautogui.click()
    time.sleep(2)


if __name__ == '__main__':
    # initalized driver
    # driver = webdriver.Chrome('/mnt/c/webdriver/chromedriver.exe')
    driver = webdriver.Chrome('C:\webdriver\chromedriver.exe')
    driver.get(LOGIN_URL)
    client_ids = read_client_ids()
    # uncomment to hardcode client IDs for testing
    # client_ids = ['12']
    # ___________________________________________
    login(driver)
    for id in client_ids:
        id = int(id)
        client_URL = PROFILE_URL + str(id)
        case_urls = find_cases(driver, client_URL)
        if case_urls == None:
            continue
        print(case_urls)
        seen = []
        trail = 0
        for url in case_urls:
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            title = soup.find('h2', attrs={'class':'margin-top-xxsmall text-nowrap overflow-ellipsis float-left'}).text
            print(title)
            if title in seen:
                trail = trail + 1
            else:
                seen.append(title)
            notes_count = click_print(driver, url)
            if notes_count > 0:
                save_to_file(notes_count/2, trail, id)


    

        
        


