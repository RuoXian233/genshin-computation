import random

from enum import Enum
from dataclasses import dataclass
from typing import Any
from ..utils import create_enum_by_index, format_num, enum_values
from ..locals import ElementType, get_element_label
from .artifact_locals import *

import numpy as np


class Artifact:

    @staticmethod 
    def choose(possibilities: dict[Any, float]) -> Any:
        assert possibilities
        percentage_accuracy = 10 ** max([len(str(possibility)) - 2 for possibility in possibilities.values()])
        value = random.randint(1, percentage_accuracy)
        intervals: list[tuple[tuple[int, int], Any]] = []
        current, possibilities_values = 1, tuple(possibilities.values())
        
        for i, k in enumerate(possibilities):
            next_current = int(current + possibilities_values[i] * percentage_accuracy)
            intervals.append(((current, next_current), k))
            current = next_current

        for interval in intervals:
            if value in range(*interval[0]):
                return interval[1]
            
    @staticmethod
    def evaluate_by_crit(art: 'Artifact') -> float:
        score = 0
        if art.primary_attribute == Artifact.PrimaryAttributeType.critical_rate:
            score += art.primary_attribute.value * 2 * 100
        elif art.primary_attribute == Artifact.PrimaryAttributeType.critical_damage:
            score += art.primary_attribute.value * 100
        
        for sub_attribute in art.sub_attributes:
            if sub_attribute.attribute_type == Artifact.SubAttributeType.critical_rate:
                score += sub_attribute.value * 2 * 100
            elif sub_attribute.attribute_type == Artifact.SubAttributeType.critical_damage:
                score += sub_attribute.value * 2 * 100
        return score


    class Kits(Enum):
        denouement_of_sin = ('谐律', ('逐影猎人', '黄金剧团'))

    class Parts(Enum):
        flower_of_life = '生之花'
        plume_of_death = '死之羽'
        sands_of_eon = '时之沙'
        goblet_of_eonothem = '空之杯'
        circlet_of_logos = '理之冠'

    class PrimaryAttributeType(Enum):
        atk_value = '攻击力'
        atk_percentage = '攻击力%'
        hp_value = '生命值'
        hp_percentage = '生命值%'
        elemental_recharge = '元素充能效率'
        elemental_master = '元素精通'
        critical_rate = '暴击率'
        critical_damage = '暴击伤害'
        def_percentage = '防御力%'
        elemental_damage_bonus = '元素伤害加成'
        healing_bonus = '治疗加成'

    class SubAttributeType(Enum):
        atk_value = '攻击力'
        atk_percentage = '攻击力%'
        def_value = '防御力'
        def_percentage = '防御力%'
        hp_value = '生命值'
        hp_percentage = '生命值%'
        critical_rate = '暴击率'
        critical_damage = '暴击伤害'
        elemental_recharge = '元素充能效率'
        elemental_master = '元素精通'

    @dataclass
    class AritfactPrimaryAttribute:
        attribute_type: 'Artifact.PrimaryAttributeType'
        value: float
        level: int
        element_bonus_type: ElementType | None


    @dataclass
    class ArtifactsSubAttributes:
       attribute_type: 'Artifact.SubAttributeType'
       value: float

    def __init__(self, kits: Kits) -> None:
        self.kits = kits
        self.kit = ''
        self.part: Artifact.Parts
        self.determine_kit_and_part()

        self.artifact_enhanced_point_count: int = 4
        self.primary_attribute: Artifact.AritfactPrimaryAttribute
        self.determine_primary_attribute()
        self.sub_attributes: list[Artifact.ArtifactsSubAttributes] = []
        self.determine_sub_attributes()

        self.delta: list[float] = []
        self.previous_enhanced_attribute_type: list['Artifact.SubAttributeType'] = []

    def determine_kit_and_part(self) -> None:
        self.kit = self.kits.value[1][random.randint(0, 1)]
        self.part = create_enum_by_index(Artifact.Parts, random.randint(0, 4))

    def determine_primary_attribute(self) -> None:
        assert self.part
        attribute_type: Artifact.PrimaryAttributeType
        # 决定主词条属性
        match self.part:
            case Artifact.Parts.flower_of_life:
                attribute_type = Artifact.PrimaryAttributeType.hp_value
            case Artifact.Parts.plume_of_death:
                attribute_type = Artifact.PrimaryAttributeType.atk_value
            case _:
                attribute_type = Artifact.PrimaryAttributeType(
                    Artifact.choose(PRIMARY_ATTRIBUTES_DISTRIBUTION[self.part.value])
                )
        
        # 获取主词条初始值
        if attribute_type != Artifact.PrimaryAttributeType.elemental_damage_bonus:
            self.primary_attribute = Artifact.AritfactPrimaryAttribute(
                attribute_type, PRIMARY_ATTRIBUTES_INITIAL_VALUE[attribute_type.value],
                0, None
            )
        else:
            # 若是元素伤害主词条，那么等可能决定其对应的加成类型
            bonus_type = create_enum_by_index(ElementType, random.randint(0, 7))
            if bonus_type.value == 0:
                self.primary_attribute = Artifact.AritfactPrimaryAttribute(
                    attribute_type, PRIMARY_ATTRIBUTES_INITIAL_VALUE['物理伤害加成'],
                    0, bonus_type
                )
            else:
                self.primary_attribute = Artifact.AritfactPrimaryAttribute(
                    attribute_type, PRIMARY_ATTRIBUTES_INITIAL_VALUE['元素伤害加成'],
                    0, bonus_type
                )

    def determine_sub_attributes(self, minimal_count: int = 3) -> None:
        assert self.primary_attribute
        # 过滤主词条属性
        avalible_sub_attributes_value = list(set(enum_values(Artifact.SubAttributeType)) - set((self.primary_attribute.attribute_type.value, )))
        sub_attributes_weight = np.array([SUB_ATTRIBUTE_WEIGHT[v] for v in avalible_sub_attributes_value])
        
        # 决定初始词条数
        sub_attributes_count = minimal_count
        if Artifact.choose(SUB_ATTRIBUTES_COUNT_POSSIBILITY_DISTRIBUTION) == 'n + 1':
            sub_attributes_count += 1
        self.artifact_enhanced_point_count += sub_attributes_count == ARTIFACT_MAX_SUB_ATTRIBUTES_COUNT
        
        # 抽取副词条
        result = np.random.choice(
            np.array(avalible_sub_attributes_value),
            size=sub_attributes_count, replace=False,
            p=sub_attributes_weight / sum(sub_attributes_weight) 
        )
        for a in result.tolist():
            sub_attribute_type = Artifact.SubAttributeType(a)
            value = SUB_ATTRIBUTES_INITIAL_VALUE[a] / sorted(SUB_ATTRIBUTES_INITIAL_RATIO)[0] * random.choice(SUB_ATTRIBUTES_INITIAL_RATIO)
            self.sub_attributes.append(
                Artifact.ArtifactsSubAttributes(sub_attribute_type, value)
            )

    def show(self) -> None:
        assert self.primary_attribute
        print(f'{"-" * 5} {self.kit} | {self.part.value} (+{self.primary_attribute.level}) {"-" * 5}')
        if self.primary_attribute.attribute_type != Artifact.PrimaryAttributeType.elemental_damage_bonus:
            print(f'  主属性 - {self.primary_attribute.attribute_type.value.rstrip('%')}: {format_num(self.primary_attribute.value)}')
        else:
            assert self.primary_attribute.element_bonus_type
            print(f'  主属性 - {get_element_label(self.primary_attribute.element_bonus_type)}{self.primary_attribute.attribute_type.value.rstrip('%')}: {format_num(self.primary_attribute.value)}')
        print('  副属性')
        for sub_attribute in self.sub_attributes:
            print(f'   | {sub_attribute.attribute_type.value.rstrip('%')} +{format_num(sub_attribute.value)}')
        print()
        print('圣遗物强化记录: ')
        if not len(self.delta):
            print('  未强化副词条')
            return
        i = 0 + self.artifact_enhanced_point_count < ARTIFACT_MAX_SUB_ATTRIBUTES_COUNT + 1
        for attr_type, delta_value in zip(self.previous_enhanced_attribute_type, self.delta, strict=True):
            i += 1
            print(f'  +{i * 4}: 属性: {attr_type.value}, 强化值: +{format_num(delta_value)}')


class CompoundedArtifact(Artifact):
    pass
