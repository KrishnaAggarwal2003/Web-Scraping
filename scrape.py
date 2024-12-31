import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import random
from selenium.webdriver.chrome.options import Options

# function for scraping data
def website_scraper_with_proxies(website_url, proxies):
    proxy_list = [
    "http://51.158.68.68:8811",
    "http://51.91.212.159:3128",
    "http://104.248.63.17:30588",
    # Add more proxies to the list
]    
    
    print("Starting scraping process")
    
    chrome_driver_path = 'C:\\Users\\DELL\\Downloads\\AI-Web-Scraper\\chromedriver.exe'  # Update this path if needed
    
    for attempt in range(len(proxies)):
        proxy = random.choice(proxies)  # Select a random proxy
        print(f"Attempt {attempt + 1}: Using proxy {proxy}")
        
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument(f"--proxy-server={proxy}")
        
        # Initialize the driver
        driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)
        
        try:
            driver.get(website_url)
            print("Page loaded successfully.")
            html = driver.page_source
            return html
        except Exception as e:
            print(f"An error occurred with proxy {proxy}: {e}")
        finally:
            driver.quit()
        
        # Wait before trying the next proxy
        time.sleep(random.uniform(1, 3))
    
    print("All proxies failed. Unable to scrape the page.")
    return None


# Without Proxies
def website_scraper(website_url):
    print("Starting scraping process")
    
    chrome_driver_path = "C:\\Users\\DELL\\Downloads\\AI-Web-Scraper\\chromedriver.exe"
    Options = webdriver.ChromeOptions() # If user want to give options as to how it should control the browser, for now I kept it as blank
    
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=Options)
    
    try:
        driver.get(website_url)
        print("Page loaded...")
        html = driver.page_source
        
        return html
    except Exception as e:
        print(f"An error occurred while loading the page: {e}")
        return None
    finally:
        driver.quit()
        


def extract_body_content(html_data):
    soup = BeautifulSoup(html_data,"html.parser")
    
    body_content = soup.body
    
    if body_content:
        return body_content
    else:
        return f'Nothing in the body'



def clean_body_content(body_content):
    if not isinstance(body_content, str):
        body_content = str(body_content)  # Convert to string if not already
    body_soup = BeautifulSoup(body_content, "html.parser")
    
    for script_or_style in body_soup(["script", "style"]):
        script_or_style.extract()
    
    cleaned_body_content = body_soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_body_content.splitlines() if line.strip()
    )
    
    return cleaned_content



def split_dom_content(dom_content, max_size=6000):
    
    if dom_content:
     return[
        dom_content[i: i+max_size] for i in range(0,len(dom_content), max_size) # to make batches of size=max_size of the html content, as LLM have a limited token size.
     ]
    
    else:
        return f'No content to split' 

    