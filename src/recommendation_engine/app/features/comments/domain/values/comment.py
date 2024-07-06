from dataclasses import dataclass
from ....mixins import DataclassValidationMixin


@dataclass(frozen=True)
class CommentValue(DataclassValidationMixin):
    pass
