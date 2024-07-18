import dataclasses


@dataclasses.dataclass(frozen=True)
class DataclassValidationMixin:
    def __post_init__(self):
        for field in dataclasses.fields(self):
            if method := getattr(self, f"validate_{field.name}", None):
                object.__setattr__(self, field.name, method())
