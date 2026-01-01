from .Author import Author
from .Comment import Comment

# discussion class holds all data around an un-embedded discussion
# can be generated from scraping, or by json deserialization
# holds list of comment objects (individual comments)
# had author object
# to and from dict methods for serialization/deserialization
class Discussion:
    def __init__(self, url: int, discussion_id: int, title: str, author: Author, date: str, content: str, comments: list):
        self.url = url
        self.discussion_id = discussion_id
        self.title = title
        self.author = author
        self.date = date
        self.content = content
        self.comments = comments

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "discussion_id": self.discussion_id,
            "title": self.title,
            'author': self.author.to_dict() if self.author else None,
            'date': self.date,
            "content": self.content,
            'comments': [comment.to_dict() for comment in self.comments] if self.comments else []
        }

    @classmethod
    def from_dict(cls, data: dict):
        author = Author.from_dict(data['author']) if data.get('author') else None
        comments = [Comment.from_dict(c) for c in data.get('comments',) if data.get('comments')]
        return cls(
            url=data['url'],
            discussion_id=data['discussion_id'],
            title=data['title'],
            author=author,
            date=data['date'],
            content=data['content'],
            comments=comments
        )

    def __eq__(self, other):
        if not isinstance(other, Discussion):
            return False
        return (
            self.url == other.url and
            self.discussion_id == other.discussion_id and
            self.title == other.title and
            self.author == other.author and
            self.date == other.date and
            self.content == other.content and
            self.comments == other.comments
        )