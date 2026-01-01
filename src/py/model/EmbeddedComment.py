from .Author import  Author
import numpy as np

# EACH SENTENCE GETS EMBEDDED AS ITS OWN VECTOR, MEANING EACH CONTENT IS LIST OF VECTORS
# embedded comment class holds all data around an embedded comment
# can be generated from embedding process, or by json deserialization
# has author object
class EmbeddedComment:
    def __init__(self, url: str, author: Author, date: str, sentences: list, content: list):
        self.url = url
        self.author = author
        self.date = date
        self.sentences = sentences
        self.content = content

    def to_dict(self):
        return {
            'url': self.url,
            "author": self.author.to_dict() if self.author else None,
            'sentences': self.sentences,
            "content": [
                {
                    '__np_arr': True,
                    'dtype': str(vector.dtype),
                    'shape': str(vector.shape),
                    'vector': vector.tolist()
                } for vector in self.content if self.content
            ],
            'date': self.date
        }

    @classmethod
    def from_dict(cls, data: dict):
        author = Author.from_dict(data['author']) if data.get('author') else None
        sentences_data = data['sentences']
        sentences = list(sentences_data)
        content_data = data['content']
        if content_data.get('__np_arr'):
            vectors = np.array(content_data['vectors'], dtype=content_data['dtype'])
        else:
            vectors = np.array([])
        return cls(
            url=data['url'],
            author=author,
            date=data['date'],
            sentences=sentences,
            content=vectors
        )

    def __eq__(self, other):
        if not isinstance(other, EmbeddedComment):
            return False
        return (
            self.author == other.author and
            self.date == other.date and
            np.array_equal(self.content, other.content)
        )