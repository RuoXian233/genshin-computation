from enum import Enum


class Data:
    base_def_data = 'base-attributes-def-lv90.csv'
    base_atk_data = 'base-attributes-atk-lv90.csv'
    base_hpmax_data = 'base-attributes-hpmax-lv90.csv'
    level_multiplier_data = 'lvl-multiplier.csv'
    character_element_mapping_data = 'character-element-mapping.txt'
    character_star_mapping_data = 'character-star-mapping.txt'
    extra_bonus_multiplier_data = 'extra-bonus-multiplier.csv'
    extra_bonus_attributes_data = 'extra-attributes-bonus.txt'

class ElementType(Enum):
    none = 0
    hydro = 1
    pyro = 2
    cyro = 3
    electro = 4
    anemo = 5
    geo = 6
    dendro = 7

def get_element_label(e: ElementType) -> str:
    match e:
        case ElementType.none:
            raise Exception('No label found')
        case ElementType.hydro:
            return '水'
        case ElementType.pyro:
            return '火'
        case ElementType.cyro:
            return '冰'
        case ElementType.electro:
            return '雷'
        case ElementType.anemo:
            return '风'
        case ElementType.geo:
            return '岩'
        case ElementType.dendro:
            return '草'
        case _:
            raise Exception('Invilid access')


class DamageElementType(Enum):
    none = 0
    hydro = 1
    pyro = 2
    cyro = 3
    electro = 4
    anemo = 5
    geo = 6
    dendro = 7

class AttributesType(Enum):
    attack = 1
    hp = 2
    element_damage_bonus = 3
    element_recharge = 4
    critcal_dmg = 5
    critical_rate = 6
    elemental_master = 7
    healing_bonus = 8
    def_ = 9
    physical_dmg_bonus = 10


class Constants:
    MAX_CHARACTER_LEVEL = 90
    BASE_CRITICAL_RATE = 0.05
    BASE_CRITICAL_DAMAGE = 0.5
    BASE_EM = 0
    BASE_ELEMENT_DAMAGE_BOUNS = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    ELEMENT_LABELS = ('物理', '水元素', '火元素', '冰元素', '雷元素', '风元素', '岩元素', '草元素')
    BASE_ELEMENT_RECHARGE = 1.0
    BASE_HEALING_BONUS = 0.0
    ENEMY_BASE_DEF_MULTIPLIER = 5
    ENEMY_EXTRA_DEF_VALUE = 500
