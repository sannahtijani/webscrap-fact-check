import requests
import html5lib
from bs4 import BeautifulSoup
import csv
import io
import time
import unicodedata  # Added to handle accents and special characters
import re  # Added for regular expressions

# Function to clean and normalize text
def clean_text(text):
    # Correct spelling and normalize accents
    normalized_text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    return normalized_text

# Custom function to clean and normalize the category text
def clean_category(category_element):
    if category_element:
        category_text = category_element.text
        cleaned_category = clean_text(category_text)
        # Replace "Ã©" with "é" specifically in the category text
        cleaned_category = cleaned_category.replace("Ã©", "é")
        return cleaned_category
    return ''

def recupere(url):
    r = requests.get(url)
    page = r.content
    info = []

    soup = BeautifulSoup(page, 'html5lib')

    art = soup.find_all('div', class_='jsx-3330840791 ArticleList__Article')
    for item in art:
        category_element = item.find('span', class_='ArticleItem__Category')
        category = clean_category(category_element)
        article_url = item.find('a')['href']
        if not article_url.startswith('http'):
            article_url = 'https://www.tf1info.fr' + article_url
        article_page = requests.get(article_url).content
        article_soup = BeautifulSoup(article_page, 'html5lib')
        title_element = article_soup.find('h1')
        if title_element is None:
            title_element = article_soup.find('h2')

        if title_element is not None:
            title = title_element.text
        else:
            title = ''
        author_element = article_soup.find('span', class_='jsx-1842855038')
        author = author_element.text.replace('par', '').strip() if author_element else ''
        date_element = item.find('div', class_='ArticleItem__Date')
        date = date_element.text if date_element else ''
        summary_elements = article_soup.find_all('span', class_='ArticleChapo__Point')
        summary = ' '.join([element.text for element in summary_elements])
        paragraph_elements = article_soup.find_all('span', {'data-module': 'article-paragraph'})
        paragraphs = []

        for element in paragraph_elements:
            p_tags = element.find_all('p')
            for p_tag in p_tags:
                cleaned_paragraph = clean_text(p_tag.text)  # Clean and normalize text
                cleaned_paragraph = re.sub(r'[^a-zA-Z0-9\s]', ' ', cleaned_paragraph)
                paragraphs.append(cleaned_paragraph)

        cleaned_title = clean_text(title)
        cleaned_summary = clean_text(summary)
        cleaned_author = clean_text(author)
        cleaned_date = clean_text(date)

        full_text = cleaned_title + '\n' + cleaned_summary + '\n' + '\n'.join(paragraphs)


        info.append([article_url, cleaned_title, cleaned_author, cleaned_date, cleaned_summary, category, paragraphs, full_text])

    return info

ur = "https://www.tf1info.fr/actualite/les-verificateurs-12325/"

with open("TF1webscap.csv", "w", encoding="utf-8", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['URL', 'Title', 'Author', 'Date', 'Summary', 'Category', 'Paragraphe', 'Full Text'])
    for k in range(1, 72):
        url = ur + str(k)
        print(k)
        c = recupere(url)
        for item in c:
            print(item)
            writer.writerow(item)

