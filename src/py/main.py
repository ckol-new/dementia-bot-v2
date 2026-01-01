from py.util.Crawler import ALZConnectedCrawler
from py.util.Scraper import ALZConnectedScraper
from py.util.Encoder import ALZConnectedEncoder
import pathlib

def scraping():
    # get current working directory
    cwd = pathlib.Path().resolve() / 'src'
    print(cwd)
    seed_path = cwd / 'data' / 'seeds'
    crawl_path = cwd / 'data' / 'Crawler_Output'
    scrape_path= cwd / 'data' / 'Scraped_Output'
    encode_path = cwd / 'data' / 'Encoded_Output'

    early_onset: dict = {
        'base_url': 'https://alzconnected.org/categories/i-have-younger-onset-alzheimers',
        'num_pages': 10,
        'seed_path': seed_path / 'ALZConnected' / 'early_onset_seeds.txt',
        'crawl_output_path': crawl_path / 'ALZConnected' / 'early_onset_crawler_output.txt',
        'scrape_output_path': scrape_path / 'ALZConnected' / 'early_onset_scraper_output.jsonl',
        'encode_output_path': encode_path / 'ALZConnected' / 'early_onset_encoder_output.jsonl'
    }
    dementia_or_other = {
        'base_url': 'https://alzconnected.org/categories/i-have-alzheimers-or-other-dementia',
        'num_pages': 11,
        'seed_path': seed_path / 'ALZConnected' / 'dementia_or_other_seeds.txt',
        'crawl_output_path': crawl_path / 'ALZConnected' / 'dementia_or_other_crawler_output.txt',
        'scrape_output_path': scrape_path / 'ALZConnected' / 'dementia_or_other_scraper_output.jsonl',
        'encode_output_path': encode_path / 'ALZConnected' / 'dementia_or_other_encoder_output.jsonl'
    }

    caregiver_general = {
        'base_url': 'https://alzconnected.org/categories/i-am-a-caregiver-(general-topics)',
        'num_pages': 100,
        'seed_path': seed_path / 'ALZConnected' / 'caregiver_general_seeds.txt',
        'crawl_output_path': crawl_path / 'ALZConnected' / 'caregiver_general_crawler_output_p1-100.txt',
        'scrape_output_path': scrape_path / 'ALZConnected' / 'caregiver_general_scraper_output_p1-100.jsonl',
        'encode_output_path': encode_path / 'ALZConnected' / 'caregiver_general_encoder_output_p1-100.jsonl'
    }

    # test crawler
    print("CRAWLING")
    ALZConnectedCrawler.crawl(
        base_url= caregiver_general['base_url'],
        num_pages= caregiver_general['num_pages'],
        seed_path= caregiver_general['seed_path'],
        crawl_output_path= caregiver_general['crawl_output_path'],
        timer=True
    )

    print("SCRAPING")
    ALZConnectedScraper.scrape(
        input=caregiver_general['crawl_output_path'],
        output=caregiver_general['scrape_output_path'],
    )

    print("ENCODING")
    ALZConnectedEncoder.encode_file(
        scraped_file=caregiver_general['scrape_output_path'],
        encoded_output=caregiver_general['encode_output_path'],
        timer=True
    )

def query():
    pass

def main():
    pass

if __name__ == "__main__":
    main()