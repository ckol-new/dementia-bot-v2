from util.ALZConnectedCrawler import crawl
import pathlib

def main():
    # get current working directory
    cwd = pathlib.Path().resolve() / 'src'
    print(cwd)
    seed_path = cwd / 'data' / 'seeds'
    crawl_path = cwd / 'data' / 'Crawler_Output'
    scrape_path= cwd / 'data' / 'Scrape_Output'
    encode_path = cwd / 'data' / 'Encoded_Output'

    early_onset: dict = {
        'base_url': 'https://alzconnected.org/categories/i-have-younger-onset-alzheimers',
        'num_pages': 10,
        'seed_path': seed_path / 'ALZConnected' / 'early_onset_seeds.txt',
        'crawl_output_path': crawl_path / 'ALZConnected' / 'early_onset_crawler_output.txt',
    }

    # test crawler
    crawl(
        base_url= early_onset['base_url'],
        num_pages= early_onset['num_pages'],
        seed_path= early_onset['seed_path'],
        crawl_output_path= early_onset['crawl_output_path'],
        timer=True
    )

if __name__ == "__main__":
    main()