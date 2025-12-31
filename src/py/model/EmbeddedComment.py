from Author import  Author
import numpy as np

# EACH SENTENCE GETS EMBEDDED AS ITS OWN VECTOR, MEANING EACH CONTENT IS LIST OF VECTORS
# embedded comment class holds all data around an embedded comment
# can be generated from embedding process, or by json deserialization
# has author object
class EmbeddedComment:
    def __init__(self, author: Author, date: str, content: np.ndarray):
        self.author = author
        self.date = date
        self.content = content

    def to_dict(self):
        return {
            "author": self.author.to_dict() if self.author else None,
            "content": {
                '__np_arr': True,
                'dtype': str(self.content.dtype),
                'shape': self.content.shape,
                'vectors': [self.content[i].tolist() for i in range(self.content.shape[0])]
            },
            'date': self.date
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
            author=author,
            date=data['date'],
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