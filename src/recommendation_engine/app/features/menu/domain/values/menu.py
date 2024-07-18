from dataclasses import dataclass

from recommendation_engine.app.shared_kernel.mixins import DataclassValidationMixin


@dataclass(frozen=True)
class MenuValue(DataclassValidationMixin):
    pass
