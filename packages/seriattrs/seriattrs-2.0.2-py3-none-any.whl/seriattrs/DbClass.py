import json
import random
from typing import Any, Self, get_args

from attr import define, fields, field

from .DbClassCreator import DbClassCreator
from .db_attrs_converter import db_attrs_converter
from .JsonEncoder import Decoder
from .JsonEncoder.default_json_encoder import json_encoder


@define
class DbClass(metaclass=DbClassCreator):
    _id = field(init=False, type=Any, factory=lambda: random.randint(-2**63, 2**63 - 1))

    def __attrs_post_init__(self):
        if hasattr(self, 'id'):
            self._id = self.id
        self._decode()

    def serialize(self) -> dict:
        from .DbClassLiteral import DbClassLiteral

        return json.loads(
            json.dumps(
                dict(
                    (
                        f.name,
                        getattr(self, f.name)._id
                        if isinstance(getattr(self, f.name), DbClass)
                        and not isinstance(getattr(self, f.name), DbClassLiteral)
                        else getattr(self, f.name),
                    )
                    for f in fields(type(self))
                ),
                cls=json_encoder,
            )
        )

    @classmethod
    def deserialize(cls, dictionary: dict) -> Self:
        deserialized = db_attrs_converter.structure(dictionary, cls)
        deserialized._fill_id(dictionary)
        return deserialized

    def _fill_id(self, dictionary: dict):
        from .DbClassLiteral import DbClassLiteral

        self._id = dictionary["_id"]
        for f in fields(type(self)):
            types = list(get_args(f.type))
            if isinstance(f.type, type):
                types.append(f.type)
            if any(issubclass(type(self) if field_type == Self else field_type, DbClassLiteral) for field_type in types):
                f.type._fill_id(getattr(self, f.name), dictionary[f.name])

    def _decode(self):
        for f in fields(type(self)):
            for decoder in Decoder.__subclasses__():
                if decoder.is_valid(f.type):
                    setattr(self, f.name, decoder.decode(getattr(self, f.name), f.type))
                    break
