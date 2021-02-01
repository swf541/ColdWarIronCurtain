from codecs import open
from os import listdir
import os


army = ['army_chief_morale_3', 'army_chief_drill_1', 'rarity_the_designer', 'imperial_connections', 'army_chief_old_guard', 'army_chief_planning_3', 'army_cavalry_3', 'experimental_genius', 'armaments_organizer', 'uniform_designer', 'quartermaster_general', 'army_chief_organizational_1', 'special_forces_commander', 'revolutionary_intellectual', 'wartime_innovator', 'military_bishop' , 'olenian_seer', 'army_chief_reform_2', 'army_chief_planning_2', 'army_chief_drill_2', 'industry_theorist', 'royal_magician', 'army_commando_1', 'blitzkrieg_theorist', 'jungle_warfare_expert', 'state_investor', 'bookworm', 'research_center', 'mass_assault_expert', 'defence_theorist', 'local_magician', 'superior_firepower_expert', 'pie_artillery', '', 'army_entrenchment_2', 'army_concealment_3', 'army_entrenchment_3', 'army_chief_defensive_2', 'army_entrenchment_3', 'army_cavalry_2', '', 'army_commando_2', 'army_concealment_2', 'army_commando_3', 'army_logistics_1', 'army_armored_2', 'army_commando_2', 'army_infantry_3','army_chief_maneuver_2', 'army_chief_morale_2', 'army_regrouping_1', 'army_cavalry_1', 'mobile_warfare_expert', 'grand_battle_plan_expert', 'army_logistics_3', 'army_chief_maneuver_1', 'army_regrouping_2', 'army_armored_1', 'army_logistics_2', 'army_chief_planning_1', 'nuclear_scientist', 'military_theorist', 'army_infantry_1', 'army_infantry_2','army_artillery_1', 'army_artillery_2', 'YAL_military_theorist_better', 'army_regrouping_3']
navy = ['navy_screen_2', 'navy_anti_submarine_2', 'naval_aviation_pioneer', 'navy_fleet_logistics_2', 'navy_carrier_2', 'navy_submarine_3', 'navy_chief_maneuver_1', 'naval_theorist', 'grand_fleet_proponent', 'navy_naval_air_defense_1', 'navy_capital_ship_2', 'navy_anti_submarine_1', 'navy_fleet_logistics_1']
air = ['air_air_superiority_3', 'air_air_combat_training_1', 'air_combat_academy', 'air_bomber_interception_1', 'air_chief_all_weather_1', 'air_naval_strike_2', 'air_chief_ground_support_3', 'air_close_air_support_3', 'air_chief_reform_2', 'air_tactical_bombing_3', 'air_air_superiority_2', 'air_airborne_3', 'air_airborne_2', 'air_chief_ground_support_1', 'dive_bomber', 'close_air_support_proponent', 'rocket_scientist', 'air_chief_safety_1', 'air_warfare_theorist', 'air_air_combat_training_2', 'assault_avaition', 'air_bomber_interception_2', 'air_tactical_bombing_2', 'air_air_superiority_1', 'air_close_air_support_1']
filter_list = [army, navy, air]
filter_list_keyword = ["army", "navy", "air"]

def get_keywords(effect):
    for number, check in enumerate(filter_list):
        if effect in check:
            return filter_list_keyword[number]

eaw_folder = r'C:\Users\Martijn\Documents\Paradox Interactive\Hearts of Iron IV\mod\equestria_dev'



for filename in listdir(os.path.join(eaw_folder, "common", "ideas")):
    file = open(os.path.join(eaw_folder, "common", "ideas", filename), 'r', 'utf-8')
    lines = file.readlines()
    file.close()
    file = open(os.path.join(eaw_folder, "common", "ideas", filename), 'w', 'utf-8')
    file.truncate(0)

    level = 0
    target = False
    advisor = ""
    trait = ""
    buffer = []
    fill_buffer = False

    for lineno, line in enumerate(lines):
        orig_line = line[:]
        line = line.strip()
        if line.startswith('#') or line == "":
            if fill_buffer:
                buffer.append(orig_line)
            else:
                file.write(orig_line)
            continue
        if '#' in line:
            line = line.split('#')[0]

        if level == 1 and ('theorist' in line or 'high_command' in line):
            target = True

        if level == 2 and '}' in line and line.count('{') - line.count('}') != 0:
            target = False

        if level == 2 and target:
            advisor = line.split("=")[0].strip()
            fill_buffer = True

        if line.startswith('trait') and target:
            if "}" in line:
                trait = line.split("{")[1].split("}")[0].strip()
            else:
                trait = lines[lineno+1].strip()

            buffer.insert(1, "\t\t\tledger = " + get_keywords(trait) + "\r\n")
            file.write("".join(buffer))
            fill_buffer = False
            buffer = []

        if '{' in line:
            level += line.count('{')
        if '}' in line:
            level -= line.count('}')

        if fill_buffer:
            buffer.append(orig_line)
        else:
            file.write(orig_line)

    if buffer != []:
        file.write("".join(buffer))