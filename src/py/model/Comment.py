from .Author import Author

# comment class holds all data around an un-embedded comment
# can be generated from scraping, or by json deserialization
# had author object
# to and from dict methods for serialization/deserialization
class Comment:
    def __init__(self, url: str, author: Author, date: str, content: str):
        self.url = url
        self.author = author
        self.date = date
        self.content = content

    def to_dict(self) -> dict:
        return {
            'url': self.url,
            "author": self.author.to_dict() if self.author else None,
            'date': self.date,
            "content": self.content,
        }

    @classmethod
    def from_dict(cls, data: dict):
        author = Author.from_dict(data['author']) if data.get('author') else None
        return cls(
            url=data['url'],
            author=author,
            date=data['date'],
            content=data['content']
        )

    def __eq__(self, other):
        if not isinstance((other), Comment):
            return False
        return (
            self.url == other.url and
            self.author == other.author and
            self.date == other.date and
            self.content == other.content
        )
