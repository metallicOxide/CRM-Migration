import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time, datetime
import os
import pandas as pd
import re
import loginCredentials

LOGIN_URL = 'https://auzone1.nookal.com/v2.0/auth/login'
PROFILE_URL = 'https://auzone1.nookal.com/v2.0/clients/profile/1/'
ABS_URL = 'https://auzone1.nookal.com'
DOCUMENT_BASE_URL = 'https://auzone1.nookal.com/v2.0/clients/profile/1/'
# NEED TO CHANGE THIS SO IT'S COMPATITABLE WITH OTHER SYSTEMS (IE JERRY LU PART)

###################### these needs changing ################################
DOWNLOAD_FOLDER_PATH = "C:\\Users\\jerry lu\\Downloads\\QLDDocs"
CLIENT_ID_DOCUMENT = 'test_client_ids.xlsx'
CHROME_DOWNLOAD = "C:\\Users\\jerry lu\\Downloads"
############################################################################

def login(driver, waitTime):
    # driver object persists session
    driver.find_element_by_id('login-company').send_keys('login-domain')
    driver.find_element_by_id('login-email').send_keys('login-email')
    driver.find_element_by_id('login-password').send_keys('login-password')
    driver.find_element_by_class_name('button').click()
    # sleep for 10 second to ensure website loads
    time.sleep(waitTime)

def read_client_ids():
    df = pd.read_excel (CLIENT_ID_DOCUMENT) # csv qill not work if we are trying to read by column name. Use .xlsx for now
	# Returns an array of client IDs
    return df['ClientID']

# def getDocumentLink(driver, clientURL):
#     driver.get(clientURL)
#     # driver.page source gives you back the html source of web tab
#     htmlSrc = driver.page_source
#     soup = BeautifulSoup(htmlSrc, 'html.parser')
#     div_tag_arr = soup.find_all('a')
#     # in beautiful soup, things like href = 'link'
#     # will be saved as tuples where href is primiary key
#     print(div_tag_arr)
#     return div_tag_arr[4]['href']


def generateXPATH(filePosition, numFolder):
    basePath = '//*[@id="client-documents"]/div[1]/div[1]/div/ul/li['
    return basePath + str(numFolder + filePosition) + ']'

def downloadDocs(driver, client_URL, DOC_URL):
    # clicks on documents link
    driver.get(client_URL)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="menu-left"]/div/div/a[6]').click()

    # counts number of folder and files
    htmlSrc = driver.page_source
    soup = BeautifulSoup(htmlSrc, 'html.parser')
    folderList = soup.find_all('li', attrs = {'class':'jqtree_common jqtree-folder jqtree-closed jqtree-type-case'})
    numFolder = len(folderList)
    print('number of folders: ' + str(numFolder))
    downloadList = soup.find_all('li', attrs = {'class':'jqtree_common jqtree-type-file'})
    numFiles = len(downloadList)
    letterList = soup.find_all('li', attrs = {'class':'jqtree_common jqtree-type-letter'})
    downloadList.extend(letterList)
    numFiles += len(downloadList)
    print('number of documents: ' + str(numFiles))
    # print(downloadList)

    # early termination if no files
    if numFiles == 0:
        return

    downloaded = []
    # checks if there are files in folders
    # chucks an exeception if there is
            
    documents = driver.find_elements_by_css_selector("li[class='jqtree_common jqtree-type-file']")
    letters = driver.find_elements_by_css_selector("li[class='jqtree_common jqtree-type-letter']")
    documents.extend(letters)
    print(len(documents))
    print(documents)

    avoidList = ['MSG', 'XML']
    for element in documents:
        try:
            if element not in downloaded:
                fileType = element.find_element_by_xpath(".//span[@class='text-help']").text.split("-")[0].strip().split(" ")[0]
                print(fileType)
                if fileType in avoidList:
                    f=open("FileError.txt", "a+")
                    f.write("ClientID: {0}, {1}\n".format(id, fileType))
                    f.close()
                    continue
                element.click()
                downloaded.append(element)
                time.sleep(0.8)
                # print(driver.find_element_by_xpath('//*[@id="menu-right"]/div/div/div/ul[1]/li[2]/a').text)

                if driver.find_element_by_xpath('//*[@id="menu-right"]/div/div/div/ul[1]/li[2]/a').text == 'Download':
                    driver.find_element_by_xpath('//*[@id="menu-right"]/div/div/div/ul[1]/li[2]/a').click()
                else:
                    driver.find_element_by_xpath('//*[@id="menu-right"]/div/div/div/ul[1]/li[1]/a').click()
                time.sleep(1.3)
                # time.sleep(0.8)
                # element.find_element_by_class_name("selectable-input").click()
        except Exception as e:
            print("failed to scrap:" + element.text)
            print(e)
            continue

    for folder in folderList:
        folderName = folder.find('span', attrs = {'class':'tree-title'}).text
        folderString = folder.find('span', attrs = {'class':'text-help'}).text
        numFilesInFolder = int(folderString.split("-")[1].split(" ")[1])
        if (numFilesInFolder > 0):
            time.sleep(3)
            downloaded = scrapFileInFolder(folder["data-menu-title"], driver, downloaded)

        
    # handling different file edge case
    fileTypeList = []
    for fileSoup in downloadList:
        fileDetail = fileSoup.find('span', attrs = {'class':'text-help'}).text
        print(fileDetail)
        fileTypeList.append(fileDetail.split("-")[0].split(" ")[0])


    # driver.find_element_by_xpath('//*[@id="menu-right"]/div/div/div/ul[1]/li[2]/a').click()
    # driver.find_element_by_xpath('//*[@id="menu-right"]/div/div/div/ul[1]/li[1]/a').click()

    # print(fileTypeList)
    # documents = driver.find_elements_by_css_selector("li[class='jqtree_common jqtree-type-file']")
    # letters = driver.find_elements_by_css_selector("li[class='jqtree_common jqtree-type-letter']")
    # documents.extend(letters)
    # print(len(documents))
    # print(documents)

    # download all files
    # iterator = 0
    # openList = ['PDF', 'JPG', 'PNG', 'JPEG']
    # non_openlist = ['DOCX', 'XLSX', 'DOC', 'MOV', 'ODT', 'TIFF', 'ZIP', 'PPTX','Letter']

    # for document in documents:
    #     flag = 0
    #     try:
    #         document.click()
    #     except:
    #         print("iffy link\n")
    #         flag = 1
        
    #     if flag == 1:
    #         iterator+=1
    #         continue
        
        # # check if file type is PDF or DOCX
        # # chucks an exception if neither
        # print(fileTypeList[iterator])
        # time.sleep(1)
        # if fileTypeList[iterator] in openList:
        #     driver.find_element_by_xpath('//*[@id="menu-right"]/div/div/div/ul[1]/li[2]/a').click()
        # elif fileTypeList[iterator] in non_openlist:
        #     print("download docx")
        #     driver.find_element_by_xpath('//*[@id="menu-right"]/div/div/div/ul[1]/li[1]/a').click()
        # else:
        #     # chucks exception with message file not known to make sure program does not incorrectly save files
        #     f=open("FileTypeError.txt", "a+")
        #     f.write("ClientID: {0}, file: {1}\n".format(id, fileTypeList[iterator]))
        # time.sleep(1.5)
        # iterator += 1
   

def scrapFileInFolder(folderName, driver, downloaded):
    # driver.execute_script("scrollBy(0,-500);")
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    time.sleep(2)
    folder = driver.find_element_by_xpath("//li[@data-menu-title='{0}']".format(folderName))
    folder.click()
    # driver.execute_script("arguments[0].click();", folder)
    # give it 2 seconds to load it in
    time.sleep(1)
    htmlSrc = driver.page_source
    soup = BeautifulSoup(htmlSrc, 'html.parser')

    # nestedFolders = folder.find_elements_by_xpath("//li[@class='jqtree_common jqtree-folder jqtree-closed jqtree-type-case']")
    # print("Num of nested Folder:")
    # print(nestedFolders)

    # folderElement = soup.findAll('li', attrs = {'class':'jqtree_common jqtree-folder jqtree-closed jqtree-type-case'})
    # print(len(folderElement))
    # print(folderElement)
    innerFolderHTML = folder.get_attribute('innerHTML')
    # print(innerFolderHTML)
    # print("\n\n\n")
    # print("innerFolderHTMLSoup\n")
    innerFolderHTMLSoup = BeautifulSoup(innerFolderHTML, 'html.parser')
    # print(innerFolderHTMLSoup);
    # print("\n\n\n")
    # print("nested folder find \n")
    nestedFolder = innerFolderHTMLSoup.findChildren('li', attrs = {'class':'jqtree_common jqtree-folder jqtree-closed jqtree-type-folder'})
    # print(nestedFolder)
    print(len(nestedFolder))

    if len(nestedFolder) > 0:
        f=open("Folder.txt", "a+")
        f.write("ClientID: {0}\n".format(id))
        f.close()

    downloadList = soup.find_all('li', attrs = {'class':'jqtree_common jqtree-type-file'})
    numFiles = len(downloadList)
    print("number of normal Files: {0}".format(numFiles))
    # for element in downloadList:
    #     print(element["data-menu-title"])

    letterList = soup.find_all('li', attrs = {'class':'jqtree_common jqtree-type-letter'})
    downloadList.extend(letterList)
    numFiles += len(downloadList)
    print('number of documents: ' + str(numFiles))

    documents = driver.find_elements_by_css_selector("li[class='jqtree_common jqtree-type-file']")
    letters = driver.find_elements_by_css_selector("li[class='jqtree_common jqtree-type-letter']")
    documents.extend(letters)
    print(len(documents))
    print(documents)

    avoidList = ['MSG', 'XML']
    for element in documents:
        try:
            if element not in downloaded:
                print(element.text)
                fileType = element.find_element_by_xpath(".//span[@class='text-help']").text.split("-")[0].strip().split(" ")[0]
                if fileType in avoidList:
                    f=open("FileError.txt", "a+")
                    f.write("ClientID: {0}, {1}\n".format(id, fileType))
                    f.close()
                    continue
                element.click()
                time.sleep(0.8)
                downloaded.append(element)
                print(driver.find_element_by_xpath('//*[@id="menu-right"]/div/div/div/ul[1]/li[2]/a').text)
                if driver.find_element_by_xpath('//*[@id="menu-right"]/div/div/div/ul[1]/li[2]/a').text == 'Download':
                    driver.find_element_by_xpath('//*[@id="menu-right"]/div/div/div/ul[1]/li[2]/a').click()
                else:
                    driver.find_element_by_xpath('//*[@id="menu-right"]/div/div/div/ul[1]/li[1]/a').click()
                time.sleep(2)
        except Exception as e:
            print("failed to scrap:" + element.text)
            print(e)
            continue

    # close folder
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    time.sleep(5)
    folder = driver.find_element_by_xpath("//li[@data-menu-title='{0}']/div".format(folderName)).click()
    # driver.execute_script("arguments[0].click();", folder)
    return downloaded


def create_folder(root ,id):
    dstPath = os.path.join(root, str(id))
    if os.path.isdir(dstPath):
        return dstPath

    try:
        os.mkdir(dstPath)
    except OSError:
        print("Creation of the directory %s failed" % dstPath)
        raise OSError
    else:
        print ("Sucessfully created directory %s" % dstPath)
        return dstPath

def moveFiles(src ,dst):
    documents = os.listdir(src)
    print(documents)
    for doc in documents:
        if doc.find(".crdownload") != -1:
            time.sleep(3)
            # recursive call to moveFile if file still getting downloaded
            moveFiles(src, dst)
        if os.path.isfile(os.path.join(src, doc)):
            # if dest path is already an file, append date to end of name
            if os.path.isfile(os.path.join(dst, doc)):
                currDate = datetime.datetime.now()
                dateTStr = str(currDate.day) + str(currDate.month) + str(currDate.year) + str(currDate.minute) + str(currDate.second)
                os.rename(os.path.join(src, doc), os.path.join(dst, dateTStr + str(doc)))
            else:
                os.rename(os.path.join(src, doc), os.path.join(dst, doc))



if __name__ == '__main__':
    # initalized driver
    # driver = webdriver.Chrome('/mnt/c/webdriver/chromedriver.exe')
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": r"C:\Users\jerry lu\downloads",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": False
    })

    chrome_options.add_experimental_option("args", {
        'disable-extensions',
        'safebrowsing-disable-extension-blacklist',
        'safebrowsing-disable-download-protection'
    })
    driver = webdriver.Chrome('C:\webdriver\chromedriver.exe', options=chrome_options)

    driver.get(LOGIN_URL)
    client_ids = read_client_ids()
    # uncomment to hardcode client IDs for testing
    # client_ids = ['239']
    # ___________________________________________
    # client_ids = ['5']
    login(driver, 5)
    for id in client_ids:
        try:
            id = int(id)
        except:
            print("")
        else:
            dest = create_folder(DOWNLOAD_FOLDER_PATH, id)
            client_URL = PROFILE_URL + str(id)
            DOC_URL = DOCUMENT_BASE_URL + str(id)
            downloadDocs(driver, client_URL, DOC_URL)
            time.sleep(1.5)
            moveFiles(CHROME_DOWNLOAD, dest)

    time.sleep(2)
    # driver.close()
