import requests
import html5lib
from bs4 import BeautifulSoup
import csv
import io
import time
import unicodedata
import re

# Function to clean and normalize text
def clean_text(text):
    normalized_text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    return normalized_text

# Custom function to clean and normalize the category text
def clean_category(category_element):
    if category_element:
        category_text = category_element.text
        cleaned_category = clean_text(category_text)
        return cleaned_category
    return ''

def recupere(urls):
    correct_urls = []
    for url in urls:
        url = url.strip("['")  # remove leading [' characters
        url = url.strip("']")  # remove trailing '] characters
        correct_url = 'https://www.20minutes.fr' + url
        correct_urls.append(correct_url)

    info = []
    for url in correct_urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html5lib')
        title_element = soup.find('h1', class_='nodeheader-title')
        date_element = soup.find('time')
        author_element = soup.find('span', class_='author-name') or soup.find('span', class_='authorsign-label')
        summary_element = soup.find('span', class_='hat-summary')
        category_element = soup.find('strong', class_='hat-label color-default')
        text_elements = soup.find_all('p')
        
        title = clean_text(title_element.text.strip()) if title_element else None
        date = date_element['datetime'] if date_element else None
        author = clean_text(author_element.text.strip()) if author_element else None
        summary = clean_text(summary_element.text.strip()) if summary_element else None
        category = clean_category(category_element)
        text = ' '.join([clean_text(element.text.strip()) for element in text_elements])
        full_text = ' '.join(filter(None, [title, summary, text]))
        
        info.append([url, title, date, author, summary, category, text, full_text])

    return info

with open('20MinutesURL.txt', 'r') as f:
    urls = f.read().splitlines()

correct_urls = recupere(urls)

with open('20Minutes.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['URL', 'Title', 'Date', 'Author', 'Summary', 'Category', 'Text', 'Full_Text'])
    for url_info in correct_urls:
        writer.writerow(url_info)
