import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import csv
import os


master_site_info = {
    "entracker": {
        "url": "https://entrackr.com/?s={}",
        "next_button_xpath": "//a[@class='page-numbers next']",
        "css_selector": "h3.elementor-heading-title",
        "tag_name": "a"   
    },
    
    "inc42": {},
    "techcrunch": {
        "url": "https://search.techcrunch.com/search;_ylc=X3IDMgRncHJpZANxMEJ4Z3h5Y1NycXZCSXJDVEdvRElBBG5fc3VnZwM4BHBvcwMwBHBxc3RyAwRwcXN0cmwDMARxc3RybAM2BHF1ZXJ5A3JhaXNlcwR0X3N0bXADMTY1OTQzMzU3MA--?p={}&fr=techcrunch",
        "next_button_xpath": "//a[@class='next']",
        "css_selector": "h4.pb-10",
        "tag_name": "a"   
        },
    "techfunding": {},
    "vccircle": {}
    
}


def scrape(site_name, search_term="raisesioijwjehfew"):
    
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    site_data = master_site_info.get(site_name)
    if not site_data:
        raise Exception("No master site info")
    
    search_url = site_data["url"].format(search_term)
    driver.get(search_url)
    
    #this dmaximize the chrome browser window
    driver.maximize_window()
    time.sleep(5)

    final_list = []
    for i in range(2):
        web_element_list = driver.find_elements(By.CSS_SELECTOR, site_data["css_selector"]) 
        for web_element in web_element_list:
            try:
                text_element = web_element.text
                a_element = web_element.find_element(By.TAG_NAME, 'a')
                href_attr = a_element.get_attribute("href")
                final_list.append((href_attr, text_element))
                
            except Exception:
                continue

        next_button = driver.find_element(By.XPATH, site_data["next_button_xpath"])
        next_button.click()
        time.sleep(2)
    
    # Check save destination path exists
    BASE_DIR = os.path.dirname(os.path.abspath(_file_))
    save_folder_path = os.path.join(BASE_DIR, 'data')
    
    print(save_folder_path)
    os.makedirs(save_folder_path, exist_ok=True)
    
    with open(f"{save_folder_path}/{site_name}.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(final_list)
        f.close()

    driver.close()
    return 


if _name_ == "_main_":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", help="name of the site")
    parser.add_argument("--search", help="search for this term on the website")
    args = parser.parse_args()
    print(args)  
    if args.name:
        print(args.name)
        print("=="*45)
        scrape(args.name)