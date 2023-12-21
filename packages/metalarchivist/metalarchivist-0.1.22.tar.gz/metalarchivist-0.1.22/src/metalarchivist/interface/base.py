
from enum import StrEnum, auto
from abc import ABC
from dataclasses import dataclass, field, InitVar, asdict
from typing import ClassVar



class Period(StrEnum, ABC):
    EARLY = auto()
    MID = auto()
    LATER = auto()
    ALL = auto()
    ERROR = auto()

    @classmethod
    def has_value(cls, value) -> set:
        return value in cls._value2member_map_



class PageDataType(ABC):
    ...


@dataclass
class Page(ABC):
    data_type: ClassVar[type] = PageDataType

    i_total_records: InitVar[int] = field(kw_only=True)
    i_total_display_records: InitVar[int] = field(kw_only=True)
    s_echo: InitVar[int] = field(kw_only=True)
    aa_data: InitVar[list] = field(kw_only=True)

    metadata: dict = field(default_factory=dict, kw_only=True)

    total_records: int = field(init=False) 
    total_display_records: int = field(init=False)
    echo: int = field(init=False)
    data: list[data_type] = field(init=False)

    def __post_init__(self, i_total_records: int, i_total_display_records: int,
                      s_echo: int, aa_data: list):
        
        self.total_records = i_total_records
        self.total_display_records = i_total_display_records
        self.echo = s_echo
        self.data = sum(list(map(self._process, aa_data)), [])

        for key, value in self.metadata.items():
            setattr(self, key, value)

    def __init_subclass__(cls, /, data_type=PageDataType, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.data_type = data_type

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            class_str = str(self.__class__)
            raise TypeError(f'{class_str} objects can only be summed with other {class_str} objects')
        
        self.data += other.data
        return self

    def _process(self, record: list[str]) -> list[data_type]:
        return [self.data_type(record, **self.metadata)]
    
    def to_json(self):
        return list(map(asdict, self.data))


class Pages(ABC, list):
    data_type = Page

    def combine(self) -> data_type:
        first_page, *remaining = self
        return sum(remaining, start=first_page)
    
    def __init_subclass__(cls, /, data_type, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.data_type = data_type
