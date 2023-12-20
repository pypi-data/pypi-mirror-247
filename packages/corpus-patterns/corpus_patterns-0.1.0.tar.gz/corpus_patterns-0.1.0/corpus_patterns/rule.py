from typing import Any, Self

from pydantic import BaseModel, StringConstraints, model_serializer
from typing_extensions import Annotated

from .utils import uncamel


class Rule(BaseModel):
    """`patterns` associated with a single `label` (optionally
    with an `id` as well that serve as the `ent_id_` in `spacy.tokens.Doc.ents`).
    It can also be used for pattern objects for `spacy.tokens.Doc.spans`. See generally:

    1. https://spacy.io/usage/rule-based-matching#entityruler-files
    2. https://spacy.io/usage/rule-based-matching#spanruler-files

    A `Rule` enables the creation of such pattern objects containing the same `Label`
    and custom `id`, if provided. Sample rule:

    ```py
    sample = Rule(
        id="ministry-labor",
        label="GOVT",
        patterns=[
            [
                {"LOWER": "the", "OP": "?"},
                {"LOWER": "ministry"},
                {"LOWER": "of"},
                {"LOWER": "labor"},
            ]
        ],
    )
    ```
    """

    id: str | None = None
    label: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            to_upper=True,
            pattern=r"^[A-Za-z]+$",
        ),
    ]
    patterns: list[list[dict[str, Any]]]

    def __str__(self) -> str:
        return f"<Rule {self.ent_id})>"

    def __repr__(self) -> str:
        return f"<Rule {self.ent_id}: {len(self.patterns)} patterns>"

    @property
    def ent_id(self):
        return self.id or "-".join(uncamel(self.label)).lower()

    @model_serializer
    def ser_model(self) -> list[dict[str, Any]]:
        """Following the pydantic convention for .model_dump(); instead of a traditional
        `dict` return, the function results in a serialized list of patterns
        for consumption by either `create_file()` or the _entity_ruler_ spacy pipeline.
        """
        return [{"id": self.ent_id, "label": self.label.upper(), "pattern": pattern} for pattern in self.patterns]

    @classmethod
    def setup(cls, label: str, patterns: list[list[dict[str, Any]]], id: str | None = None) -> Self:
        return cls(id=id, label=label.lower(), patterns=patterns)
