NDefines.NAI.DEPLOY_MIN_EQUIPMENT_WAR_FACTOR = 0.75 -- Required percentage of equipment (1.0 = 100%) for AI to deploy unit in wartime
NDefines.NAI.DIPLO_PREFER_OTHER_FACTION = -125 -- The country has yet to ask some other faction it would prefer to be a part of.
NDefines.NAI.DIPLOMACY_CREATE_FACTION_FACTOR = 0.0 -- Factor for AI desire to create a new faction. Val < 1.0 makes it less likely to create than to join.
NDefines.NAI.DIPLOMACY_FACTION_GLOBAL_TENSION_FACTOR = 0.0 -- How much the AI takes global tension into account when considering faction actions
NDefines.NAI.DIPLOMACY_FACTION_SAME_IDEOLOGY_MAJOR = 0 -- AI bonus acceptance when being asked about faction is a major of the same ideology
NDefines.NAI.DIPLOMACY_FACTION_WRONG_IDEOLOGY_PENALTY = 0 -- AI penalty for diplomatic faction acitons between nations of different ideologies
NDefines.NAI.DIPLOMATIC_ACTION_BREAK_SCORE = -10 -- AI must score a diplomatic action less than this to break it off
NDefines.NAI.RESEARCH_AHEAD_OF_TIME_FACTOR = 10.0 -- To which extent AI should care about ahead of time penalties to research
NDefines.NAI.RESEARCH_AIR_DOCTRINE_NEED_GAIN_FACTOR = 0.08 -- Multiplies value based on relative number of air base / country size.
NDefines.NAI.RESEARCH_BONUS_FACTOR = 1.5 -- To which extent AI should care about bonuses to research
NDefines.NAI.RESEARCH_LAND_DOCTRINE_NEED_GAIN_FACTOR = 0.1 -- Multiplies value based on relative military industry size / country size.
NDefines.NAI.RESEARCH_NAVAL_DOCTRINE_NEED_GAIN_FACTOR = 0.075 -- Multiplies value based on relative naval industry size / country size.
NDefines.NAI.AIR_WING_REINFORCEMENT_LIMIT = 60

NDefines.NAir.AIR_WING_FLIGHT_SPEED_MULT = 0.02					-- Global speed multiplier for airplanes (affects fe.transferring to another base)
NDefines.NAir.AIR_WING_MAX_STATS_ATTACK = 1000					-- Max stats
NDefines.NAir.AIR_WING_MAX_STATS_DEFENCE = 1000
NDefines.NAir.AIR_WING_MAX_STATS_AGILITY = 1000
NDefines.NAir.AIR_WING_MAX_STATS_SPEED = 10000
NDefines.NAir.AIR_WING_MAX_STATS_BOMBING = 1000
NDefines.NAir.AIR_WING_MAX_SIZE = 1000 							-- Max amount of airplanes in wing
NDefines.NAir.AIR_WING_BOMB_DAMAGE_FACTOR = 2					-- Used to balance the damage done while bombing.
NDefines.NAir.COMBAT_STAT_IMPORTANCE_SPEED = 2 				-- How important is speed when comparing stats.
NDefines.NAir.COMBAT_STAT_IMPORTANCE_AGILITY = 1				-- How important is agility when comparing stats.
NDefines.NAir.BIGGEST_AGILITY_FACTOR_DIFF = 2.5					-- biggest factor difference in agility for doing damage (caps to this)
NDefines.NAir.COMBAT_DAMAGE_STATS_MULTILIER = 0.3
NDefines.NAir.COMBAT_BETTER_AGILITY_DAMAGE_REDUCTION = 0.6 		-- How much the better agility (then opponent's) can reduce their damage to us.
NDefines.NAir.COMBAT_MAX_WINGS_AT_ONCE = 10000						-- Max amount of air wings in one combat simulation. The higher value, the quicker countries may loose their wings. It's a gameplay balance value.
NDefines.NAir.COMBAT_MAX_WINGS_AT_GROUND_ATTACK = 10000	        	-- we can really pounce a land strike and escalate
NDefines.NAir.COMBAT_MAX_WINGS_AT_ONCE_PORT_STRIKE = 10000      -- we can really pounce a naval strike and escalate
NDefines.NAir.AIR_REGION_SUPERIORITY_PIXEL_SCALE = 0.04          -- air superiority scale = superiority/(pixels*this)
NDefines.NAir.COMBAT_MULTIPLANE_CAP = 3						-- How many planes can shoot at each plane on other side ( if there are 100 planes we are atttacking COMBAT_MULTIPLANE_CAP * 100 of our planes can shoot )
NDefines.NAir.COMBAT_DAMAGE_SCALE = 0.2						-- Higher value = more shot down planes
NDefines.NAir.CAS_NIGHT_ATTACK_FACTOR = 0.8 -- CAS damaged get multiplied by this in land combats at night
NDefines.NAir.STRATEGIC_BOMBER_NUKE_AIR_SUPERIORITY = 10.0 -- How much air superiority is needed for a tactical bomber to be able to nuke a province
NDefines.NAir.NAVAL_COMBAT_EXTERNAL_PLANES_JOIN_RATIO = 0.02 -- Max planes that can join a combat comparing to the total strength of the ships
NDefines.NAir.COMBAT_STACK_LIMIT = 3 -- The biggest allowed dogfight combination (1vs1 or 2vs1). Bigger value cause that amount of airplanes matters more then their stats. Only used in naval air combat, for land air combat see COMBAT_MULTIPLANE_CAP
NDefines.NAir.NAVAL_STRIKE_DAMAGE_TO_STR = 2 -- Balancing value to convert damage ( naval_strike_attack * hits ) to Strength reduction.
NDefines.NAir.MISSION_COMMAND_POWER_COSTS = {  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 }
NDefines.NAir.MISSION_FUEL_COSTS = {  1.0, 0.5, 0.2, 1.3, 1.3, 20.0, 3.0, 1.0, 1.3, 2.0, 0.5, 2.0, 2.0, 1.0 }
NDefines.NAir.CAS_NIGHT_ATTACK_FACTOR = 0.5 -- Balancing value to convert damage ( naval_strike_attack * hits ) to Strength reduction.
NDefines.NAir.AIR_WING_AVERAGE_SIZE = 50 						-- Eyeballed average amount of airplanes in wing. Used when calculating air volunteer.

NDefines.NBuildings.AIRBASE_CAPACITY_MULT = 50 -- Each level of airbase building multiplied by this, gives capacity (max operational value). Value is int. 1 for each airplane.
NDefines.NBuildings.ANTI_AIR_SUPERIORITY_MULT = 100.0 -- How much air superiority reduction to the enemy does our AA guns? Normally each building level = -1 reduction. With this multiplier.
NDefines.NBuildings.INFRASTRUCTURE_RESOURCE_BONUS= 0.0
NDefines.NBuildings.MAX_BUILDING_LEVELS = 200
NDefines.NBuildings.MAX_SHARED_SLOTS = 42
NDefines.NBuildings.RADAR_RANGE_MAX = 400 -- Range is interpolated between building levels 1-15.
NDefines.NBuildings.SUPPLY_PORT_LEVEL_THROUGHPUT = 5 -- Supply throughput per level of naval base. Vanilla value is 3.
NDefines.NBuildings.SUPPLY_ROUTE_RESOURCE_BONUS = 0.0

NDefines.NCountry.EVENT_PROCESS_OFFSET = 20 -- Events are checked every X day per country or state (1 is ideal, but CPU heavy)
NDefines.NCountry.POLITICAL_POWER_CAP = 2000000.0
NDefines.NCountry.ARMY_SCORE_MULTIPLIER = 2.0 -- Based on number of armies.
NDefines.NCountry.NAVY_SCORE_MULTIPLIER = 25.0 -- Based on number of navies.
NDefines.NCountry.AIR_SCORE_MULTIPLIER = 0.01 -- Based on number of planes (which is typically a lot).
NDefines.NCountry.INDUSTRY_SCORE_MULTIPLIER = 1.0 -- Based on number of factories.
NDefines.NCountry.PROVINCE_SCORE_MULTIPLIER = 0.1 -- Based on number of controlled provinces.
NDefines.NCountry.STATE_VALUE_NON_CORE_STATE_FRACTION = 1
NDefines.NCountry.POPULATION_YEARLY_GROWTH_BASE = 0.008
NDefines.NCountry.MIN_COUP_SUCCESS_STABILITY = -2 -- NO COUPS ALLOWED!!!!
NDefines.NCountry.BASE_FUEL_GAIN_PER_OIL = 4 -- VANILLA 2

NDefines.NCountry.AIR_VOLUNTEER_PLANES_LIMIT = 0.5	-- Ratio for volunteer planes available for sending in relation to sender air force
NDefines.NCountry.AIR_VOLUNTEER_BASES_CAPACITY_LIMIT = 0.5	-- Ratio for volunteer planes available for sending in relation to receiver air base capacity


NDefines.NDiplomacy.BASE_PEACE_TAKE_UNCONTROLLED_STATE_FACTOR = 10.0 -- Base factor for taking state you do not control in %
NDefines.NDiplomacy.CIVIL_WAR_INVOLVEMENT_MIN_TENSION = 0.0 -- base value of world tension to involve other sides to the civil war
NDefines.NDiplomacy.IDEOLOGY_JOIN_FACTION_MIN_LEVEL = 0 -- ideology limit required to join faction
NDefines.NDiplomacy.MAX_OPINION_VALUE = 200 -- Max opinion value cap.
NDefines.NDiplomacy.MIN_OPINION_VALUE = -200
NDefines.NDiplomacy.TENSION_ANNEX_CLAIM = 1.5 -- Amount of tension generated by annexing a state you DO have claims on
NDefines.NDiplomacy.TENSION_ANNEX_CORE = 1 -- Amount of tension generated by annexing a state that is your core
NDefines.NDiplomacy.TENSION_CAPITULATE = 1.0 -- Scale of the amount of tension created by a countries capitulation.
NDefines.NDiplomacy.TENSION_CB_WAR = 5 -- Amount of tension generated by a war with a CB
NDefines.NDiplomacy.TENSION_DECAY = 0.10 -- Each months tension decays this much
NDefines.NDiplomacy.TENSION_GUARANTEE = 0
NDefines.NDiplomacy.TENSION_LIBERATE = 0 -- Amount of tension generated by liberating a country.
NDefines.NDiplomacy.TENSION_NO_CB_WAR = 15 -- Amount of tension generated by a no-CB war
NDefines.NDiplomacy.TENSION_PEACE_FACTOR = 0.0 -- scale of the amount of tension (from war declaration) reduced when peace is completed.
NDefines.NDiplomacy.TENSION_SIZE_FACTOR = 0.25 -- All action tension values are multiplied by this value
NDefines.NDiplomacy.TENSION_STATE_VALUE = 5 -- Tension value gained by annexing one state
NDefines.NDiplomacy.TENSION_TIME_SCALE_MIN = 0.0 -- Timed tension scale won't decrease under this value
NDefines.NDiplomacy.TENSION_TIME_SCALE_MONTHLY_FACTOR = 0.00 -- Timed tension scale will be modified by this amount starting with TENSION_TIME_SCALE_START_DATE
NDefines.NDiplomacy.TENSION_TIME_SCALE_START_DATE = "1999.1.1.12" -- Starting at this date the tension values will be scaled down (will be equal to 1 before that)
NDefines.NDiplomacy.VOLUNTEERS_DIVISIONS_REQUIRED = 1 -- This many divisons are required for the country to be able to send volunteers.
NDefines.NDiplomacy.VOLUNTEERS_PER_COUNTRY_ARMY = 0.05 -- Each army unit owned by the source country contributes this amount of volunteers to the limit.
NDefines.NDiplomacy.VOLUNTEERS_PER_TARGET_PROVINCE = 0.05 -- Each province owned by the target country contributes this amount of volunteers to the limit.

NDefines.NDiplomacy.VOLUNTEERS_TRANSFER_SPEED = 21

NDefines.NGame.END_DATE = "2050.5.23.12"
NDefines.NGame.START_DATE = "1945.5.23.12"

NDefines.NMilitary.MAX_DIVISION_SUPPORT_WIDTH = 2 -- Max width of support in division designer.
NDefines.NMilitary.MAX_DIVISION_SUPPORT_HEIGHT = 5 -- Max width of support in division designer.
NDefines.NMilitary.MAX_ARMY_EXPERIENCE = 5000;
NDefines.NMilitary.MAX_NAVY_EXPERIENCE = 5000;
NDefines.NMilitary.MAX_AIR_EXPERIENCE = 5000;
NDefines.NMilitary.CORPS_COMMANDER_ARMIES_CAP = -1
NDefines.NMilitary.FIELD_MARSHAL_DIVISIONS_CAP = 0
NDefines.NMilitary.BASE_CAPTURE_EQUIPMENT_RATIO = 0.05
NDefines.NMilitary.BASE_DIVISION_BRIGADE_GROUP_COST = 3 	--Base cost to unlock a regiment slot,
NDefines.NMilitary.BASE_DIVISION_BRIGADE_CHANGE_COST = 3	--Base cost to change a regiment column.
NDefines.NMilitary.BASE_DIVISION_SUPPORT_SLOT_COST = 1 	--Base cost to unlock a support slot
NDefines.NMilitary.EXPERIENCE_COMBAT_FACTOR = 0.1 --Combat bonus units get from their experience. Default value is 0.25. Experience per unit level = -x, 0, x, 2x, 3x, level 2 being the "basic" level and always having 0% bonus.

NDefines.NNavy.CARRIER_STACK_PENALTY = 8 -- The most efficient is 4 carriers in combat. 5+ brings the penalty to the amount of wings in battle.
NDefines.NNavy.CARRIER_STACK_PENALTY_EFFECT = 0.1 -- Each carrier above the optimal amount decreases the amount of airplanes being able to takeoff by such %.
NDefines.NNavy.SUBMARINE_HIDE_TIMEOUT = 4 -- Amount of in-game-hours that takes the submarine (with position unrevealed) to hide.
NDefines.NNavy.SUBMARINE_REVEAL_BASE_CHANCE = 0.002 -- Base chance for submarine detection. It's modified by the difference of a spootter's submarines detection vs submarine visibility. Use this variable for game balancing.
NDefines.NNavy.SUBMARINE_REVEALED_TIMEOUT = 8 -- Amount of in-game-hours that makes the submarine visible if it is on the defender side.
NDefines.NNavy.SHORE_BOMBARDMENT_CAP = 0.15 -- Maximum shore bombardment
NDefines.NNavy.LIGHT_GUN_ATTACK_TO_SHORE_BOMBARDMENT = 0.15 --heavy gun attack value is divided by this value * 100 and added to shore bombardment modifier --changed from vanilla (0.05) to reflect gun/missile dichotomy
NDefines.NNavy.HEAVY_GUN_ATTACK_TO_SHORE_BOMBARDMENT = 0.05 -- light gun attack value is divided by this value * 100 and added to shore bombardment modifier --changed from vanilla (0.1) to reflect gun/missile dichotomy
NDefines.NNavy.NAVAL_INVASION_PREPARE_HOURS = 72 -- base hours needed to prepare an invasion
NDefines.NNavy.SEA_AIR_COMBAT_MAX_WINGS_ON_STACK = 75 -- max planes that can enter naval combat
NDefines.NTechnology.BASE_RESEARCH_POINTS_SAVED = 50.0 -- Base amount of research points a country can save per slot.
NDefines.NTechnology.BASE_YEAR_AHEAD_PENALTY_FACTOR = 1 -- Base year ahead penalty
NDefines.NTechnology.MAX_TECH_SHARING_BONUS = 0.15 -- Max technology sharing bonus that can be applied instantly
NDefines.NTechnology.BASE_TECH_COST = 100 -- Multiplied by tech cost, then years ahead penalty

NDefines.NTrade.RELATION_TRADE_FACTOR = 5 -- Trade factor is modified by Opinion value times this

NDefines.NFocus.FOCUS_POINT_DAYS = 5 -- Each point takes a week
NDefines.NFocus.MAX_SAVED_FOCUS_PROGRESS = 15 -- This much progress can be saved while not having a focus selected

NDefines.NGame.LAG_DAYS_FOR_LOWER_SPEED = 100
NDefines.NGame.LAG_DAYS_FOR_PAUSE = 50

NDefines.NAI.DIPLOMACY_SCARED_MINOR_EXTRA_RELUCTANCE = -50 -- extra reluctance to join stuff as scared minor
NDefines.NAI.DIPLOMACY_BOOST_PARTY_COST_FACTOR = 0.0	-- Desire to boost party popularity subtracts the daily cost multiplied by this
NDefines.NAI.DIPLOMACY_IMPROVE_RELATION_COST_FACTOR = 0.0-- Desire to boost relations subtracts the cost multiplied by this
NDefines.NAI.DIPLOMACY_IMPROVE_RELATION_PP_FACTOR = 0.0	-- Desire to boost relations adds total PP multiplied by this
NDefines.NAI.DIVISION_UPGRADE_MIN_XP = 9999999
NDefines.NAI.DIVISION_CREATE_MIN_XP = 9999999
NDefines.NAI.VARIANT_UPGRADE_MIN_XP = 9999999
NDefines.NAI.MAX_AHEAD_RESEARCH_PENALTY = 0
NDefines.NAI.RESEARCH_AHEAD_OF_TIME_FACTOR = 9999999

NDefines.NProduction.MAX_EQUIPMENT_RESOURCES_NEED = 4
NDefines.NProduction.MAX_CIV_FACTORIES_PER_LINE = 10
NDefines.NProduction.BASE_FACTORY_SPEED_NAV = 2.5 -- Double construction time for ships, vanilla 25
NDefines.NProduction.INFRA_MAX_CONSTRUCTION_COST_EFFECT = 0.7
NDefines.NProduction.EQUIPMENT_MODULE_ADD_XP_COST = 2.0
NDefines.NProduction.EQUIPMENT_MODULE_REPLACE_XP_COST = 2.0
NDefines.NProduction.EQUIPMENT_MODULE_CONVERT_XP_COST = 2.0
NDefines.NProduction.EQUIPMENT_MODULE_REMOVE_XP_COST = 2.0

NDefines.NAI.ROCKET_MIN_ASSIGN_SCORE = 0
NDefines.NAI.ROCKET_MIN_PRIO_ASSIGN_SCORE = 0
NDefines.NAI.ROCKET_ASSIGN_SCORE_REDUCTION_PER_ASSIGNMENT = 0
NDefines.NAI.ROCKETSITE_CAPACITY_MULT = 0
NDefines.NAI.NUM_SILOS_PER_CIVILIAN_FACTORIES = 0.2

NDefines.NOperatives.AGENCY_CREATION_DAYS = 200
NDefines.NOperatives.AGENCY_UPGRADE_DAYS = 100
NDefines.NOperatives.AGENCY_OPERATIVE_RECRUITMENT_TIME = 90
NDefines.NOperatives.AGENCY_CREATION_FACTORIES = 15
NDefines.NOperatives.AGENCY_UPGRADE_PER_OPERATIVE_SLOT = 24 -- lol that's all of them
NDefines.NOperatives.MAX_RECRUITED_OPERATIVES = 25

NDefines.NMilitary.LAND_COMBAT_STR_DAMAGE_MODIFIER = 0.025
NDefines.NMilitary.LAND_COMBAT_ORG_DAMAGE_MODIFIER = 0.025
NDefines.NMilitary.LAND_AIR_COMBAT_STR_DAMAGE_MODIFIER = 0.08
NDefines.NMilitary.LAND_AIR_COMBAT_ORG_DAMAGE_MODIFIER = 0.12
NDefines.NMilitary.LAND_COMBAT_STR_ARMOR_ON_SOFT_DICE_SIZE = 6
NDefines.NMilitary.LAND_COMBAT_COLLATERAL_FACTOR = 0.02

NDefines.NPolitics.BASE_POLITICAL_POWER_INCREASE = 2
