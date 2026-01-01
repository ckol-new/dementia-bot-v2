import numpy as np
import json
import re
from time import perf_counter
from huggingface_hub import edit_discussion_comment
from sentence_transformers import SentenceTransformer
from sympy.logic.algorithms.z3_wrapper import encoded_cnf_to_z3_solver
from py.model.Comment import Comment
from py.model.EmbeddedComment import EmbeddedComment
from py.model.Discussion import Discussion
from py.model.EmbeddedDiscussion  import EmbeddedDiscussion

class ALZConnectedEncoder:
    @classmethod
    def break_into_sentence(cls, text: str) -> list:
        if not text: return None
        pattern = r"[.,?!;:\-\n\t]"
        sentences = re.split(pattern, text)
        return sentences

    @classmethod
    def encode_sentence(cls, model, sentence: str) -> np.ndarray:
        if not model:
            model = SentenceTransformer('all-MiniLM-L6-v2')
        return model.encode(sentence)

    @classmethod
    def encode_comment(cls, model, comment: Comment):
        # break content into sentences
        sentences = cls.break_into_sentence(comment.content)
        # encode each sentence
        encoded_sentences = [cls.encode_sentence(model, sentence) for sentence in sentences if sentences]

        # get encoded comment
        e_comment = EmbeddedComment(
            url=comment.url,
            author=comment.author,
            date=comment.date,
            sentences=sentences,
            content=encoded_sentences
        )
        return e_comment

    @classmethod
    def encode_discussion(cls, model, discussion: Discussion):
        # get encoded title
        encoded_title = cls.encode_sentence(model, discussion.title)

        # get encoded comment
        content_sentences = cls.break_into_sentence(discussion.content)
        encoded_content = [cls.encode_sentence(model, sentence) for sentence in content_sentences if content_sentences]

        # get encoded comments
        comments = discussion.comments
        culled_comments = []
        for comment in comments:
            if cls.cull_comment(comment):
                continue
            else: culled_comments.append(comment)

        encoded_comments = (cls.encode_comment(model, comment) for comment in culled_comments)

        # get encoded discussion
        e_discussion = EmbeddedDiscussion(
            url=discussion.url,
            discussion_id=discussion.discussion_id,
            title_string=discussion.title,
            title=encoded_title,
            author=discussion.author,
            date=discussion.date,
            sentences=discussion.content,
            content=encoded_content,
            comments=encoded_comments
        )

        return e_discussion

    @classmethod
    def cull_discussion(cls, discussion: Discussion):
        if not discussion.url: return True
        if not discussion.discussion_id: return True
        if not discussion.title: return True
        if not discussion.content: return True
        if not discussion.date: return True
        if not discussion.author: return True
        if not discussion.comments: return True

        return False

    @classmethod
    def cull_comment(cls, comment: Comment):
        if not comment.url: return True
        if not comment.author: return True
        if not comment.content: return True
        if not comment.date: return True

        return False


    @classmethod
    def encode_file(cls, scraped_file: str, encoded_output: str, model=None, timer: bool = False):
        start_time = perf_counter()
        if not model:
            model = SentenceTransformer('all-MiniLM-L6-v2')

        # get length of file
        length = None
        with open(scraped_file, 'r') as sf:
            length = sum([1 for _ in sf])

        # open file
        with open(scraped_file, 'r') as sf:
            with open(encoded_output, 'w') as ef:
                num = 0
                for line in sf:
                    if num % 10 == 0:
                        print(f'%{(num / length) * 100}')
                    num += 1
                    # get discussion obj
                    discussion = Discussion.from_dict(json.loads(line))

                    # if missing data field, do not encode
                    if cls.cull_discussion(discussion): continue

                    # get embedded discussion
                    e_discussion = cls.encode_discussion(model, discussion)

                    ef.write(json.dumps(e_discussion.to_dict()))
                    ef.write('\n')

        end_time = perf_counter()

        if timer: print(f'Time time to encode {end_time - start_time}')
