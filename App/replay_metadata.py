import json
import os
import sqlite3

POSITIONS = ["TOP", "JUNGLE", "MID", "ADC", "SUPPORT"]
global fileName
global root_dir
def get_metadata(filename):
    print(filename)
    with open(filename, "rb") as f:
        # Magic
        magic = str(f.read(4), encoding="utf-8")

        # Length fields
        lengths_buffer = []
        f.seek(262)
        length_field_buffer = f.read(26)
        metadata_offset = length_field_buffer[6:10]
        metadata_length = length_field_buffer[10:14]

        metadata_offset = int.from_bytes(metadata_offset, byteorder='little')
        metadata_length = int.from_bytes(metadata_length, byteorder='little')

        # Metadata
        f.seek(metadata_offset)
        replay_metadata = f.read(metadata_length)
        replay_metadata = json.loads(str(replay_metadata, encoding="utf-8"))
        
        stats_json = json.loads(replay_metadata["statsJson"])

        #champs = [s["SKIN"] for s in stats_json]

        return replay_metadata, stats_json

def insert_game(cur, org, metadata, game_id):
    global fileName
    global root_dir
    surrender = any([m["GAME_ENDED_IN_SURRENDER"] for m in metadata])
    surrender = 1 if surrender else 0
    early_surrender = any([m["GAME_ENDED_IN_EARLY_SURRENDER"] for m in metadata])
    early_surrender = 1 if early_surrender else 0
    for i, player in enumerate(metadata):
        GAME_ID = os.path.basename(fileName).split(".")[0].split("-")[1]
        print(root_dir)
        ASSISTS = player["ASSISTS"],
        BARON_KILLS= player["BARON_KILLS"] 
        BARRACKS_KILLED= player["BARRACKS_KILLED"] 
        BARRACKS_TAKEDOWNS= player["BARRACKS_TAKEDOWNS"] 
        BOUNTY_LEVEL= player["BOUNTY_LEVEL"]
        CHAMPIONS_KILLED= player["CHAMPIONS_KILLED"] 
        CHAMPION_TRANSFORM= player["CHAMPION_TRANSFORM"] 
        CONSUMABLES_PURCHASED= player["CONSUMABLES_PURCHASED"] 
        DOUBLE_KILLS= player["DOUBLE_KILLS"] 
        DRAGON_KILLS= player["DRAGON_KILLS"] 
        EXP= player["EXP"] 
        FRIENDLY_DAMPEN_LOST= player["FRIENDLY_DAMPEN_LOST"] 
        FRIENDLY_HQ_LOST= player["FRIENDLY_HQ_LOST"] 
        FRIENDLY_TURRET_LOST= player["FRIENDLY_TURRET_LOST"] 
        GAME_ENDED_IN_EARLY_SURRENDER= player["GAME_ENDED_IN_EARLY_SURRENDER"] 
        GAME_ENDED_IN_SURRENDER= player["GAME_ENDED_IN_SURRENDER"] 
        GOLD_EARNED= player["GOLD_EARNED"] 
        GOLD_SPENT= player["GOLD_SPENT"] 
        HQ_KILLED= player["HQ_KILLED"] 
        HQ_TAKEDOWNS= player["HQ_TAKEDOWNS"] 
        ID= player["ID"]
        INDIVIDUAL_POSITION = player["INDIVIDUAL_POSITION"]
        ITEM0= player["ITEM0"] 
        ITEM1= player["ITEM1"] 
        ITEM2= player["ITEM2"] 
        ITEM3= player["ITEM3"] 
        ITEM4= player["ITEM4"] 
        ITEM5= player["ITEM5"] 
        ITEM6= player["ITEM6"] 
        ITEMS_PURCHASED= player["ITEMS_PURCHASED"] 
        KEYSTONE_ID= player["KEYSTONE_ID"] 
        KILLING_SPREES= player["KILLING_SPREES"] 
        LARGEST_CRITICAL_STRIKE= player["LARGEST_CRITICAL_STRIKE"] 
        LARGEST_KILLING_SPREE= player["LARGEST_KILLING_SPREE"] 
        LARGEST_MULTI_KILL= player["LARGEST_MULTI_KILL"] 
        LEVEL= player["LEVEL"] 
        LONGEST_TIME_SPENT_LIVING= player["LONGEST_TIME_SPENT_LIVING"] 
        MAGIC_DAMAGE_DEALT_PLAYER= player["MAGIC_DAMAGE_DEALT_PLAYER"] 
        MAGIC_DAMAGE_DEALT_TO_CHAMPIONS= player["MAGIC_DAMAGE_DEALT_TO_CHAMPIONS"] 
        MAGIC_DAMAGE_TAKEN= player["MAGIC_DAMAGE_TAKEN"] 
        MINIONS_KILLED= player["MINIONS_KILLED"] 
        NAME= player["NAME"] 
        NEUTRAL_MINIONS_KILLED= player["NEUTRAL_MINIONS_KILLED"] 
        NEUTRAL_MINIONS_KILLED_ENEMY_JUNGLE= player["NEUTRAL_MINIONS_KILLED_ENEMY_JUNGLE"] 
        NEUTRAL_MINIONS_KILLED_YOUR_JUNGLE= player["NEUTRAL_MINIONS_KILLED_YOUR_JUNGLE"] 
        NUM_DEATHS= player["NUM_DEATHS"] 
        OBJECTIVES_STOLEN= player["OBJECTIVES_STOLEN"] 
        OBJECTIVES_STOLEN_ASSISTS= player["OBJECTIVES_STOLEN_ASSISTS"] 
        PENTA_KILLS= player["PENTA_KILLS"] 
        PERK_PRIMARY_STYLE= player["PERK_PRIMARY_STYLE"] 
        PERK_SUB_STYLE= player["PERK_SUB_STYLE"] 
        PHYSICAL_DAMAGE_DEALT_PLAYER= player["PHYSICAL_DAMAGE_DEALT_PLAYER"] 
        PHYSICAL_DAMAGE_DEALT_TO_CHAMPIONS= player["PHYSICAL_DAMAGE_DEALT_TO_CHAMPIONS"] 
        PHYSICAL_DAMAGE_TAKEN= player["PHYSICAL_DAMAGE_TAKEN"] 
        PING= player["PING"] 
        PLAYER_POSITION= player["PLAYER_POSITION"] 
        QUADRA_KILLS= player["QUADRA_KILLS"] 
        SIGHT_WARDS_BOUGHT_IN_GAME= player["SIGHT_WARDS_BOUGHT_IN_GAME"] 
        SKIN= player["SKIN"] 
        SPELL1_CAST= player["SPELL1_CAST"] 
        SPELL2_CAST= player["SPELL2_CAST"] 
        SPELL3_CAST= player["SPELL3_CAST"] 
        SPELL4_CAST= player["SPELL4_CAST"] 
        STAT_PERK_0= player["STAT_PERK_0"] 
        STAT_PERK_1= player["STAT_PERK_1"] 
        STAT_PERK_2= player["STAT_PERK_2"] 
        SUMMON_SPELL1_CAST= player["SUMMON_SPELL1_CAST"] 
        SUMMON_SPELL2_CAST= player["SUMMON_SPELL2_CAST"] 
        TEAM= player["TEAM"] 
        TEAM_EARLY_SURRENDERED= player["TEAM_EARLY_SURRENDERED"] 
        TEAM_OBJECTIVE= player["TEAM_OBJECTIVE"] 
        TEAM_POSITION= player["TEAM_POSITION"] 
        TIME_CCING_OTHERS= player["TIME_CCING_OTHERS"] 
        TIME_PLAYED= player["TIME_PLAYED"] 
        TOTAL_DAMAGE_DEALT= player["TOTAL_DAMAGE_DEALT"] 
        TOTAL_DAMAGE_DEALT_TO_BUILDINGS= player["TOTAL_DAMAGE_DEALT_TO_BUILDINGS"] 
        TOTAL_DAMAGE_DEALT_TO_CHAMPIONS= player["TOTAL_DAMAGE_DEALT_TO_CHAMPIONS"] 
        TOTAL_DAMAGE_DEALT_TO_OBJECTIVES= player["TOTAL_DAMAGE_DEALT_TO_OBJECTIVES"] 
        TOTAL_DAMAGE_DEALT_TO_TURRETS= player["TOTAL_DAMAGE_DEALT_TO_TURRETS"] 
        TOTAL_DAMAGE_SELF_MITIGATED= player["TOTAL_DAMAGE_SELF_MITIGATED"] 
        TOTAL_DAMAGE_SHIELDED_ON_TEAMMATES= player["TOTAL_DAMAGE_SHIELDED_ON_TEAMMATES"] 
        TOTAL_DAMAGE_TAKEN= player["TOTAL_DAMAGE_TAKEN"] 
        TOTAL_HEAL= player["TOTAL_HEAL"] 
        TOTAL_HEAL_ON_TEAMMATES= player["TOTAL_HEAL_ON_TEAMMATES"] 
        TOTAL_TIME_CROWD_CONTROL_DEALT= player["TOTAL_TIME_CROWD_CONTROL_DEALT"] 
        TOTAL_TIME_SPENT_DEAD= player["TOTAL_TIME_SPENT_DEAD"] 
        TOTAL_UNITS_HEALED= player["TOTAL_UNITS_HEALED"] 
        TRIPLE_KILLS= player["TRIPLE_KILLS"] 
        TRUE_DAMAGE_DEALT_PLAYER= player["TRUE_DAMAGE_DEALT_PLAYER"] 
        TRUE_DAMAGE_DEALT_TO_CHAMPIONS= player["TRUE_DAMAGE_DEALT_TO_CHAMPIONS"] 
        TRUE_DAMAGE_TAKEN= player["TRUE_DAMAGE_TAKEN"] 
        TURRETS_KILLED= player["TURRETS_KILLED"] 
        TURRET_TAKEDOWNS= player["TURRET_TAKEDOWNS"] 
        UNREAL_KILLS= player["UNREAL_KILLS"] 
        VICTORY_POINT_TOTAL= player["VICTORY_POINT_TOTAL"] 
        VISION_SCORE= player["VISION_SCORE"] 
        VISION_WARDS_BOUGHT_IN_GAME= player["VISION_WARDS_BOUGHT_IN_GAME"] 
        WARD_KILLED= player["WARD_KILLED"] 
        WARD_PLACED= player["WARD_PLACED"] 
        WARD_PLACED_DETECTOR= player["WARD_PLACED_DETECTOR"] 
        WAS_EARLY_SURRENDER_ACCOMPLICE= player["WAS_EARLY_SURRENDER_ACCOMPLICE"] 
        WIN= player["WIN"] 


        test = f"""{ASSISTS}"""
        test = test.replace(")","").replace("(","").replace("\'","").replace(",","")
        cur.execute(f"""INSERT INTO UpdatedplayerGame VALUES(
            "{GAME_ID}",
            "{test}",
            "{BARON_KILLS}",
            {BARRACKS_KILLED},
            {BARRACKS_TAKEDOWNS},
            {BOUNTY_LEVEL},
            {CHAMPIONS_KILLED},
            {CHAMPION_TRANSFORM},
            {CONSUMABLES_PURCHASED},
            {DOUBLE_KILLS},
            {DRAGON_KILLS},
            {EXP},
            {FRIENDLY_DAMPEN_LOST},
            {FRIENDLY_HQ_LOST},
            {FRIENDLY_TURRET_LOST},
            {GAME_ENDED_IN_EARLY_SURRENDER},
            {GAME_ENDED_IN_SURRENDER},
            {GOLD_EARNED},
            {GOLD_SPENT},
            {HQ_KILLED},
            {HQ_TAKEDOWNS},
            {ID},
            "{INDIVIDUAL_POSITION}",
            {ITEM0},
            {ITEM1},
            {ITEM2},
            {ITEM3},
            {ITEM4},
            {ITEM5},
            {ITEM6},
            {ITEMS_PURCHASED},
            {KEYSTONE_ID},
            {KILLING_SPREES},
            {LARGEST_CRITICAL_STRIKE},
            {LARGEST_KILLING_SPREE},
            {LARGEST_MULTI_KILL},
            {LEVEL},
            {LONGEST_TIME_SPENT_LIVING},
            {MAGIC_DAMAGE_DEALT_PLAYER},
            {MAGIC_DAMAGE_DEALT_TO_CHAMPIONS},
            {MAGIC_DAMAGE_TAKEN},
            {MINIONS_KILLED},
            "{NAME}",
            {NEUTRAL_MINIONS_KILLED},
            {NEUTRAL_MINIONS_KILLED_ENEMY_JUNGLE},
            {NEUTRAL_MINIONS_KILLED_YOUR_JUNGLE},
            {NUM_DEATHS},
            {OBJECTIVES_STOLEN},
            {OBJECTIVES_STOLEN_ASSISTS},
            {PENTA_KILLS},
            {PERK_PRIMARY_STYLE},
            {PERK_SUB_STYLE},
            {PHYSICAL_DAMAGE_DEALT_PLAYER},
            {PHYSICAL_DAMAGE_DEALT_TO_CHAMPIONS},
            {PHYSICAL_DAMAGE_TAKEN},
            {PING},
            {PLAYER_POSITION},
            {QUADRA_KILLS},
            {SIGHT_WARDS_BOUGHT_IN_GAME},
            "{SKIN}",
            {SPELL1_CAST},
            {SPELL2_CAST},
            {SPELL3_CAST},
            {SPELL4_CAST},
            {STAT_PERK_0},
            {STAT_PERK_1},
            {STAT_PERK_2},
            {SUMMON_SPELL1_CAST},
            {SUMMON_SPELL2_CAST},
            {TEAM},
            {TEAM_EARLY_SURRENDERED},
            {TEAM_OBJECTIVE},
            "{TEAM_POSITION}",
            {TIME_CCING_OTHERS},
            {TIME_PLAYED},
            {TOTAL_DAMAGE_DEALT},
            {TOTAL_DAMAGE_DEALT_TO_BUILDINGS},
            {TOTAL_DAMAGE_DEALT_TO_CHAMPIONS},
            {TOTAL_DAMAGE_DEALT_TO_OBJECTIVES},
            {TOTAL_DAMAGE_DEALT_TO_TURRETS},
            {TOTAL_DAMAGE_SELF_MITIGATED},
            {TOTAL_DAMAGE_SHIELDED_ON_TEAMMATES},
            {TOTAL_DAMAGE_TAKEN},
            {TOTAL_HEAL},
            {TOTAL_HEAL_ON_TEAMMATES},
            {TOTAL_TIME_CROWD_CONTROL_DEALT},
            {TOTAL_TIME_SPENT_DEAD},
            {TOTAL_UNITS_HEALED},
            {TRIPLE_KILLS},
            {TRUE_DAMAGE_DEALT_PLAYER},
            {TRUE_DAMAGE_DEALT_TO_CHAMPIONS},
            {TRUE_DAMAGE_TAKEN},
            {TURRETS_KILLED},
            {TURRET_TAKEDOWNS},
            {UNREAL_KILLS},
            {VICTORY_POINT_TOTAL},
            {VISION_SCORE},
            {VISION_WARDS_BOUGHT_IN_GAME},
            {WARD_KILLED},
            {WARD_PLACED},
            {WARD_PLACED_DETECTOR},
            {WAS_EARLY_SURRENDER_ACCOMPLICE},
            "{WIN}"
            )""")

def uploadrofl(Name):
    global fileName
    fileName = Name
    global root_dir
    BASE_PATH = os.path.dirname(__file__)
    root_dir = os.path.join(BASE_PATH, 'static\\rofl\\')
    counts = {}
    con = sqlite3.connect("./instance/auction_alchemy.db")
    cur = con.cursor()
    files = [root_dir+fileName]
    cur.execute("BEGIN;")
    for fname in files:
        game_id = os.path.basename(fname).split(".")[0].split("-")[1]
        org, metadata = get_metadata(fname)
        insert_game(cur, org, metadata, game_id)
    cur.execute("COMMIT;")
    con.close()

""" if __name__ == "__main__":
    # root_dir = "D:\\LoL Replays\\11.21\\Replays\\"
    root_dir = "C:\\Users\\Alex\\Desktop\\IAB207\\rofl\\"
    fileName = "OC1-540339643.rofl"
    counts = {}

    i = 0
    total = len(os.listdir(root_dir))

    con = sqlite3.connect("./instance/auction_alchemy.db")
    cur = con.cursor()
    files = [root_dir+fileName]
    cur.execute("BEGIN;")
    
    #    game_id = os.path.basename(fname).split(".")[0].split("-")[1]
    #    org, metadata = get_metadata(fname)
    #    insert_game(cur, org, metadata, game_id)
    #    print(i)
    #    i+= 1
    for fname in files:
        game_id = os.path.basename(fname).split(".")[0].split("-")[1]
        org, metadata = get_metadata(fname)
        insert_game(cur, org, metadata, game_id)
    cur.execute("COMMIT;")
    con.close()
    print(counts) """