import numpy as np
from Author import Author

# EACH SENTENCE GETS EMBEDDED AS ITS OWN VECTOR, MEANING EACH CONTENT IS LIST OF VECTORS
# embedded discussion class holds all data around an embedded discussion
# can be generated from embedding process, or by json deserialization
# holds list of embedded comment objects (individual embedded comments)
# has author object
class EmbeddedDiscussion:
    def __init__(self, url: str, discussion_id: int, title: str, author: Author, date: str, content: np.ndarray, comments: list):
        self.url = url
        self.discussion_id = discussion_id
        self.title = title
        self.author = author
        self.date = date
        self.content = content
        self.comments = comments

    def to_dict(self):
        return {
            "url": self.url,
            "discussion_id": self.discussion_id,
            "title": self.title,
            'author': self.author.to_dict() if self.author else None,
            'date': self.date,
            "content": {
                '__np_arr': True,
                'dtype': str(self.content.dtype),
                'shape': str(self.content.shape),
                'vectors': [self.content[i].tolist() for i in range(self.content.shape[0])]
            },
            'comments': [comment.to_dict() for comment in self.comments] if self.comments else []
        }

    @classmethod
    def from_dict(cls, data: dict):
        author = Author.from_dict(data['author']) if data.get('author') else None
        content_data = data['content']
        if content_data.get('__np_arr'):
            vectors = np.array(content_data['vectors'], dtype=content_data['dtype'])
        else:
            vectors = np.array([])
        return cls(
            url=data['url'],
            discussion_id=data['discussion_id'],
            title=data['title'],
            author=author,
            date=data['date'],
            content=vectors,
            comments=data.get('comments', [])
        )