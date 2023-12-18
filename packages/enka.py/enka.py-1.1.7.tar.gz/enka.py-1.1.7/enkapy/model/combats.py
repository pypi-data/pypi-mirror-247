from pydantic import BaseModel, Field


class CharacterCombat(BaseModel):
    BASE_HP: float = Field(0, alias="1")
    FIGHT_PROP_HP: float = Field(0, alias="2")
    FIGHT_PROP_HP_PERCENT: float = Field(0, alias="3")
    FIGHT_PROP_BASE_ATTACK: float = Field(0, alias="4")
    FIGHT_PROP_ATTACK: float = Field(0, alias="5")
    FIGHT_PROP_ATTACK_PERCENT: float = Field(0, alias="6")
    FIGHT_PROP_BASE_DEFENSE: float = Field(0, alias="7")
    FIGHT_PROP_DEFENSE: float = Field(0, alias="8")
    FIGHT_PROP_DEFENSE_PERCENT: float = Field(0, alias="9")
    FIGHT_PROP_BASE_SPEED: float = Field(0, alias="10")
    FIGHT_PROP_SPEED_PERCENT: float = Field(0, alias="11")
    FIGHT_PROP_HP_MP_PERCENT: float = Field(0, alias="12")
    FIGHT_PROP_ATTACK_MP_PERCENT: float = Field(0, alias="13")
    FIGHT_PROP_CRITICAL: float = Field(0, alias="20")
    FIGHT_PROP_ANTI_CRITICAL: float = Field(0, alias="21")
    FIGHT_PROP_CRITICAL_HURT: float = Field(0, alias="22")
    FIGHT_PROP_CHARGE_EFFICIENCY: float = Field(0, alias="23")
    FIGHT_PROP_ADD_HURT: float = Field(0, alias="24")
    FIGHT_PROP_SUB_HURT: float = Field(0, alias="25")
    FIGHT_PROP_HEAL_ADD: float = Field(0, alias="26")
    FIGHT_PROP_HEALED_ADD: float = Field(0, alias="27")
    FIGHT_PROP_ELEMENT_MASTERY: float = Field(0, alias="28")
    FIGHT_PROP_PHYSICAL_SUB_HURT: float = Field(0, alias="29")
    FIGHT_PROP_PHYSICAL_ADD_HURT: float = Field(0, alias="30")
    FIGHT_PROP_DEFENCE_IGNORE_RATIO: float = Field(0, alias="31")
    FIGHT_PROP_DEFENCE_IGNORE_DELTA: float = Field(0, alias="32")
    FIGHT_PROP_FIRE_ADD_HURT: float = Field(0, alias="40")
    FIGHT_PROP_ELEC_ADD_HURT: float = Field(0, alias="41")
    FIGHT_PROP_WATER_ADD_HURT: float = Field(0, alias="42")
    FIGHT_PROP_GRASS_ADD_HURT: float = Field(0, alias="43")
    FIGHT_PROP_WIND_ADD_HURT: float = Field(0, alias="44")
    FIGHT_PROP_ROCK_ADD_HURT: float = Field(0, alias="45")
    FIGHT_PROP_ICE_ADD_HURT: float = Field(0, alias="46")
    FIGHT_PROP_HIT_HEAD_ADD_HURT: float = Field(0, alias="47")
    FIGHT_PROP_FIRE_SUB_HURT: float = Field(0, alias="50")
    FIGHT_PROP_ELEC_SUB_HURT: float = Field(0, alias="51")
    FIGHT_PROP_WATER_SUB_HURT: float = Field(0, alias="52")
    FIGHT_PROP_GRASS_SUB_HURT: float = Field(0, alias="53")
    FIGHT_PROP_WIND_SUB_HURT: float = Field(0, alias="54")
    FIGHT_PROP_ROCK_SUB_HURT: float = Field(0, alias="55")
    FIGHT_PROP_ICE_SUB_HURT: float = Field(0, alias="56")
    FIGHT_PROP_EFFECT_HIT: float = Field(0, alias="60")
    FIGHT_PROP_EFFECT_RESIST: float = Field(0, alias="61")
    FIGHT_PROP_FREEZE_RESIST: float = Field(0, alias="62")
    FIGHT_PROP_TORPOR_RESIST: float = Field(0, alias="63")
    FIGHT_PROP_DIZZY_RESIST: float = Field(0, alias="64")
    FIGHT_PROP_FREEZE_SHORTEN: float = Field(0, alias="65")
    FIGHT_PROP_TORPOR_SHORTEN: float = Field(0, alias="66")
    FIGHT_PROP_DIZZY_SHORTEN: float = Field(0, alias="67")
    FIGHT_PROP_MAX_FIRE_ENERGY: float = Field(0, alias="70")
    FIGHT_PROP_MAX_ELEC_ENERGY: float = Field(0, alias="71")
    FIGHT_PROP_MAX_WATER_ENERGY: float = Field(0, alias="72")
    FIGHT_PROP_MAX_GRASS_ENERGY: float = Field(0, alias="73")
    FIGHT_PROP_MAX_WIND_ENERGY: float = Field(0, alias="74")
    FIGHT_PROP_MAX_ICE_ENERGY: float = Field(0, alias="75")
    FIGHT_PROP_MAX_ROCK_ENERGY: float = Field(0, alias="76")
    FIGHT_PROP_SKILL_CD_MINUS_RATIO: float = Field(0, alias="80")
    FIGHT_PROP_SHIELD_COST_MINUS_RATIO: float = Field(0, alias="81")

    FIGHT_PROP_CUR_FIRE_ENERGY: float = Field(0, alias="1000")
    FIGHT_PROP_CUR_ELEC_ENERGY: float = Field(0, alias="1001")
    FIGHT_PROP_CUR_WATER_ENERGY: float = Field(0, alias="1002")
    FIGHT_PROP_CUR_GRASS_ENERGY: float = Field(0, alias="1003")
    FIGHT_PROP_CUR_WIND_ENERGY: float = Field(0, alias="1004")
    FIGHT_PROP_CUR_ICE_ENERGY: float = Field(0, alias="1005")
    FIGHT_PROP_CUR_ROCK_ENERGY: float = Field(0, alias="1006")
    FIGHT_PROP_CUR_HP: float = Field(0, alias="1010")

    FIGHT_PROP_MAX_HP: float = Field(0, alias="2000")
    FIGHT_PROP_CUR_ATTACK: float = Field(0, alias="2001")
    FIGHT_PROP_CUR_DEFENSE: float = Field(0, alias="2002")
    FIGHT_PROP_CUR_SPEED: float = Field(0, alias="2003")

    FIGHT_PROP_NONEXTRA_ATTACK: float = Field(0, alias="3000")
    FIGHT_PROP_NONEXTRA_DEFENSE: float = Field(0, alias="3001")
    FIGHT_PROP_NONEXTRA_CRITICAL: float = Field(0, alias="3002")
    FIGHT_PROP_CUR_SPEED: float = Field(0, alias="3003")
    FIGHT_PROP_NONEXTRA_CRITICAL_HURT: float = Field(0, alias="3004")
    FIGHT_PROP_NONEXTRA_CHARGE_EFFICIENCY: float = Field(0, alias="3005")
    FIGHT_PROP_NONEXTRA_ELEMENT_MASTERY: float = Field(0, alias="3006")
    FIGHT_PROP_NONEXTRA_PHYSICAL_SUB_HURT: float = Field(0, alias="3007")
    FIGHT_PROP_NONEXTRA_FIRE_ADD_HURT: float = Field(0, alias="3008")
    FIGHT_PROP_NONEXTRA_ELEC_ADD_HURT: float = Field(0, alias="3009")
    FIGHT_PROP_NONEXTRA_WATER_ADD_HURT: float = Field(0, alias="3010")
    FIGHT_PROP_NONEXTRA_GRASS_ADD_HURT: float = Field(0, alias="3011")
    FIGHT_PROP_NONEXTRA_WIND_ADD_HURT: float = Field(0, alias="3012")
    FIGHT_PROP_NONEXTRA_ROCK_ADD_HURT: float = Field(0, alias="3013")
    FIGHT_PROP_NONEXTRA_ICE_ADD_HURT: float = Field(0, alias="3014")
    FIGHT_PROP_NONEXTRA_FIRE_SUB_HURT: float = Field(0, alias="3015")
    FIGHT_PROP_NONEXTRA_ELEC_SUB_HURT: float = Field(0, alias="3016")
    FIGHT_PROP_NONEXTRA_WATER_SUB_HURT: float = Field(0, alias="3017")
    FIGHT_PROP_NONEXTRA_GRASS_SUB_HURT: float = Field(0, alias="3018")
    FIGHT_PROP_NONEXTRA_WIND_SUB_HURT: float = Field(0, alias="3019")
    FIGHT_PROP_NONEXTRA_ROCK_SUB_HURT: float = Field(0, alias="3020")
    FIGHT_PROP_NONEXTRA_ICE_SUB_HURT: float = Field(0, alias="3021")
    FIGHT_PROP_NONEXTRA_SKILL_CD_MINUS_RATIO: float = Field(0, alias="3022")
    FIGHT_PROP_NONEXTRA_SHIELD_COST_MINUS_RATIO: float = Field(0, alias="3023")
    FIGHT_PROP_NONEXTRA_PHYSICAL_ADD_HURT: float = Field(0, alias="3024")

    RAW: dict = {}

    def __init__(self, **data):
        super().__init__(**data)
        self.RAW = data
