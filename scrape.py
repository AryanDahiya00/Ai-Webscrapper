import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service 
from bs4 import BeautifulSoup
import time

#scrape the site
def scrape_website(website):
    print("launching chrome browser..")
    chrome_driver_path = ".\chromedriver.exe"  # Correct this path
    options=webdriver.ChromeOptions()
    driver=webdriver.Chrome(service=Service(chrome_driver_path),options=options)
    
    try:
        driver.get(website)
        print("page loading..")
        html=driver.page_source
        time.sleep(10)
        return html
    finally:
        driver.quit()
     
     
#extract the content   
def extract_body_content(html_content):
    soup=BeautifulSoup(html_content,"html.parser")
    body_content=soup.body
    if(body_content):
        return str(body_content)
    return ""

#clean the content
def clean_body_content(body_content):
     soup=BeautifulSoup(body_content,"html.parser")
     for script_or_style in soup(["script","style"]):
         script_or_style.extract() # removing scripts and styles
    
     cleaned_content=soup.get_text(separator="\n")
     cleaned_content="\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip()) #remove \n if there is no text btw them
     return cleaned_content
    
#convert the content into bacth to match the prompt size limit
def split_dom_content(dom_content,max_length=6000):
    return [
        dom_content[i:i+max_length] for i in range(0,len(dom_content),max_length)
    ]
    
    


    
    
    