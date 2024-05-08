from dataclasses import dataclass
from .comment import CommentValue


@dataclass(frozen=True)
class CommentStack:
    _comments = []

    def retrieve_comments(self) -> list[CommentValue]:
        return self._comments

    def add_comment(self, comment_value: CommentValue):
        self._comments.append(comment_value)

    def __len__(self) -> int:
        return len(self._comments)

    def clean_restaurants(self):
        self._comments.clear()
