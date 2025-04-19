from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, Optional



@dataclass
class MediaDocument:
    id_object: Any
    name: str
    path: str
    date_start: date
    type_document: Any

    content: str = field(default="", init=False)
    keyword_match: Optional[Dict[Any, Any]] = field(default=None, init=False)

    # Property getter for `id` to mirror the original behavior
    @property
    def id(self):
        return self.id_object
