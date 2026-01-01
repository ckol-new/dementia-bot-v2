import requests
import json
from py.model.Author import Author
from py.model.Discussion import Discussion
from py.model.Comment import Comment
from time import perf_counter
from bs4 import BeautifulSoup
from time import perf_counter



# class(no instance)
class ALZConnectedScraper:
    @classmethod
    def request_page(cls, url: str, header=None, timer: bool = False) -> str:
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

    @classmethod
    def scrape_discussion_links(cls, html: str, timer: bool = False) -> list:
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

    @classmethod
    def __get_title(cls, soup):
        title_text = soup.title.string
        title_text = title_text.removesuffix(' \u2014 ALZConnected')
        return title_text

    @classmethod
    def __get_discussion_id(cls, url):
        sep = '/discussion/'
        _, _, id_string = url.partition(sep)
        id = id_string[0:5]
        return id

    @classmethod
    def __get_discussion_author(cls, soup):
        author_div = soup.find('span', class_="Author")
        if not author_div: return None
        author_a = author_div.find('a')
        if not author_a: return None

        author_name = author_a.string
        author_id = author_a.get('data-userid')
        link = author_a.get('href')

        # get author obj
        author = Author(author_name, author_id, link)
        return author

    @classmethod
    def __get_discussion_content(cls, soup):
        content_arr = []

        div_discussion = soup.find('div', class_='Discussion')
        if not div_discussion: return None
        div_content = div_discussion.find('div', class_='Message userContent')
        if not div_content: return None

        for paragraph in div_content.find_all('p'):
            content_arr.append(paragraph.string)

        # join paragraph
        content = '\n'.join([str(content) for content in content_arr])

        return content

    @classmethod
    def __get_discussion_date(cls, soup):
        div_discussion = soup.find('div', class_='Discussion')
        if not div_discussion: return None
        div_meta_discussion = div_discussion.find('div', class_='Meta DiscussionMeta')
        if not div_meta_discussion: return None
        time_div = div_meta_discussion.find('time')
        if not time_div: return None
        date = time_div.get('title')
        return date
        ...

    @classmethod
    def __get_comment_author(cls, comment):
        # get author data
        div_meta_comment = comment.find('div', class_='Meta CommentMeta CommentInfo')
        if not div_meta_comment: return None
        time_div = div_meta_comment.find('time')
        if not time_div: return None
        date = time_div.get('title')
        author_name = comment.find('a', class_='Username js-userCard').string
        author_id = comment.find('a', class_='Username js-userCard').get('data-userid')
        link = comment.find('a', class_='Username js-userCard').get('href')

        # get author obj
        author = Author(author_name, author_id, link)
        return author

    def __get_comments_div(cls, soup):
        comment_div_list = soup.find('ul', class_='MessageList DataList Comments pageBox')
        comment_list = []
        if not comment_div_list: return None
        for comment_div in comment_div_list.find_all('div', class_='Comment'):
            comment_list.append(comment_div)

        return comment_list

    def __get_comment_date(cls, comment):
        time_div = comment.find('time')
        return time_div.get('title')

    @classmethod
    def __get_comment_content(cls, comment):
        content_arr = []

        div_content = comment.find('div', class_='Message userContent')
        if not div_content: return None

        paragraphs = div_content.find_all('p')
        if len(paragraphs) == 0:
            return div_content.string

        for paragraph in paragraphs:
            content_arr.append(paragraph.string)

        content = '\n'.join([str(c) for c in content_arr])
        return content

    @classmethod
    def get_discussion_post(cls, url):
        # init comments
        comments = []

        # get page
        response_html = ALZConnectedScraper.request_page(url)

        # get soup obj
        soup = BeautifulSoup(response_html, 'html.parser')

        # get title
        title = cls.__get_title(soup)
        print(title)

        # get id
        id = cls.__get_discussion_id(url)

        # get author
        dauthor = cls.__get_discussion_author(soup)

        # get date
        date = cls.__get_discussion_date(soup)

        # get content
        content = cls.__get_discussion_content(soup)

        # for each comment
        num = 1
        comments_div = cls.__get_comments_div(cls=cls, soup=soup)
        if comments_div:
            for comment in comments_div:
                # get comment author
                author = cls.__get_comment_author(comment)

                # get comment date
                date = cls.__get_comment_date(cls=cls, comment=comment)

                # get comment content
                content = cls.__get_comment_content(comment)

                # get comment obj
                comment = Comment(url, author, date, content)
                comments.append(comment)

                num += 1

        # get discussion obj
        discussion = Discussion(url, id, title, dauthor, date, content, comments)
        return discussion

    @classmethod
    def scrape(cls, input, output, limit=None):
        time_start = perf_counter()
        length = None
        with open(input, 'r') as f:
            length = sum([1 for _ in f])
        with open(input, 'r') as f:
            # write to output
            with open(output, 'w') as wf:
                num_visited = 0
                for line in f:
                    if limit:
                        if num_visited >= limit:
                            break

                    if num_visited % 10 == 0:
                        print(f"Processing %{(num_visited / length) * 100:.2f}")

                    discussion = cls.get_discussion_post(line)
                    json_line = json.dumps(discussion.to_dict())

                    wf.write(json_line)
                    wf.write('\n')
                    num_visited += 1

        time_end = perf_counter()
        print('time to scrape: ', (time_end - time_start))