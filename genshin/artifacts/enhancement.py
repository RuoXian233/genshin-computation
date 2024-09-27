from ..utils import enum_values
from .artifact import Artifact
from .artifact_locals import *
from ..locals import ElementType

import random

import numpy as np


class ArtifactEnhancement:
    
    def __init__(self, art: Artifact) -> None:
        assert art
        self.art = art

    def upgrade(self, level: int = 1) -> None:
        assert self.art.primary_attribute.level + level <= ARTIFACT_MAX_LEVEL, \
            f'圣遗物等级超出上限 (+{ARTIFACT_MAX_LEVEL})'
        # 判断圣遗物当前强化阶段
        current_state: int
        for i, point in enumerate(UPGRADE_POINTS):
            if self.art.primary_attribute.level < point:
                current_state = i
                break

        # 决定副词条强化次数
        level_tmp = level
        sub_attribute_upgrade_times = 0
        if level_tmp >= UPGRADE_POINTS[current_state] - self.art.primary_attribute.level:
            level_tmp -= UPGRADE_POINTS[current_state] - self.art.primary_attribute.level
            while level_tmp >= 0:
                sub_attribute_upgrade_times += 1
                level_tmp -= SUB_ATTRIBUTE_UPGRADE_INTERVAL
        
        # 分别强化主, 副词条 (等价于一起强化)
        self.art.primary_attribute.level += level
        for _ in range(sub_attribute_upgrade_times):
            self._upgrade_sub_attribute()
        
        for _ in range(level):
            self._upgrade_primary_attribute()

    def _upgrade_primary_attribute(self) -> None:
        if self.art.primary_attribute != Artifact.PrimaryAttributeType.elemental_damage_bonus:
            self.art.primary_attribute.value += PRIMARY_ATTRIBUTE_INCREAMENT[self.art.primary_attribute.attribute_type.value]
        elif self.art.primary_attribute.element_bonus_type == ElementType.none:
            self.art.primary_attribute.value += PRIMARY_ATTRIBUTE_INCREAMENT['物理伤害加成']
        else:
            self.art.primary_attribute.value += PRIMARY_ATTRIBUTE_INCREAMENT['元素伤害加成']            

    def _upgrade_sub_attribute(self) -> None:
        random_get_sub_attribute_value = \
                        lambda x: SUB_ATTRIBUTES_INITIAL_VALUE[x] / sorted(SUB_ATTRIBUTES_INITIAL_RATIO)[0] * random.choice(SUB_ATTRIBUTES_INITIAL_RATIO)
        
        # 若副词条数不满足五星圣遗物副词条上限，则优先抽取一条副词条
        if len(self.art.sub_attributes) < ARTIFACT_MAX_SUB_ATTRIBUTES_COUNT:
            # 过滤已有词条属性
            avalible_sub_attributes_value = list(set(enum_values(Artifact.SubAttributeType)) - set([i.attribute_type.value for i in self.art.sub_attributes]))
            sub_attributes_weight = np.array([SUB_ATTRIBUTE_WEIGHT[v] for v in avalible_sub_attributes_value])
            
            # 抽取副词条
            result = np.random.choice(
                np.array(avalible_sub_attributes_value),
                size=1, replace=False,
                p=sub_attributes_weight / sum(sub_attributes_weight) 
            )

            value = random_get_sub_attribute_value(result[0])
            self.art.sub_attributes.append(
                Artifact.ArtifactsSubAttributes(Artifact.SubAttributeType(result), value)
            )
            return
        
        # 等概率强化一条副词条
        sub_attribute_index = random.randint(0, ARTIFACT_MAX_SUB_ATTRIBUTES_COUNT - 1)
        enhanced_value = random_get_sub_attribute_value(self.art.sub_attributes[sub_attribute_index].attribute_type.value)
        self.art.sub_attributes[sub_attribute_index].value += enhanced_value
        # 记录强化历史
        self.art.previous_enhanced_attribute_type.append(self.art.sub_attributes[sub_attribute_index].attribute_type)        
        self.art.delta.append(enhanced_value)
