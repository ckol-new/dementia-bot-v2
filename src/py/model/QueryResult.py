import numpy as np
from py.model.Comment import Comment
from py.model.Author import Author

# class that contains the query results of a single comment
# tracking information to correspond each cosine similarity output with the sentence it corresponds to
class QueryResultComment:
    def __init__(self, url: str, author: Author, content: list[str], content_results: list):
        self.url = url
        self.author = author
        self.content = content
        self.content_results = content_results


    def to_dict(self):
        return {
            'url': self.url,
            'author': self.author.to_dict(),
            'content': self.content,
            'content_results': self.content_results
        }

    @classmethod
    def from_dict(cls, data):
        url = data['url']
        author = Author.from_dict(data['author'])
        content_dict = data['content']
        content = list(content_dict)
        content_results_data= data['content_results']
        content_results = []
        for result_data in content_results_data:
            vresult = np.array(result_data['vector'], dtype=result_data['dtype'])
            vresult = np.reshape(vresult, shape=result_data['shape'])
            content_results.append(vresult)

        return cls(
            url=url,
            author=author,
            content=content,
            content_results=content_results
        )



# class that contains the query result of a single discussion
# tracking information to correspond each cosine similarity output with the sentence it corresponds to
class QueryResultDiscussion:
    def __init__(self, url: str, title: str, title_result: np.float32, author: Author,  content: list[str], content_results: list[np.float32], comments: list[Comment], comment_results: list[QueryResultComment]):
        self.url = url
        self.title = title
        self.title_result = title_result
        self.author = author
        self.content = content
        self.content_results = content_results
        self.comments = comments
        self.comment_results = comment_results


    def to_dict(self):
        return {
            'url': self.url,
            'title': self.title,
            'title_result': {
                '__np_arr': True,
                'dtype': str(self.title_result.dtype),
                'shape': str(self.title_result.shape),
                'vector': self.title_result.tolist()
            },
            'author': self.author.to_dict(),
            'content': self.content,
            'content_results': [
                {
                    '__np_arr': True,
                    'dtype': str(result.dtype),
                    'shape': str(result.shape),
                    'vector': result.tolist()
                } for result in self.content_results if self.content_results
            ],
            'comments': [comment.to_dict() for comment in self.comments if self.comments],
            'comment_results': [comment_result.to_dict() for comment_result in self.comment_results if self.comment_results]
        }

    @classmethod
    def from_dict(cls, data):
        url = data['url']
        title = data['title']
        title_result_data = data['title_result']
        if not title_result_data['__np_arr']:
            return None
        title_result_vector = np.array(title_result_data['vector'], dtype=title_result_data['dtype'])
        title_result_vector = np.reshape(title_result_vector, shape=title_result_data['shape'])
        author = Author.from_dict(data['author'])

        content = data['content']
        content_result_data = data['content_results']
        content_results = []
        for result_data in content_result_data:
            if result_data['__np_arr']:
                vresult = np.array(result_data['vector'], dtype=result_data['dtype'])
                vresult = np.reshape(vresult, shape=result_data['shape'])
                content_results.append(vresult)

        comments = [Comment.from_dict(comment_data) for comment_data in data['comments']]
        comment_results = [QueryResultComment.from_dict(comment_result_data) for comment_result_data in data['comment_results']]

        return cls(
            url=url,
            title=title,
            title_result=title_result_vector,
            author=author,
            content=content,
            content_results=content_results,
            comments=comments,
            comment_results=comment_results
        )

class QueryResponse:
    def __init__(self, limit=None):
        self.limit = limit
        self.__query_results = []

    def add(self, query_result: QueryResultDiscussion):
        if self.limit:
            if len(self.__query_results) >= self.limit:
                return

        self.__query_results.append(query_result)


