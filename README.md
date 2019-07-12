# CRM-Migration

### About this program
This is a suit of scripts designed to do the following:

1. Scrap data and files off of existing CRM using PyAutoGui, BeautifulSoup and Selenium webdriver
1. Process scrapped data into a format that is compliant with requirements from new CRM

Selenium webdriver had to be used as the website contained dynamically generated html which will be inaccessible using conventional webscrapping means.

### Description of scripts

1.save_pdf.py -> python script used to save the pdf version of client notes for backup
1.ProcessClient.sh -> shell script used to extract the JSON string containing the client notes
1.save_document.py -> python script used to save all attachment (pdf, docx, jpeg etc) associated with client. 
1.ZIPfiles.py -> python script used to concatinate client-ID in front of file name and add them to folder. If folder exceeds 400 mb, it will create new folder and add additional files there.
