from typing import Any
from ..artifacts.artifact import Artifact

import numpy as np


class Character:

    @staticmethod
    def CreateChracterFromName(name: str, level: int = 90) -> 'Character':
        return Character(name, level=level)

    def __init__(self, name: str, *, level: int = 90) -> None:
        self.name = name
        self.level = level

        # 基础属性
        self.atk_base: int = 0
        self.atk_artifacts_extra: int = 0
        self.hpmax_base: int = 0
        self.hpmax_artifacts_extra: int = 0
        self.def_base: int = 0
        self.def_artifacts_extra: int = 0
        self.em_base: int = 0
        self.em_artifacts_extra: int = 0

        # 附加属性
        self.critical_rate_base: float = 0
        self.critical_rate_artifacts_extra: float = 0
        self.critical_damage_base: float = 0
        self.critical_damage_artifacts_extra: float = 0
        self.healing_bonus_base: float = 0
        self.healing_bonus_artifacts_extra: float = 0
        self.healing_effect_bonus_base: float = 0
        self.healing_effect_bonus_extra: float = 0 
        self.cd_shortage: float = 0
        self.elemental_damage_bonus_base: list[float] = [0 for _ in range(8)]
        self.elemental_damage_bonus_base_extra: list[float] = [0 for _ in range(8)]

        self.atk_talents: list[Any]
        self.artifacts: list[Artifact]

    @property
    def atk(self) -> int:
        return self.atk_base + self.atk_artifacts_extra

    @property
    def hpmax(self) -> int:
        return self.def_base + self.def_artifacts_extra
    
    @property
    def def_(self) -> int:
        return self.def_base + self.def_artifacts_extra
    
    @property
    def em(self) -> int:
        return self.em_base + self.em_artifacts_extra
    
    @property
    def critical_rate(self) -> float:
        return self.critical_rate_base + self.critical_rate_artifacts_extra
    
    @property
    def critical_damage(self) -> float:
        return self.critical_damage_base + self.critical_damage_artifacts_extra

    @property
    def elemental_damage_bonus(self) -> list[float]:
        return (np.array(self.elemental_damage_bonus_base) + np.array(self.elemental_damage_bonus_base_extra)).tolist()
