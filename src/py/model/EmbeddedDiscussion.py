import numpy as np
from .Author import Author
from py.model.EmbeddedComment import EmbeddedComment

# EACH SENTENCE GETS EMBEDDED AS ITS OWN VECTOR, MEANING EACH CONTENT IS LIST OF VECTORS
# embedded discussion class holds all data around an embedded discussion
# can be generated from embedding process, or by json deserialization
# holds list of embedded comment objects (individual embedded comments)
# has author object
class EmbeddedDiscussion:
    def __init__(self, url: str, discussion_id: int, title_string: str,  title: np.ndarray, author: Author, date: str, sentences: list, content: list[np.ndarray], comments: list):
        self.url = url
        self.discussion_id = discussion_id
        self.title_string = title_string
        self.title = title
        self.author = author
        self.date = date
        self.sentences = sentences
        self.content = content
        self.comments = comments

    def to_dict(self):
        return {
            "url": self.url,
            "discussion_id": self.discussion_id,
            'title_string': self.title_string,
            "title": {
                '__np_arr': True,
                'dtype': str(self.title.dtype),
                'shape': str(self.title.shape),
                'vector': self.title.tolist()
            },
            'author': self.author.to_dict() if self.author else None,
            'date': self.date,
            'sentences': self.sentences,
            "content": [{
                '__np_arr': True,
                'dtype': str(vector.dtype),
                'shape': str(vector.shape),
                'vector': vector.tolist()
            } for vector in self.content if self.content
            ],
            'comments': [comment.to_dict() for comment in self.comments] if self.comments else []
        }

    @classmethod
    def from_dict(cls, data: dict):
        author = Author.from_dict(data['author']) if data.get('author') else None
        title_data = data['title']
        if title_data.get('__np_arr'):
            title = np.array(title_data['vector'], dtype=title_data['dtype'])
        else: title = None
        sentences_data = data['sentences']
        sentences = list(sentences_data)
        content_data = data['content']
        vectors = []
        if content_data.get('__np_arr'):
            vectors_data = content_data['vectors']
            vectors_list = list(vectors_data)
            for vector_data in vectors_list:
                vector_list = list(vectors_data)
                vector = np.array(vector_list, dtype=content_data['dtype']) if vector_data is not None else None
                vectors.append(vector)
        else:
            vectors = np.array([])

        comments = [EmbeddedDiscussion.from_dict(comment_data) for comment_data in data['comments']]

        return cls(
            url=data['url'],
            discussion_id=data['discussion_id'],
            title_string=data['title_string'],
            title=title,
            author=author,
            date=data['date'],
            sentences=sentences,
            content=vectors,
            comments=comments
        )