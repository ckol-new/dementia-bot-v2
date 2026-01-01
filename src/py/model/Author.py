# author clas holds all data around an author/user that made a post, discussion, or comment
# username, user id, profile url
# DOES NOT GET EMBEDDED AS ANYTHING, JUST FOR BOOK KEEPING OF WHO SAID WHAT
class Author:
    def __init__(self, username: str, user_id: int, profile_url: str):
        self.username = username
        self.user_id = user_id
        self.profile_url = profile_url

    def to_dict(self):
        return {
            "username": self.username,
            "user_id": self.user_id,
            "profile_url": self.profile_url
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            username= data['username'],
            user_id= data['user_id'],
            profile_url= data['profile_url']
        )

    def __eq__(self, other):
        if not isinstance(other, Author):
            return False
        return (
            self.username == other.username and
            self.user_id == other.user_id and
            self.profile_url == other.profile_url
        )