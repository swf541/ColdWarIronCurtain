from codecs import open
from os import listdir
import os

#region rules
FOCUS_FILTER_POLITICAL = ['add_political_power', 'create_country_leader', 'create_faction', 'can_create_factions', 'add_relation_modifier', 'start_civil_war', 'set_politics']
FOCUS_FILTER_RESEARCH = ['add_tech_bonus', 'modify_tech_sharing_bonus', 'add_research_slot', 'add_to_tech_sharing_group', 'set_technology']
FOCUS_FILTER_INDUSTRY = ['add_building_construction', 'add_extra_state_shared_building_slots', 'free_building_slots', 'add_offsite_building', 'add_resource', 'modify_building_resources']
FOCUS_FILTER_STABILITY = ['add_stability']
FOCUS_FILTER_WAR_SUPPORT = ['add_war_support']
FOCUS_FILTER_MANPOWER = ['create_unit', 'add_manpower', 'load_oob']
FOCUS_FILTER_ANNEXATION = ['create_wargoal', 'add_state_core', 'add_state_claim', 'add_core_of', 'declare_war_on', 'annex_country']
FOCUS_FILTER_TFV_AUTONOMY = ['set_autonomy', 'add_autonomy_ratio']
FOCUS_FILTER_ARMY_BONUS = ['army_experience']
FOCUS_FILTER_NAVY_BONUS = ['navy_experience']
FOCUS_FILTER_AIRFORCE_BONUS = ['air_experience', 'add_ace']
FOCUS_FILTER_RESISTANCE = []

FOCUS_FILTER_POLITICAL_idea = ['trade_laws_cost_factor', 'navy_chief_cost_factor', 'air_chief_cost_factor', 'mobilization_laws_cost_factor', 'master_ideology_drift', 'economy_cost_factor', 'neutrality_drift', 'military_leader_cost_factor', 'army_chief_cost_factor', 'high_command_cost_factor', 'theorist_cost_factor', 'political_advisor_cost_factor', 'join_faction_tension', 'lend_lease_tension', 'guarantee_tension', 'fascism_drift', 'democratic_drift','legitimacy_daily', 'targeted_legitimacy_daily', 'political_power_gain', 'political_power_factor', 'political_power_cost', 'communism_drift', 'drift_defence_factor']
FOCUS_FILTER_RESEARCH_idea = ['research_speed_factor', 'research_bonus']
FOCUS_FILTER_INDUSTRY_idea = ['industry_air_damage_factor', 'production_speed_radar_station_factor', 'production_speed_anti_air_building_factor', 'production_speed_air_base_factor', 'production_speed_bunker_factor', 'industry_repair_factor', 'industry_free_repair_factor', 'production_speed_dockyard_factor', 'conversion_cost_mil_to_civ_factor', 'production_speed_synthetic_refinery_factor', 'max_fuel_factor', 'production_speed_infrastructure_factor', 'production_speed_industrial_complex_factor', 'fuel_gain_factor', 'production_speed_arms_factory_factor', 'production_speed', 'production_factory_max_efficiency_factor', 'line_change_production_efficiency_factor', 'production_speed_buildings_factor', 'conversion_cost_civ_to_mil_factor', 'industrial_capacity_factory', 'industrial_capacity_dockyard', 'consumer_goods_factor', 'production_factory_efficiency_gain_factor', 'production_factory_start_efficiency_factor', 'local_building_slots_factor', 'local_resources_factor', 'production_oil_factor', 'global_building_slots_factor']
FOCUS_FILTER_STABILITY_idea = ['stability_factor', 'stability_weekly', 'offensive_war_stability_factor', 'defensive_war_stability_factor']
FOCUS_FILTER_WAR_SUPPORT_idea = ['war_support_factor', 'war_support_weekly']
FOCUS_FILTER_MANPOWER_idea = ['weekly_manpower', 'conscription_factor', 'conscription', 'non_core_manpower', 'MONTHLY_POPULATION', 'monthly_population']
FOCUS_FILTER_ANNEXATION_idea = ['justify_war_goal_time', 'send_volunteer_size', 'send_volunteers_tension', 'surrender_limit', 'generate_wargoal_tension', 'enemy_justify_war_goal_time']
FOCUS_FILTER_TFV_AUTONOMY_idea = ['autonomy_gain', 'subjects_autonomy_gain']
FOCUS_FILTER_ARMY_BONUS_idea = ['special_forces_training_time_factor', 'command_power_gain', 'max_command_power', 'command_power_gain_mult', 'defense_bonus_against', 'attack_bonus_against', 'army_leader_start_level', 'modifier_army_sub_unit_infiltrator_company_defence_factor', 'mobilization_speed', 'special_forces_cap', 'modifier_army_sub_unit_infiltrator_company_attack_factor', 'army_core_attack_factor', 'army_core_defence_factor', 'training_time_army_factor', 'training_time_factor', 'planning_speed', 'max_planning', 'army_org_factor', 'army_org', 'recon_factor', 'army_morale_factor', 'amphibious_invasion', 'invasion_preparation', 'land_reinforce_rate', 'defence', 'offence', 'army_defence_factor', 'army_attack_factor', 'army_speed_factor', 'attrition', 'heat_attrition_factor', 'winter_attrition_factor', 'acclimatization_cold_climate_gain_factor', 'acclimatization_hot_climate_gain_factor', 'terrain_penalty_reduction', 'max_dig_in', 'dig_in_speed', 'dig_in_speed_factor', 'supply_consumption_factor', 'out_of_supply_factor', 'experience_gain_army', 'experience_gain_army_factor', 'experience_loss_factor', 'minimum_training_level', 'no_supply_grace', 'army_armor_speed_factor', 'army_armor_attack_factor', 'army_armor_defence_factor', 'army_artillery_attack_factor', 'army_artillery_defence_factor', 'army_infantry_attack_factor', 'army_infantry_defence_factor', 'special_forces_attack_factor', 'special_forces_defence_factor', 'cavalry_attack_factor', 'cavalry_defence_factor', 'mechanized_attack_factor', 'mechanized_defence_factor', 'motorized_attack_factor', 'motorized_defence_factor', 'air_paradrop_attack_factor', 'air_paradrop_defence_factor', 'air_paradrop_agility_factor']
FOCUS_FILTER_NAVY_BONUS_idea = ['naval_torpedo_screen_penetration_factor', 'navy_carrier_air_attack_factor', 'navy_carrier_air_targetting_factor', 'navy_carrier_air_agility_factor', 'navy_capital_ship_attack_factor', 'navy_capital_ship_defence_factor', 'navy_submarine_attack_factor', 'navy_submarine_defence_factor', 'navy_screen_attack_factor', 'navy_screen_defence_factor', 'naval_torpedo_range_factor', 'convoy_escort_efficiency', 'naval_retreat_chance', 'naval_retreat_speed', 'ships_at_battle_start', 'spotting_chance', 'navy_anti_air_attack_factor', 'sortie_efficiency', 'naval_hit_chance', 'naval_coordination', 'convoy_raiding_efficiency_factor', 'naval_speed_factor', 'navy_submarine_detection_factor', 'navy_max_range_factor', 'experience_gain_navy', 'experience_gain_navy_factor']
FOCUS_FILTER_AIRFORCE_BONUS_idea = ['air_defence_factor', 'air_bombing_targetting', 'air_attack_factor', 'air_ace_generation_chance_factor', 'enemy_army_bonus_air_superiority_factor', 'air_accidents_factor', 'air_night_penalty', 'air_weather_penalty', 'air_range_factor', 'experience_gain_air', 'experience_gain_air_factor', 'naval_strike_attack_factor', 'naval_strike_targetting_factor', 'naval_strike_agility_factor', 'air_interception_attack_factor', 'air_interception_defence_factor', 'air_interception_agility_factor', 'air_air_superiority_attack_factor', 'air_air_superiority_defence_factor', 'air_air_superiority_agility_factor', 'air_close_air_support_attack_factor', 'air_close_air_support_defence_factor', 'air_close_air_support_agility_factor', 'air_strategic_bomber_attack_factor', 'air_strategic_bomber_defence_factor', 'air_strategic_bomber_agility_factor', 'air_strategic_bomber_bombing_factor', 'air_cas_present_factor']
FOCUS_FILTER_RESISTANCE_idea = ['resistance_growth_on_our_occupied_states', 'resistance_damage_to_garrison', 'foreign_subversive_activites']

filter_list = [FOCUS_FILTER_POLITICAL, FOCUS_FILTER_RESEARCH, FOCUS_FILTER_INDUSTRY, FOCUS_FILTER_STABILITY, FOCUS_FILTER_WAR_SUPPORT, FOCUS_FILTER_MANPOWER, FOCUS_FILTER_ANNEXATION, FOCUS_FILTER_TFV_AUTONOMY, FOCUS_FILTER_ARMY_BONUS, FOCUS_FILTER_NAVY_BONUS, FOCUS_FILTER_AIRFORCE_BONUS, FOCUS_FILTER_RESISTANCE, FOCUS_FILTER_POLITICAL_idea, FOCUS_FILTER_RESEARCH_idea, FOCUS_FILTER_INDUSTRY_idea, FOCUS_FILTER_STABILITY_idea, FOCUS_FILTER_WAR_SUPPORT_idea, FOCUS_FILTER_MANPOWER_idea, FOCUS_FILTER_ANNEXATION_idea, FOCUS_FILTER_TFV_AUTONOMY_idea, FOCUS_FILTER_ARMY_BONUS_idea, FOCUS_FILTER_NAVY_BONUS_idea, FOCUS_FILTER_AIRFORCE_BONUS_idea, FOCUS_FILTER_RESISTANCE_idea]
filter_list_keyword = ["FOCUS_FILTER_POLITICAL", "FOCUS_FILTER_RESEARCH", "FOCUS_FILTER_INDUSTRY", "FOCUS_FILTER_STABILITY", "FOCUS_FILTER_WAR_SUPPORT", "FOCUS_FILTER_MANPOWER", "FOCUS_FILTER_ANNEXATION", "FOCUS_FILTER_TFV_AUTONOMY", "FOCUS_FILTER_ARMY_BONUS", "FOCUS_FILTER_NAVY_BONUS", "FOCUS_FILTER_AIRFORCE_BONUS", "FOCUS_FILTER_RESISTANCE","FOCUS_FILTER_POLITICAL", "FOCUS_FILTER_RESEARCH", "FOCUS_FILTER_INDUSTRY", "FOCUS_FILTER_STABILITY", "FOCUS_FILTER_WAR_SUPPORT", "FOCUS_FILTER_MANPOWER", "FOCUS_FILTER_ANNEXATION", "FOCUS_FILTER_TFV_AUTONOMY", "FOCUS_FILTER_ARMY_BONUS", "FOCUS_FILTER_NAVY_BONUS", "FOCUS_FILTER_AIRFORCE_BONUS", "FOCUS_FILTER_RESISTANCE"]


def get_keywords(effect):
    for number, check in enumerate(filter_list):
        if effect in check:
            return filter_list_keyword[number]


""""
FOCUS_FILTER_POLITICAL
FOCUS_FILTER_RESEARCH
FOCUS_FILTER_INDUSTRY
FOCUS_FILTER_STABILITY
FOCUS_FILTER_WAR_SUPPORT
FOCUS_FILTER_MANPOWER
FOCUS_FILTER_ANNEXATION
FOCUS_FILTER_TFV_AUTONOMY

custom
FOCUS_FILTER_ARMY_BONUS
FOCUS_FILTER_NAVY_BONUS
FOCUS_FILTER_AIRFORCE_BONUS

search_filters = {XXX XXX XX}
"""

eaw_folder = r'C:\Users\Martijn\Documents\Paradox Interactive\Hearts of Iron IV\mod\equestria_dev'

idea_markers = dict()

for filename in listdir(os.path.join(eaw_folder, "common", "ideas")):
    with open(os.path.join(eaw_folder, "common", "ideas", filename), 'r', 'utf-8') as file:
        lines = file.readlines()

    level = 0
    current_keywords = set()
    check_shit = False
    idea = ""

    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            continue
        if '#' in line:
            line = line.split('#')[0]

        if level == 2 and '{' in line:
            idea = line.split("=")[0].strip()

        if level == 3 and "modifier" in line:
            check_shit = True

        #if check_shit and "}" in line and level == 3:
        #    check_shit = False

        if check_shit:
            if (result := get_keywords(line.split("=")[0].strip())) is not None:
                current_keywords.add(result)

        if level == 3 and "}" in line and ("modifier" in line or "{" not in line):
            check_shit = False
            idea_markers[idea] = current_keywords
            #print(idea, current_keywords)
            current_keywords = set()

        if '{' in line:
            level += line.count('{')
        if '}' in line:
            level -= line.count('}')


for filename in listdir(os.path.join(eaw_folder, "common", "national_focus")):
    file = open(os.path.join(eaw_folder, "common", "national_focus", filename), 'r', 'utf-8')
    lines = file.readlines()
    file.close()
    file = open(os.path.join(eaw_folder, "common", "national_focus", filename), 'w', 'utf-8')
    file.truncate(0)

    check_shit = False
    current_keywords = set()
    level = 0
    exit_level = -1
    focus_name = ""
    find_ideas = False


    for line in lines:
        orig_line = line[:]
        line = line.strip()
        if line.startswith('#'):
            file.write(orig_line)
            continue
        if '#' in line:
            line = line.split('#')[0]

        if (level == 1 or level == 2) and line.startswith('id'):
            focus_name = line.split('=')[1].strip()

        if 'completion_reward' in line:
            check_shit = True
            exit_level = level + 1

        if (check_shit and '=' in line) or find_ideas:
            arg = [_.strip() for _  in line.split("=")]

            if find_ideas:
                arg.append(arg[0])
            if arg[0].startswith('add_idea'):
                if arg[1] == '{':
                    find_ideas = True
                else:
                    current_keywords.update(idea_markers[arg[1]])
            if (result := get_keywords(arg[0])) is not None:
                current_keywords.add(result)

        if find_ideas and '}' in line:
            find_ideas = False

        file.write(orig_line)

        if check_shit and '}' in line and level == exit_level and line.count('{') - line.count('}') < 0:
            check_shit = False
            #print(filename, focus_name, current_keywords)
            if len(current_keywords) > 0:
                whitespace = orig_line[:-len(orig_line.lstrip())]
                file.write(whitespace + "search_filters = { " + " ".join([str(i) for i in list(current_keywords)]) + " }\n")
                current_keywords = set()

        if '{' in line:
            level += line.count('{')
        if '}' in line:
            level -= line.count('}')

