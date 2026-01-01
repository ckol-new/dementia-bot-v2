import json
from sentence_transformers import SentenceTransformer
from py.model.Discussion import Discussion
from py.model.Comment import Comment
from py.model.EmbeddedDiscussion import EmbeddedDiscussion
from py.model.EmbeddedComment import EmbeddedComment
from py.model.QueryResult import QueryResultComment, QueryResultDiscussion
import numpy as np

# Query util class performs the query on the data set, Query result
class Query:
    # load embedded discussion object from line in encoded.jsonl
    # deserialize from jsonl
    # @param: pass function the line
    @classmethod
    def load_embedded_discussion(cls, line: str) -> EmbeddedDiscussion:
        e_discussion = EmbeddedDiscussion.from_dict(json.loads(line))
        return e_discussion

    # load embedded discussion object from line in encoded.jsonl
    # deserialize from jsonl
    # @param: pass function the line
    @classmethod
    def load_embedded_comment(cls, line: str) -> EmbeddedDiscussion:
        e_comment = EmbeddedComment.from_dict(json.loads(line))
        return e_comment

    # cosine similarity of two vectors: should all be size 384 if using all-MiniLM-L6-v2
    @classmethod
    def get_cosine_similarity(cls, vector1: np.ndarray, vector2: np.ndarray) -> np.float32:
        return vector1.dot(vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))

    # get similarity of title
    @classmethod
    def get_title_similarity(cls,query_vector: np.ndarray, title_vector: np.ndarray) -> np.float32:
        title_cos_similarity = cls.get_cosine_similarity(query_vector, title_vector)
        return title_cos_similarity

    # get similarity of each sentence of discussion content as a list of float32
    @classmethod
    def get_content_similarity(cls, query_vector: np.ndarray, content: list[np.ndarray]) -> list[np.float32]:
        content_cos_similarities: list[np.float32] = []

        for sentence_vector in content:
            cos_simil = cls.get_cosine_similarity(query_vector, sentence_vector)
            content_cos_similarities.append(cos_simil)

        return content_cos_similarities

    @classmethod
    def get_query_result_comment(cls, query_vector: np.ndarray, comment: Comment, embedded_comment: EmbeddedComment) -> QueryResultComment:
        cos_simil_content = cls.get_content_similarity(query_vector, embedded_comment.content)
        query_result_comment = QueryResultComment(url=comment.url, content=embedded_comment.sentences, content_results=cos_simil_content)
        return query_result_comment

    # get QueryResult for one discussion
    @classmethod
    def get_query_result_discussion(cls, query_vector: np.ndarray, scraped_line: str, encoded_line: str) -> QueryResultDiscussion:
        # get embedded discussion and unembedded discussion
        e_discussion = cls.load_embedded_discussion(encoded_line)
        e_comments = e_discussion.comments
        discussion = Discussion.from_dict(json.loads(scraped_line))
        comments = discussion.comments

        # get dictionary coupling embedded and unembedded comments
        coupled_dict = dict(zip(comments, e_comments))

        # get title similarity
        cos_simil_title = cls.get_title_similarity(query_vector, e_discussion.title)

        # discussion content similarity
        cos_simil_content = cls.get_content_similarity(query_vector, e_discussion.content)

        # get query result of comments: content similarity
        query_result_comments = []
        for e_comment, comment in coupled_dict:
            query_result_comment = cls.get_query_result_comment(query_vector, comment, e_comment)
            query_result_comments.append(query_result_comment)

        # get query result discussion object
        query_result_discussion = QueryResultDiscussion(
            url=e_discussion.url,
            title=discussion.title,
            title_result=cos_simil_title,
            author=discussion.author,
            content=e_discussion.sentences,
            content_results=cos_simil_content,
            comments=comments,
            comment_results=query_result_comments
        )

        return query_result_discussion

    # generate QueryResponse: limit is number of query result discussions it can hold (only holds the most similar)
    @classmethod
    def query(cls, query_string: str, scraped_file_path: str, embedded_file_path: str, model=None, limit=10):
        if not model:
            model = SentenceTransformer('all-MiniLM-L6-v2')
        query_vector = model.encode(query_string)




