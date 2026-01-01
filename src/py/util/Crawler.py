from time import perf_counter

class ALZConnectedCrawler:

    # py crawl method: abstracts the process away
    # memory efficient (writes to file instead of holding in memory)
    @classmethod
    def crawl(cls, base_url: str, num_pages: int, seed_path: str, crawl_output_path: str, start: int = 2, timer: bool = False):
        start_time = perf_counter()
        ALZConnectedCrawler.generate_seed_file(base_url, num_pages, seed_path, start)
        ALZConnectedCrawler.generate_crawl_data(crawl_output_path, seed_file=seed_path)
        end_time = perf_counter()

        if timer: print(f"Crawling process took {end_time - start_time:.4f} seconds.")



    # can declare page start, or leave as None to start from beginning (page 2
    @classmethod
    def generate_seed_file(cls, base_url: str, num_pages: int, seed_path: str, start: int = 2):
        with open(seed_path, 'w') as sf:
            sf.write(base_url)
            sf.write('\n')

            # loop through all pages
            for page_num in range(start, num_pages + 1):
                page_url = base_url + '/p' + str(page_num)
                sf.write(page_url)
                sf.write('\n')

    @classmethod
    def read_seed_file(cls, seed_path: str) -> list:
        seed_data = []
        with open(seed_path, 'r') as sf:
            for line in sf:
                seed_data.append(line.strip())

        return seed_data

    # can crawl from seed data in memory or from a seed file
    # memory efficient (does not hold all data in memory)
    @classmethod
    def generate_crawl_data(cls, crawl_output_path: str, seed_data: list = None, seed_file: str = None):
        from py.util.Scraper import ALZConnectedScraper

        if seed_data is not None:
            crawl_data = []
            for url in seed_data:
                html = ALZConnectedScraper.request_page(url, timer=False)
                discussion_links = ALZConnectedScraper.scrape_discussion_links(html, timer=False)

                for link in discussion_links:
                    crawl_data.append(link)

            return crawl_data
        length = None
        with open(seed_file, 'r') as sf:
            length = sum([1 for line in sf])

        with open(seed_file, 'r') as sf:
            from py.util import Scraper
            num = 0
            for line in sf:
                if num % 10 == 0:
                    print(f'% {(num / length) * 100}')
                num += 1

                url = line.strip()
                html = ALZConnectedScraper.request_page(url, timer=False)
                discussion_links = ALZConnectedScraper.scrape_discussion_links(html, timer=False)

                for link in discussion_links:
                    ALZConnectedCrawler.save_crawled_data(crawl_output_path, link)

    # save one by one (appending to end of file), to avoid holding all data in memory
    @classmethod
    def save_crawled_data(cls, crawl_output_path: str, url: str):
        with open(crawl_output_path, 'a') as cof:
            cof.write(url)
            cof.write('\n')