import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse, urljoin, unquote

MIN_WORD_COUNT = 1000
TARGET_PAGE_COUNT = 100
OUTPUT_DIR = 'downloaded_pages'
INDEX_FILE = 'index.txt'

def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Ошибка при загрузке {url}: {e}")
        return None

def parse_page(html):
    soup = BeautifulSoup(html, 'lxml')
    html_tag = soup.find('html')
    if html_tag and html_tag.get('lang') == 'ru':
        text = soup.get_text()
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        return text, links
    return None

def save_text(content, doc_number):
    filename = os.path.join(OUTPUT_DIR, f'doc_{doc_number}.txt')
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

def update_index(doc_number, url):
    with open(INDEX_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{doc_number}\t{url}\n")

def normalize_url(url):
    url = unquote(url)
    parsed_url = urlparse(url)
    return parsed_url._replace(fragment='', query='').geturl()

def crawl(start_urls):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    visited_urls = set()
    doc_count = 0
    urls_to_visit = list(start_urls)

    while urls_to_visit and doc_count < TARGET_PAGE_COUNT:
        current_url = urls_to_visit.pop(0)

        normalized_url = normalize_url(current_url)
        if normalized_url in visited_urls:
            continue
        if normalized_url.endswith('.pdf'):
            continue
        visited_urls.add(normalized_url)

        html = fetch_page(normalized_url)
        if html is None:
            continue
        parse_res = parse_page(html)
        if parse_res is None:
            continue
        text, links = parse_res

        cleaned_text = text.split()
        word_count = len(cleaned_text)
        if word_count >= MIN_WORD_COUNT:
            cleaned_text = ' '.join(cleaned_text)
            doc_count += 1
            save_text(cleaned_text, doc_count)
            update_index(doc_count, normalized_url)
            print(f"Сохранена страница {doc_count}: {normalized_url} ({word_count} слов)")

            for link in links:
                full_link = urljoin(normalized_url, link)
                normalized_link = normalize_url(full_link)
                if link not in visited_urls and normalized_link not in urls_to_visit:
                    urls_to_visit.append(normalized_link)




def main():
    args = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%B0%D0%BD%D0%B2%D0%B8%D1%82%D0%B0%D0%BB%D0%B8%D1%8F_%D0%BB%D0%B5%D0%B6%D0%B0%D1%87%D0%B0%D1%8F'
    open(INDEX_FILE, 'w').close()
    crawl([args])

if __name__ == '__main__':
    main()