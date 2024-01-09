from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def scrape_page(url):
    # Create a new instance of the Edge driver
    driver = webdriver.Edge()

    # Navigate to the page
    driver.get(url)

    # Find the cookie consent button and click it
    cookie_button = driver.find_element(By.ID, 'didomi-notice-agree-button')
    cookie_button.click()

    # Initialize an empty list to store the article URLs and titles
    info = []

    while True:
        # Wait for the page to load
        driver.implicitly_wait(10)

        # Scroll down the page until the "Voir plus d’articles" button is found
        while True:
            try:
                more_button = driver.find_element(By.XPATH, '//button[contains(text(), "Voir plus d’articles")]')
                more_button.click()
                time.sleep(5)
                break
            except:
                driver.execute_script("window.scrollBy(0, 500);")
                time.sleep(1)
        
        # Check if the "Voir plus d’articles" button is no longer present on the page
        try:
            driver.find_element(By.XPATH, '//button[contains(text(), "Voir plus d’articles")]')
        except:
            break
        
        # Get the updated page content
        page = driver.page_source

        # Parse the updated page content using BeautifulSoup
        soup = BeautifulSoup(page, 'html.parser')
        articles = soup.find_all('article')
        for article in articles:
            url = article.find('a')['href']
            info.append([url])
            print(url)

    # Close the browser window
    driver.quit()

    return info

url = 'https://www.20minutes.fr/societe/desintox/'

with open('20MinutesURL.txt', 'w', encoding='utf-8') as f:
    info = scrape_page(url)
    for item in info:
        f.writelines('%s\n' % item)
