import requests
from time import perf_counter
from bs4 import BeautifulSoup

def request_page(url: str, header=None, timer: bool = False)-> str:
    if not header:
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

    start = perf_counter()
    response = requests.get(url, headers=header)
    end = perf_counter()

    if timer:
        print(f"Request to {url} took {end - start:.4f} seconds.")

    return response.text

def scrape_discussion_links(html: str, timer: bool = False) -> list:
    soup = BeautifulSoup(html, 'html.parser')
    discussion_links = []

    start = perf_counter()
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if '/discussion/' in href:
            discussion_links.append(href)
    end = perf_counter()

    if timer: print(f"Scraping discussion links took {end - start:.4f} seconds.")

    return discussion_links