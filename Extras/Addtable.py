import sqlite3
CREATE_UPDATEDPLAYER_TABLE = """CREATE TABLE UpdatedplayerGame
                      (GAME_ID,
ASSISTS,
BARON_KILLS,
BARRACKS_KILLED,
BARRACKS_TAKEDOWNS,
BOUNTY_LEVEL,
CHAMPIONS_KILLED,
CHAMPION_TRANSFORM,
CONSUMABLES_PURCHASED,
DOUBLE_KILLS,
DRAGON_KILLS,
EXP,
FRIENDLY_DAMPEN_LOST,
FRIENDLY_HQ_LOST,
FRIENDLY_TURRET_LOST,
GAME_ENDED_IN_EARLY_SURRENDER,
GAME_ENDED_IN_SURRENDER,
GOLD_EARNED,
GOLD_SPENT,
HQ_KILLED,
HQ_TAKEDOWNS,
ID,
INDIVIDUAL_POSITION,
ITEM0,
ITEM1,
ITEM2,
ITEM3,
ITEM4,
ITEM5,
ITEM6,
ITEMS_PURCHASED,
KEYSTONE_ID,
KILLING_SPREES,
LARGEST_CRITICAL_STRIKE,
LARGEST_KILLING_SPREE,
LARGEST_MULTI_KILL,
LEVEL,
LONGEST_TIME_SPENT_LIVING,
MAGIC_DAMAGE_DEALT_PLAYER,
MAGIC_DAMAGE_DEALT_TO_CHAMPIONS,
MAGIC_DAMAGE_TAKEN,
MINIONS_KILLED,
NAME,
NEUTRAL_MINIONS_KILLED,
NEUTRAL_MINIONS_KILLED_ENEMY_JUNGLE,
NEUTRAL_MINIONS_KILLED_YOUR_JUNGLE,
NUM_DEATHS,
OBJECTIVES_STOLEN,
OBJECTIVES_STOLEN_ASSISTS,
PENTA_KILLS,
PERK_PRIMARY_STYLE,
PERK_SUB_STYLE,
PHYSICAL_DAMAGE_DEALT_PLAYER,
PHYSICAL_DAMAGE_DEALT_TO_CHAMPIONS,
PHYSICAL_DAMAGE_TAKEN,
PING,
PLAYER_POSITION,
QUADRA_KILLS,
SIGHT_WARDS_BOUGHT_IN_GAME,
SKIN,
SPELL1_CAST,
SPELL2_CAST,
SPELL3_CAST,
SPELL4_CAST,
STAT_PERK_0,
STAT_PERK_1,
STAT_PERK_2,
SUMMON_SPELL1_CAST,
SUMMON_SPELL2_CAST,
TEAM,
TEAM_EARLY_SURRENDERED,
TEAM_OBJECTIVE,
TEAM_POSITION,
TIME_CCING_OTHERS,
TIME_PLAYED,
TOTAL_DAMAGE_DEALT,
TOTAL_DAMAGE_DEALT_TO_BUILDINGS,
TOTAL_DAMAGE_DEALT_TO_CHAMPIONS,
TOTAL_DAMAGE_DEALT_TO_OBJECTIVES,
TOTAL_DAMAGE_DEALT_TO_TURRETS,
TOTAL_DAMAGE_SELF_MITIGATED,
TOTAL_DAMAGE_SHIELDED_ON_TEAMMATES,
TOTAL_DAMAGE_TAKEN,
TOTAL_HEAL,
TOTAL_HEAL_ON_TEAMMATES,
TOTAL_TIME_CROWD_CONTROL_DEALT,
TOTAL_TIME_SPENT_DEAD,
TOTAL_UNITS_HEALED,
TRIPLE_KILLS,
TRUE_DAMAGE_DEALT_PLAYER,
TRUE_DAMAGE_DEALT_TO_CHAMPIONS,
TRUE_DAMAGE_TAKEN,
TURRETS_KILLED,
TURRET_TAKEDOWNS,
UNREAL_KILLS,
VICTORY_POINT_TOTAL,
VISION_SCORE,
VISION_WARDS_BOUGHT_IN_GAME,
WARD_KILLED,
WARD_PLACED,
WARD_PLACED_DETECTOR,
WAS_EARLY_SURRENDER_ACCOMPLICE,
WIN,
FOREIGN KEY(ID) REFERENCES Players(Name)
                       )"""

con = sqlite3.connect("./instance/auction_alchemy.db")
cur = con.cursor()
cur.execute(CREATE_UPDATEDPLAYER_TABLE)
cur.execute("BEGIN;")
cur.execute("COMMIT;")
con.close()