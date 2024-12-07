from dataclasses import dataclass

from .....shared_kernel.mixins import DataclassValidationMixin


@dataclass(frozen=True)
class CommentValue(DataclassValidationMixin):
    pass
