import os
import sys
import csv
import math
from enum import Enum, EnumType
from typing import Callable, Self, TextIO, Any, TypeVar, Generic

from .locals import ElementType, Data, AttributesType
from prettytable import PrettyTable

MAX_DIGITS = 8
KEEP_DIGITS = 3


def enum_member_value(e: EnumType, index: int) -> Any:
    return [enum_member.value for enum_member in e][index] # type: ignore

def enum_values(e: EnumType) -> list[Any]:
    return [enum_member.value for enum_member in e] # type: ignore

def create_enum_by_index(e: EnumType, index: int) -> Any:
    return e(list(e.__members__.values())[index])

def format_num(num: float | int, rount: bool = True) -> str:
    if abs(num) > 5:
        if math.isclose(num, int(num)):
            return f'{int(num)}'
        else:
            return f'{num}' if not round else f'{round(num)}'
    else:
        if not round:
            fs = f'{num * 100}%'
            trim_zero_count = 0
            for d in reversed(fs):
                trim_zero_count += d == '0'
            return fs[:4 - (trim_zero_count != 0)] + '%' if len(fs) > MAX_DIGITS else fs
        else:
            return f'{round(num * 100, 1)}%'

class Scanner:
    stdin = sys.stdin

    def __init__(self, stream: TextIO) -> None:
        self.lines = []
        self.input_stream = stream

    def readlines(self, terminator: str='\n') -> Self:
        while (line := self.input_stream.readline()) != terminator:
            self.lines.append(line)
        return self

    def to(self, file: str, append: bool=False) -> None:
        with open(file, f'{"a" if append else "w"}', encoding='utf-8') as stream:
            for line in self.lines:
                stream.write(line)


class AttributesReader:

    @staticmethod
    def get_database_path() -> str:
        return os.getcwd() + '/genshin/data'
    
    class FileType(Enum):
        csv = 'csv'
        json = 'json'
        txt = 'text'

    def __init__(self, file: str) -> None:
        self.file = file
        assert os.path.isfile(file), 'Not a file'
        self.filetype = getattr(AttributesReader.FileType, file.split(os.path.sep)[-1].split('.')[1])

    def csv_reader(self, stream: TextIO) -> Any:
        for row in csv.reader(stream):
            yield row

    def text_reader(self, stream: TextIO) -> Any:
        for line in stream.readlines():
            yield line.strip()

    def read(self) -> list[Any]:
        with open(self.file, 'r', encoding='utf-8') as f:
            return [item for item in getattr(self, f'{self.filetype.value}_reader')(f)]
                

T = TypeVar('T', bound=Enum)
class DataFormatter(Generic[T]):

    RawAttributesData = list[list[str]]
    AttributesMapping = list[dict[str, Any]]

    def __init__(self) -> None:
        pass

    @staticmethod
    def format_attributes_data(data: RawAttributesData, value_T: type=int) -> AttributesMapping:
        attributes_mapping: DataFormatter.AttributesMapping = []
    
        for group in data:
            character_tmp_group: list[str] = []
            for index, item in enumerate(group):
                if index != len(group) - 1:
                    character_tmp_group.append(item)
                else:
                    for character in character_tmp_group:
                        attributes_mapping.append({character: value_T(item)})
        return attributes_mapping
    
    def format_classification_data(self, data: list[Any], enumeratable: EnumType) -> dict[str, T]:
        result = {}
        for index, character_group in enumerate(data):
            for character in character_group.split(','):
                result[character] = enumeratable(index + 1)
        return result
    
    
    @staticmethod
    def as_dict(attr_mapping: AttributesMapping) -> dict[str, Any]:
        d = {}
        for mapping in attr_mapping:
            for c, v in mapping.items():
                d[c] = v 
        return d
    

class Reader:
    @staticmethod
    def read_base_attribute_type_data(file: str) -> dict[str, Any]:
        return DataFormatter.as_dict(
            DataFormatter.format_attributes_data(
                AttributesReader(f'{AttributesReader.get_database_path()}/{file}').read()
            )
        )

    @staticmethod
    def read_element_classification() -> dict[str, ElementType]:
        return DataFormatter[ElementType]().format_classification_data(
            AttributesReader(f'{AttributesReader.get_database_path()}/{Data.character_element_mapping_data}').read(),
            ElementType
        )
    
    @staticmethod
    def read_attribute_bonus_data() -> dict[str, AttributesType]:
        return DataFormatter[AttributesType]().format_classification_data(
            AttributesReader(f'{AttributesReader.get_database_path()}/{Data.extra_bonus_attributes_data}').read(),
            AttributesType
        )
    
    @staticmethod
    def _read_multipliers(file: str) -> dict[str, tuple[float, ...]]:
        multipliers: dict[str, tuple[float, ...]] = {}
        raw_data = AttributesReader(f'{AttributesReader.get_database_path()}/{file}').read()
        for row in raw_data:
            multipliers[row[0]] = (float(row[1]), float(row[2]))
        return multipliers

    @staticmethod
    def read_lvl_multipiler() -> dict[str, tuple[float, float]]:
        # lvl_multipilers: dict[str, tuple[float, float]] = {}
        # raw_data = AttributesReader(f'{AttributesReader.get_database_path()}/{Data.level_multiplier_data}').read()
        # for row in raw_data:
        #     lvl_multipilers[row[0]] = (float(row[1]), float(row[2]))
        # return lvl_multipilers
        return Reader._read_multipliers(Data.level_multiplier_data) # type: ignore
    
    @staticmethod
    def read_attributes_bonus_multipliers() -> dict[AttributesType, tuple[float, float]]:
        m = Reader._read_multipliers(Data.extra_bonus_multiplier_data)
        return {AttributesType(int(k)): mul for k, mul in m.items() } # type: ignore

    @staticmethod
    def read_star_classification() -> dict[str, bool]:
        stars_mapping = {}
        raw_data = AttributesReader(f'{AttributesReader.get_database_path()}/{Data.character_star_mapping_data}').read()
        assert len(raw_data) == 2
        for idx, row in enumerate(raw_data):
            for character in row.split(','):
                stars_mapping[character] = bool(idx)
        return stars_mapping


def print_attr_table(fields: list[str], attr_name_map: dict[str, list[str]], o: Any, default: Any, stream: TextIO=sys.stdout, round_digits: int=-1, percentage: bool=True, percentage_keep_maximum: int=5, floating_forced_maximum: int=10, floating_ignore: bool=True) -> None:
    table = PrettyTable(fields)
    def parse(s: Any) -> str:
        if not isinstance(s, float):
            return str(s)
        else:
            s_new = s
            if abs(s) > floating_forced_maximum:
                match round_digits:
                    case -1:
                        pass
                    case 0:
                        s_new = int(s)
                    case _:
                        s_new = round(s, round_digits)

            def ignore(fnum: float) -> float:
                if len(str(fnum)) > 16 and math.isclose(fnum, int(fnum) + 1) and floating_ignore:
                    return int(fnum) + 1.0
                else:
                    return fnum

            if abs(s) < percentage_keep_maximum and percentage:
                return str(ignore(s_new * 100)) + '%'
            else:
                return str(ignore(s_new))


    for label, attr_names in attr_name_map.items():
        attr_values = [label] + [parse(getattr(o, attr_name)) for attr_name in attr_names]
        if len(attr_values) != len(fields):
            for _ in range(0, len(fields) - len(attr_values)):
                attr_values.append(str(default))
        table.add_row(attr_values)
    
    stream.write(table.get_string() + '\n')
