"""JSON utilities for CloudEvents."""
from datetime import datetime
from decimal import Decimal
from json import JSONEncoder  # pylint: disable=E0401,E0611
from typing import Any, Dict
from uuid import UUID

from pydantic import BaseModel  # pylint: disable=E0401,E0611
from typing_extensions import override


class CloudEncoder(JSONEncoder):
    """
    Encoder for:
    -----------
    - datetime.datetime
    - uuid.UUID
    - float
    """

    @override
    def default(self, o: Any):
        """Jsonifier."""
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, UUID):
            return str(o)
        if isinstance(o, float):
            return Decimal(str(o))
        if isinstance(o, BaseModel):
            return o.dict()
        return super().default(o)


def parse_json_hook(dct: Dict[str, Any]):
    """Casts floats to decimals."""
    for k, v in dct.items():
        if isinstance(v, float):
            dct[k] = Decimal(str(v))

    return dct


def jsonify(data: Any) -> str:
    """
    Convert data to JSON.
    """
    return CloudEncoder().encode(data)
