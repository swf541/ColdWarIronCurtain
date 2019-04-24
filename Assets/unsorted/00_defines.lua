NDefines = {

NGame = {
	START_DATE = "1949.5.23.12",
	END_DATE = "2050.5.23.12",
	MAP_SCALE_PIXEL_TO_KM = 7.114,					-- Yes, we did the math
	SAVE_VERSION = 3,
	LAG_DAYS_FOR_LOWER_SPEED = 10,					-- Days of client lag for decrease of gamespeed
	LAG_DAYS_FOR_PAUSE = 25,						-- Days of client lag for pause of gamespeed.
	MAJOR_PARTICIPANTS_FOR_MAJOR_WAR = 3,			-- Minimum number of major countries involved in a war to consider it major enough to not end the game even though the enddate has been reached.
	COMBAT_LOG_MAX_MONTHS = 12,
	MESSAGE_TIMEOUT_DAYS = 60,						-- Useful if running the handsoff game. The popup messages that doesn't require the player respond will automatically hide after some timeout.	
	AIR_LOG_TIMEOUT_HOURS = 24,						-- Data storring data
},

NDiplomacy = {
	DIPLOMACY_REQUEST_EXPIRY_DAYS = 30,
	BASE_SURRENDER_LEVEL = 1.0,						-- Surrender when level reached. valid 0-1
	MAX_FEAR_VALUE = 100,							-- Max fear value cap.
	MIN_FEAR_VALUE = -100,							-- Min fear  value cap.
	BASE_FEAR_FACTOR = 0,							-- Base fear factor in % for opinion
	MAX_TRUST_VALUE = 100,							-- Max trust value cap.
	MIN_TRUST_VALUE = -100,							-- Min trust value cap.
	BASE_TRUST_FACTOR = 100,						-- Base trust factor in % for opinion.
	MAX_OPINION_VALUE = 200,						-- Max opinion value cap.
	MIN_OPINION_VALUE = -200,						-- Min opinion value cap.
	BASE_TRUCE_PERIOD = 30,							-- Base truce period in days.
	TRUCE_BREAK_COST_PP = 200,						-- Base cost in PP of breaking a truce by joining a war or accepting a call to war ( you cannot declare war yourself until the truce if up ), this is then multiplied by the time left on the truce ( so once half the truce is up it only cost 50% of this )
	BASE_PEACE_ANNEX_FACTOR = 100,					-- Base factor for annexation in %.
	BASE_PEACE_PUPPET_FACTOR = 100,					-- Base factor for puppet in %.
	BASE_PEACE_LIBERATE_FACTOR = 100,				-- Base factor for liberate in %.
	BASE_PEACE_TAKE_UNCONTROLLED_STATE_FACTOR = 10.0,-- Base factor for taking state you do not control in %
	BASE_PEACE_TAKE_FACTION_CONTROLLED_STATE_FACTOR = 0.5, -- Base factor for taking state you do not control, but someone in faction does
	BASE_PEACE_FORCE_GOVERNMENT_COST = 100, 		-- Base cost for forcing a country to change government.
	BASE_IMPROVE_RELATION_COST = 10,                -- Political power cost to initiate relation improvement
	BASE_IMPROVE_RELATION_SAME_IDEOLOGY_GROUP_MAINTAIN_COST = 0.2, -- Political power cost each update when boosting relations with nation of same ideology
	BASE_IMPROVE_RELATION_DIFFERENT_IDEOLOGY_GROUP_MAINTAIN_COST = 0.4,    -- Political power cost each update when boosting relations with nation of different ideology
	BASE_GENERATE_WARGOAL_DAILY_PP = 0.2,	-- Daily pp cost for generation of wargoals
	WARGOAL_VERSUS_MAJOR_AT_WAR_REDUCTION = -0.75, 	-- reduction of pp cost for wargoal vs major at war.
	WARGOAL_WORLD_TENSION_REDUCTION = -0.5,			-- Reduction of pp cost for wargoal at 100% world tension, scales linearly
	WARGOAL_JUSTIFY_TENSION_FROM_PRODUCTION = 30.0,	-- Base value scaled by production capacity of country compared to biggest country
	MIN_WARGOAL_JUSTIFY_COST = 2.0,					-- It always takes atleast 10 days to justify a wargoal
	WARGOAL_PER_JUSTIFY_AND_WAR_COST_FACTOR = 1.5,	-- Cost factor per nation at war with or justifying against
	ER_JUSTIFY_AND_WAR_COST_FACTOR = 1.5,			-- Cost factor per nation at war with or justifying against
	BASE_BOOST_PARTY_POPULARITY_DAILY_PP = 0.25, 	-- Daily pp cost for boost party popularity
	BASE_BOOST_PARTY_POPULARITY_DAILY_DRIFT = 0.1, 	-- Daily amount of popularity that will be added by the activity.
	
	BASE_STAGE_COUP_DAILY_PP = 0.5,					-- Daily pp cost for staging a coup
	BASE_STAGE_COUP_TOTAL_COST = 200, 				-- Equipment consume factor for stage coup.
	NAP_EXPIRY_MONTHS = 48,                         -- NAPs expire after this many months
	NAP_UNBREAKABLE_MONTHS = 12,                    -- NAPS cannot be broken for this many months
	NAP_FORCE_BALANCE_RULE_MONTHS = 6,        		-- The NAP border force balance rule changes with this interval
	NAP_BREAK_FORCE_BALANCE_1 = 2.0,              	-- 2-1 brigades along the border required to break NAP
	NAP_BREAK_FORCE_BALANCE_2 = 1.0,              	-- 1-1 brigades along the border required to break NAP
	NAP_BREAK_FORCE_BALANCE_3 = 0.5,              	-- 1-2 brigades along the border required to break NAP
	VERY_GOOD_OPINION = 50,							-- Threshold for a country that has a very good opinion of you.
	VERY_BAD_OPINION = -50,							-- Threshold for a country that has a very bad opinion of you.
	TRADE_NEUTRAL_OPINION_FACTOR = 0.50,			-- If Both fear and trust are 0, this is the neutral factor for trade
	TRADE_OPINION_FACTOR_FACTOR = 100.0,				-- How much the factor should effect the possible trade amount. Setting TRADE_NEUTRAL_OPINION_FACTOR to 1.0 and TRADE_OPINION_FACTOR_FACTOR to 0 means opinion does nothing in regards to trade.
	DIPLOMACY_HOURS_BETWEEN_REQUESTS = 24,			-- How long a country must wait before sending a new diplomatic request.
	TROOP_FEAR = 1, 								-- Impact on troops on borders when deciding how willing a nation is to trade
	FLEET_FEAR = 1,									-- Impact on troops on borders when deciding how willing a nation is to trade
	IC_TO_EQUIPMENT_COUP_RATIO = 0.1,				-- Ratio for calculating cost of staging coup
	VOLUNTEERS_PER_TARGET_PROVINCE = 0.10,			-- Each province owned by the target country contributes this amount of volunteers to the limit.
	VOLUNTEERS_PER_COUNTRY_ARMY = 0.10,				-- Each army unit owned by the source country contributes this amount of volunteers to the limit.
	VOLUNTEERS_RETURN_EQUIPMENT = 0.95,				-- Returning volunteers keep this much equipment
	VOLUNTEERS_TRANSFER_SPEED = 14,					-- days to transfer a unit to another nation
	VOLUNTEERS_DIVISIONS_REQUIRED = 1,				-- This many divisons are required for the country to be able to send volunteers.
	TENSION_STATE_VALUE = 5,						-- Tension value gained by annexing one state
	TENSION_CIVIL_WAR_IMPACT = 0.2,					-- civil war multiplier on tension.
	TENSION_NO_CB_WAR = 15,							-- Amount of tension generated by a no-CB war
	TENSION_CB_WAR = 5,							-- Amount of tension generated by a war with a CB
	TENSION_ANNEX_NO_CLAIM = 2,						-- Amount of tension generated by annexing a state you don't have claims on
	TENSION_ANNEX_CLAIM = 1.5,						-- Amount of tension generated by annexing a state you DO have claims on
	TENSION_ANNEX_CORE = 1,							-- Amount of tension generated by annexing a state that is your core
	TENSION_PUPPET = 2,								-- Amount of tension generated by puppeting (per state)
	TENSION_GENERATE_WARGOAL = 1,					-- Amount of tension generated by generating a wargoal against a country
	TENSION_VOLUNTEER_FORCE_DIVISION = 0.5,			-- Amount of tension generated for each sent division
	TENSION_DECAY = 0.10,							-- Each months tension decays this much
	TENSION_SIZE_FACTOR = 0.25,						-- All action tension values are multiplied by this value
	TENSION_TIME_SCALE_START_DATE = "1999.1.1.12",	-- Starting at this date, the tension values will be scaled down (will be equal to 1 before that)
	TENSION_TIME_SCALE_MONTHLY_FACTOR = 0.00,		-- Timed tension scale will be modified by this amount starting with TENSION_TIME_SCALE_START_DATE
	TENSION_TIME_SCALE_MIN = 0.0,					-- Timed tension scale won't decrease under this value
	TENSION_GUARANTEE = 0,
	TENSION_FACTION_JOIN = 4,
	TENSION_JOIN_ATTACKER = 2,						-- scale of the amount of tension added when country joins attacker side
	TENSION_PEACE_FACTOR = 0.0,					-- scale of the amount of tension (from war declaration) reduced when peace is completed.
	TENSION_LIBERATE = 0,							-- Amount of tension generated by liberating a country. 
	TENSION_CAPITULATE = 1.0,						-- Scale of the amount of tension created by a countries capitulation.
	GUARANTEE_COST = 25,							-- Scale with the number of already guaranteed countries.
	REVOKE_GUARANTEE_COST = 25,
	MP_NUM_WINNERS_FOR_PEACE_PAUSE = 0,				-- Number of human players as winners needed for peace conference to pause and open for everyone in multiplayer, needs to fullfill MP_NUM_LOSERS_FOR_PEACE_PAUSE as well.
	MP_NUM_LOSERS_FOR_PEACE_PAUSE = 0,				-- Number of human players as losers needed for peace conference to pause and open for everyone in multiplayer, needs to fullfill MP_NUM_WINNERS_FOR_PEACE_PAUSE as well.
	BASE_CONDITIONAL_PEACE_WARESCORE_RATIO = 0.5, 	-- Warscore ratio needed for the losing side to able to surrender.
	BASE_CONDITIONAL_PEACE_MONTHS = 6,				-- War length must be before a surrender i possible.
	JOINING_NAP_WAR_PENALTY = 0.2,					-- National Unity penalty for breaking non-breakable NAP
	BREAKING_GUARANTEE_PENALTY = 0.2,				-- National Unity penalty for breaking guarantee
	PEACE_SCORE_PER_PASS = 0.2,						-- When you pass in a peace deal you gain this percent of your original score
	MAX_REMEMBERED_LEASED_IC = 1000,				-- Maximum of leased equipment value that is remembered for opinion bonus
	MAX_OPINION_FOR_LEASED_IC = 30,					-- Positive opinion when remembering the MAX_REMEMBERED_LEASED_IC equipment
	MONTHLY_LEASED_IC_DECAY = 35,					-- How much of leased equipment is being "forgot" each month
	OPINION_PER_VOLUNTEER = 3,						-- Opinion bonus per one sent volunteer division
	MAX_OPINION_FROM_VOLUNTEERS = 30,				-- Opinion bonus per one sent volunteer division
	MAX_PARTICIPANTS_FOR_MAJOR_COUNTRIES = 5,		-- If we have more then x aggressors/defenders we only list major countries in tooltip for warscore progressbar or entry in world tension view
	OPINION_FOR_DEMO_FROM_WT_GENERATION = -2.0,		-- How much less do democracies like us if we generate world tension
	NOT_READY_FOR_WAR_BASE = -50,					-- AI should be unwilling to enter accept a call to war if not ready for war against the relevant enemies.
	NOT_READY_FOR_WAR_VAL_PER_DAY_SINCE_CALL = 1,	-- Value modifying the not ready base over time.
	PEACE_MIN_SCORE = 0.3,							-- Value how much of your score you are always allowed to take
	TAKE_STATES_PUPPET_COST_MULT = 0.5,				-- Cost multiplier for feeding states to a puppet that you have created, assuming the puppet currently owns the states
	TAKE_STATES_LIBERATE_COST_MULT = 0.5,			-- Cost multiplier for feeding states to a country that has been liberated, assuming the country has cores on the states
	TAKE_STATES_CHANGE_GOV_COST_MULT = 0.5,			-- Cost multiplier for feeding states to a country you are changing government on, assuming they currently own the states
	TAKE_STATES_GIVE_CORE_TO_SUBJECT_MULT = 0.1,	-- Cost multiplier for feeding core states to a subject 
		
	RESOURCE_SENT_AUTONOMY_DAILY_BASE = 0.0,		-- If puppet provides resources to its master they increasy their autonomy by at least this amount
	RESOURCE_SENT_AUTONOMY_DAILY_FACTOR = 0.005,	-- If puppet provides resources to its master they increasy their autonomy by the resources factored by this
	WAR_SCORE_AUTONOMY_BASE = 0.0,					-- Value added if any war score is contributed by puppet
	WAR_SCORE_AUTONOMY_FACTOR = 0.6,				-- If puppet generates war score it get a boost to independence 
	LL_TO_OVERLORD_AUTONOMY_DAILY_BASE = 0.0,		-- If puppet lend leases equipment to overlord of at least same tech level as they have, they gain autonomy
	LL_TO_OVERLORD_AUTONOMY_DAILY_FACTOR = 0.05,	-- If puppet lend leases equipment to overlord of at least same tech level as they have, they gain autonomy
	LL_TO_PUPPET_AUTONOMY_DAILY_BASE = 0.0,			-- If overlord lend leases equipment to puppet of higher tech level as they have, puppet losses autonomy
	LL_TO_PUPPET_AUTONOMY_DAILY_FACTOR = -0.01,		-- If overlord lend leases equipment to puppet of higher tech level as they have, puppet losses autonomy
	AUTONOMY_FREEDOM_FROM_CAPITULATE = 0.5,         -- if overlord capitulate you get this
	
	AUTONOMY_LEVEL_CHANGE_PP_COST_BASE = 50.0,		-- Base cost of changing level of autonomy
	AUTONOMY_LEVEL_CHANGE_PP_ANNEX = 300,			-- Annexation cost
	AUTONOMY_LEVEL_CHANGE_PP_FREE = 300,			-- Break free cost
	MAX_SCORE_DIFF_TO_CHANGE_AUTONOMY = 10,			-- The max diff between current freedom score and the cap for next or previous level allowed for changing
	MASTER_BUILD_AUTONOMY_FACTOR = -0.7,            -- scales autonomy gain from construction by this
	VICTORY_POINT_WORTH_FACTOR = 10,				-- multiplier when calcualting proince worth (surrender)
	VICTORY_POINT_WORTH_FACTOR_WARSCORE = 0.2,		-- multiplier when calcualting province worth with autonomy/warscore
	IDEOLOGY_JOIN_FACTION_MIN_LEVEL = 0,			-- ideology limit required to join faction
	JOIN_FACTION_LIMIT_CHANGE_AT_WAR = 0.5,			-- if in defensive war this or your modifier is counted as limit to join factions (so if you have 80% join limit this now means you can join at 50%)
	LICENSE_ACCEPTANCE_OPINION_FACTOR = 0.2,		-- Opinion modifier for acceptance of license production requests.
	LICENSE_ACCEPTANCE_PUPPET_BASE = 20,			-- Acceptance modifier for puppets requesting production licenses.
	LICENSE_ACCEPTANCE_TECH_DIFFERENCE = 5, 		-- Acceptance modifier for each year of technology difference.
	LICENSE_ACCEPTANCE_TECH_DIFFERENCE_BASE = 20,    -- Acceptance base for tech difference
	LICENSE_ACCEPTANCE_SAME_FACTION = 20,			-- Acceptance modifier for being in the same faction
},

NCountry = {
	EVENT_PROCESS_OFFSET = 20,						-- Events are checked every X day per character or province (1 is ideal, but CPU heavy)
	BASE_RESEARCH_SLOTS = 2,						-- Base number of research slots per country.
	VP_TO_SUPPLY_BASE = 1,							-- Bonus to supply from a VP, no matter the level
	VP_TO_SUPPLY_BONUS_CONVERSION = 0.1,			-- Bonus to supply local supplies from Victory Points, multiplied by this aspect and rounded to closest integer
	SUPPLY_FROM_DAMAGED_INFRA = 0.3,                -- damaged infrastructure counts as this in supply calcs
	SUPPLY_BASE_MULT = 1,							-- multiplier on supply base values
	SUPPLY_BONUS_FROM_INPUT = 0.25,					-- % of supply bonus from input area.
	SUPPLY_PATH_MAX_DISTANCE = 15,					-- When supply route reach more than X nodes, the manpower+equipment delivery speed reach 100% penalty.
	POPULATION_YEARLY_GROWTH_BASE = 0.015,			-- basic population growth per year, used for monthly manpower gain
	RESISTANCE_STRENGTH_FROM_VP = 0.001,			-- How much strength ticking speed gives each VP score.
	RESISTANCE_STRENGTH_FROM_UNIT = 0.001,			-- How much strength ticking speed is reduced from each unit in state (multiplies subunit value resistance_suppress)
	RESISTANCE_STRENGTH_FROM_NEIGHBORS = 0.5, 		-- Multiplies how much resistance can spread from one state to its neighbors, a state will spread whatever is highest of its victorypoints resistance increase or half of any of its neighbors spread, multiplied by this
	RESISTANCE_DECAY_WHEN_NO_GROWTH = 0.005,		-- Resistance will fall by this much each day if there is nothing increasing it ( no VPs and no spread from neighbors )
	REINFORCEMENT_DIVISION_PRIORITY_COUNT = 3, 		-- How many priority stages we have in division template? 0)Reserves, 1)Normal, 2)Elite.
	REINFORCEMENT_DIVISION_PRIORITY_DEFAULT = 1, 	-- Each template by default is 1)Normal
	REINFORCEMENT_THEATER_GROUP_PRIORITY_DEFAULT = 1,-- Each theater group by default is 1)Normal
	REINFORCEMENT_THEATRE_PRIORITY_COUNT = 3,		-- Same as with divisions...
	REINFORCEMENT_THEATRE_PRIORITY_DEFAULT = 1,
	REINFORCEMENT_AIRBASE_PRIORITY_COUNT = 3,
	REINFORCEMENT_AIRBASE_PRIORITY_DEFAULT = 1,
	REINFORCEMENT_DELIVERY_SPEED_MIN = 0.6,			-- The distance from the supply region to capital should affect the speed only a little bit. Main factor for penalty is overcrowded areas, and not the route length.
	REINFORCEMENT_EQUIPMENT_DELIVERY_SPEED = 0.3,	-- Modifier for army equipment reinforcement speed
	REINFORCEMENT_MANPOWER_DELIVERY_SPEED = 10.0,	-- Modifier for army manpower reinforcement delivery speed (travel time)
	REINFORCEMENT_MANPOWER_CHUNK = 0.1,				-- Chunk size of manpower reinforcement delivery, in % of total manpower needed by the template.
	EQUIPMENT_UPGRADE_CHUNK_MAX_SIZE = 10,			-- Maximum chunk size of equipment upgrade distribution per update.
	COUNTRY_SCORE_MULTIPLIER = 1.0,					-- Weight of the country score.
	ARMY_SCORE_MULTIPLIER = 0.15,					-- Based on number of armies.
	NAVY_SCORE_MULTIPLIER = 1.0,					-- Based on number of navies.
	AIR_SCORE_MULTIPLIER = 0.1,						-- Based on number of planes (which is typically a lot).
	INDUSTRY_SCORE_MULTIPLIER = 1.0,				-- Based on number of factories.
	PROVINCE_SCORE_MULTIPLIER = 0.1,				-- Based on number of controlled provinces.
	NUCLEAR_PRODUCTION_SCALE = 365,					-- +1 nuclear_production gives 1 nuke per year
	NUCLEAR_BOMB_DROP_UNITY_EFFECT_MAX_INFRA = 0.2, -- Reduce enemy national unity on nuking a province, the value scales with infrastructure up to this number
	NUCLEAR_BOMB_DROP_UNITY_EFFECT_MAX_VP = 3,		-- National unity will be scaled down if there's less VP than this in the province
	WEEKLY_UNITY_GAIN = 0.0,
	RESOURCE_ORIGIN_PRIORITY = 1,					-- Default convoy priority for resources shipped internally
	RESOURCE_EXPORT_PRIORITY = 1,					-- Default convoy priority for export trade
	RESOURCE_LENDLEASE_PRIORITY = 1,				-- Default convoy priority for export lend lease
	SUPPLY_CONVOY_FACTOR = 0.25,					-- How many convoys each supply needs
	CONVOY_RANGE_FACTOR = 1,                        -- how much range affects convoy need
	LOCAL_MANPOWER_ACCESSIBLE_FACTOR = 0.5,         -- accessible recruitable factor base
	LOCAL_MANPOWER_ACCESSIBLE_NON_CORE_FACTOR = 0.02,  -- accessible recruitable factor base
	STATE_CONTROLLER_VP_RATIO_FLIP = 0.5,			-- If current state controller has less share than this of state total and no armies in it the state changes controller
	DEFAULT_NATIONAL_UNITY = 0.7,					-- Default national unity if not scripted otherwise.
	MAX_NATIONAL_UNITY = 0.90,
	FRONT_PROVINCE_SCORE = 20,    					-- Max province score of a front. Used for the hostile troop alert
	FRONT_PROVINCE_SCORE_HOSTILE_TROOPS = -1, 		-- If province score in a front is below this value we are losing territory, and hostile troop alert will show.
	MAJOR_IC_RATIO = 3,                             -- difference in total factories needed to be considered major with respect to other nation
	MAJOR_MIN_FACTORIES = 35,						-- need at least these many factories to become a major
	MAX_INTELLIGENCE_DIFFERENCE = 3.0,				-- Max difference in intelligence levels between countries
	MAX_INTELLIGENCE_DATA_DEVIATION = 1.0,          -- Max deviation in estimating default espionage values ( 0.0 - 1.0 )
	MAX_INTELLIGENCE_MILITARY_DATA_DEVIATION = 1.0, -- Max deviation in estimating enemy military units amount ( 0.0 - 1.0 )
	MAX_INTELLIGENCE_NAVY_DATA_DEVIATION = 0.3,		-- Max deviation in estimating enemy ships amount ( 0.0 - 1.0 )
	MAX_INTELLIGENCE_AIR_DATA_DEVIATION = 1.0,		-- Max deviation in estimating enemy air planes amount ( 0.0 - 1.0 )
	MAX_INTELLIGENCE_INDUSTRY_DATA_DEVIATION = 0.4,	-- Max deviation in estimating enemy industry amount ( 0.0 - 1.0 )
	MAX_INTELLIGENCE_CONVOY_DATA_DEVIATION = 0.3,	-- Max deviation in estimating enemy convoys amount ( 0.0 - 1.0 )
	MAX_INTELLIGENCE_MANPOWER_DATA_DEVIATION = 0.4,	-- Max deviation in estimating enemy total manpower amount ( 0.0 - 1.0 )
	MAX_INTELLIGENCE_FIELDED_MANPOWER_DATA_DEVIATION = 0.35, -- Max deviation in estimating enemy fielded manpower amount ( 0.0 - 1.0 )
	MIN_MANPOWER_RATIO = 0.15,						-- Min manpower ratio to show manpower alert
	ARMY_IMPORTANCE_FACTOR = 5.0,					-- Army factor for AI and calculations
	VICTORY_POINTS_IMPORTANCE_FACTOR = 5.0,			-- State victory points importance factor for AI and calculations
	BUILDING_IMPORTANCE_FACTOR = 3.0,				-- State building importance factor for AI and calculations
	RESOURCE_IMPORTANCE_FACTOR = 0.1,				-- State resource importance factor for AI and calculations
	INTERPOLATED_FRONT_STEPS_SHORT = 2,				-- Performance optimization - The amount of steps for interpolated fronts. Non-AI countries got full interpolated fronts, the rest has optimized version of it.
	MIN_AIR_RESERVE_RATIO = 0.33,					-- Min manpower ratio to show air reserves alert
	THEATRES_BIND_BORDER_DISTANCE = 25000,			-- Map distance (before sqrt) between the center of the borders that determines if theatres should be bound or not.
	POLITICAL_POWER_CAP = 2000.0,					-- Max amount of political power country should have
	RESISTANCE_IMPORTANT_LEVEL = 0.05,				-- Level when resistance becomes dangerous
	MIN_MAJOR_COUNTRIES	= 7,						-- MIN_MAJOR_COUNTRIES countries with most factories will be considered as major countries
	ADDITIONAL_MAJOR_COUNTRIES_IC_RATIO = 0.7,		-- Countries will also be considered major when having more factories that the average of top MIN_MAJOR_COUNTRIES countries' factories times ADDITIONAL_MAJOR_COUNTRIES_IC_RATIO
	BASE_TENSION_MAJOR_COUNTRY_INDEX = 1,			-- Which major country should be considered the base country when scaling generated world tension. 0 is the country with the most factories, 1 is the second most-factories country etc. This number has to be lower than MIN_MAJOR_COUNTRIES
	MIN_NAVAL_SUPPLY_EFFICIENCY = 0.1,				-- Min ratio when supplies will be considered delivered from the capital by naval path
	PARADROP_AIR_SUPERIORITY_RATIO = 0.7,			-- Min ratio of air superiority for paradropping
	STATE_VALUE_BUILDING_SLOTS_MULT = 4.0,			-- The Value of each building slot in a state ( Value is used to determine costs in peace conference and PP cost to occupy )
	STATE_VALUE_RESEOURCE_MULT = 0.2,				-- The Value of each resource in a state ( Value is used to determine costs in peace conference and PP cost to occupy)
	STATE_OCCUPATION_COST_MULTIPLIER = 0.01,		-- Multiplier for state value to PP cost for occupation
	STATE_VALUE_NON_CORE_STATE_FRACTION = 0.5,		-- If a state is not a core we assume we will get 50% of the factory slots
	INVASION_REPORT_EXPERATION_DAYS = 30,			-- Invasion experation days
	MIN_FOCUSES_FOR_CONTINUOUS = 10,				-- Focuses needed to unlock continuous focuses
	AUTONOMOUS_TOTAL_SCORE = 4000,					-- Total score for autonomous scale
	AUTONOMOUS_SPILLOVER = 0.025,					-- Total score that can be saved to reach next level
	CIVIL_WAR_INVOLVEMENT_MIN_TENSION = 0.0,		-- base value of world tension to involve other sides to the civil war
	UNCAPITULATE_LEVEL = 0.1,                       -- if we reclaim this much and our capital we reset capitulate status
},

NProduction = {
	MAX_EQUIPMENT_RESOURCES_NEED = 3, 	-- Max number of different strategic resources an equipment can be dependent on.
	MAX_CIV_FACTORIES_PER_LINE = 15,	-- Max number of factories that can be assigned a single production line.
	MAX_NAV_FACTORIES_PER_LINE = 15,
	MAX_MIL_FACTORIES_PER_LINE = 15,
	EFFICIENCY_LOSS_PER_UNUSED_DAY = 1,		-- Daily loss of efficiency for unused factory slots ( efficiency is tracked per factory slot in the production line )
	MAX_LINE_RESOURCE_PENALTY = 90,		-- Max penalty factor for production lines lacking strategic resources in %.
	RESOURCE_PENALTY_WARNING_CRITICAL_RATIO = 0.8, -- Switch to red progress bar if penalty is over threshold 
	BASE_FACTORY_SPEED = 5, 				-- Base factory speed multiplier (how much hoi3 style IC each factory gives).
	BASE_FACTORY_SPEED_MIL = 5, 				-- Base factory speed multiplier (how much hoi3 style IC each factory gives).
	BASE_FACTORY_SPEED_NAV = 2.5, 				-- Base factory speed multiplier (how much hoi3 style IC each factory gives).
	BASE_FACTORY_START_EFFICIENCY_FACTOR = 10,	-- Base start efficiency for factories expressed in %.
	BASE_FACTORY_MAX_EFFICIENCY_FACTOR = 50,	-- Base max efficiency for factories expressed in %.
	BASE_FACTORY_EFFICIENCY_GAIN = 1,		-- Base efficiency factor.
	BASE_FACTORY_EFFICIENCY_BALANCE_FACTOR = 0.1, 			-- Factory efficiency balancing factor
	BASE_FACTORY_EFFICIENCY_VARIANT_CHANGE_FACTOR = 90,		-- Base factor for changing production variants in %.
	BASE_FACTORY_EFFICIENCY_PARENT_CHANGE_FACTOR = 30,		-- Base factor for changing production parent<->children in %.
	BASE_FACTORY_EFFICIENCY_FAMILY_CHANGE_FACTOR = 70,		-- Base factor for changing production with same family in %.
	BASE_FACTORY_EFFICIENCY_ARCHETYPE_CHANGE_FACTOR = 20, 	-- Base factor for changing production with same archetype in %.
	BASE_CONSUMER_GOODS_NEED_FACTOR = 50,  -- Base factor for the consumer goods need of civilian factories in %.
	EQUIPMENT_BASE_LEND_LEASE_WEIGHT = 1.0, -- Base equipment lend lease weight
	EQUIPMENT_LEND_LEASE_WEIGHT_FACTOR = 0.01, -- Base equipment lend lease factor
	ANNEX_STOCKPILES_RATIO = 1.0,		-- How much stockpiled equipment will be transferred on annexation
	ANNEX_FIELD_EQUIPMENT_RATIO = 0.25,	-- How much equipment from deployed divisions will be transferred on annexation
	ANNEX_CONVOYS_RATIO = 0.15,			-- How many convoys will be transferred on annexation
	MIN_POSSIBLE_TRAINING_MANPOWER = 100000,	-- How many deployment lines minimum can be training
	MIN_FIELD_TO_TRAINING_MANPOWER_RATIO = 0.75,	-- Ratio which % of army in field can be trained
	CAPITULATE_STOCKPILES_RATIO = 0.5, -- How much equipment from deployed divisions will be transferred on capitulation
	INFRA_MAX_CONSTRUCTION_COST_EFFECT = 1, 		-- Building in a state with higher infrastructure will reduce the cost of shared buildings.
	PRODUCTION_RESOURCE_LACK_PENALTY = -0.05,			-- Penalty decrease while lack of resource per factory
	MIN_LICENSE_ACTIVE_DAYS = 30,						-- Min days for license to be active
	BASE_LICENSE_IC_COST = 1,							-- Base IC cost for lended license
	LICENSE_IC_COST_YEAR_INCREASE = 1,					-- IC cost equipment for every year of equipment after 1936
	LICENSE_EQUIPMENT_BASE_SPEED = -0.25,				-- base MIC speed modifier for licensed equipment
	LICENSE_EQUIPMENT_TECH_SPEED_PER_YEAR = -0.05,		-- MIC speed modifier for licensed equipment for each year of difference between actual and latest equipment
	LICENSE_EQUIPMENT_TECH_SPEED_MAX_YEARS = 4,			-- Maximum years for MIC speed modifier
	LICENSE_EQUIPMENT_SPEED_NOT_FACTION = -0.10,		-- MIC speed modifier for licensed equipment for not being in faction
	LICENSE_EQUIPMENT_UPGRADE_XP_FACTOR = 2.0,			-- XP cost for upgrading licensed equipment
	LICENSE_EQUIPMENT_SPEED_NO_LICENSE = -0.50,			-- Penalty for producing non licensed equipment
	CONVERSION_SPEED_BONUS = 2.0,						-- Modifier to the production speed when converting equipment
},

NTechnology = {
	MAX_SUBTECHS = 3,						-- Max number of sub technologies a technology can have.
	BASE_RESEARCH_POINTS_SAVED = 50.0,		-- Base amount of research points a country can save per slot.
	BASE_YEAR_AHEAD_PENALTY_FACTOR = 7,		-- Base year ahead penalty
	BASE_TECH_COST = 100,					-- Base cost for a tech. multiplied with tech cost and ahead of time penalties
	MAX_TECH_SHARING_BONUS = 0.5, 			-- Max technology sharing bonus that can be applied instantly
	LICENSE_PRODUCTION_TECH_BONUS = 0.2,	-- License production tech bonus
},

NPolitics = {
	BASE_LEADER_TRAITS = 3,				-- Base amount of leader traits.
	MAX_RANDOM_LEADERS = 1,				-- Maximum amount random leader to have per party.
	BASE_POLITICAL_POWER_INCREASE = 2,	-- Weekly increase of PP.
	ARMY_LEADER_COST = 5,					-- cost for recruiting new leaders, 'this value' * number_of_existing_leaders_of_type
	NAVY_LEADER_COST = 5,					-- cost for recruiting new leaders, 'this value' * number_of_existing_leaders_of_type
	GOAL_COST_FACTOR = 1.0,				-- Multiplayer for cost of political goals
	LEADER_TRAITS_XP_SHOW = 0.05,			-- Amount of XP a trait needs to be shown in tooltips of a leader.
	REVOLTER_PARTY_POPULARITY = 0.4,		-- Revolter party loses 80% popularity when the civil war breaks out
	MIN_OVERTHROWN_GOVERNMENT_SUPPORT_RATIO = 0.4, -- Min possible support for new government after puppeting the government
	NUM_OCCUPATION_POLICIES = 4,		-- Number of potential occupation policies
	DEFAULT_OCCUPATION_POLICY = 1,		-- Defaullt value for occupation policy
	INSTANT_WIN_REVOLTER_POPULARITY_RATIO = 0.4, -- Min party popularity for instant win in one province state
	INSTANT_WIN_POPULARITY_WIN = 50, -- New party popularity
},

NBuildings = {
	ANTI_AIR_SUPERIORITY_MULT = 5.0,	-- How much air superiority reduction to the enemy does our AA guns? Normally each building level = -1 reduction. With this multiplier.
	MAX_BUILDING_LEVELS = 15,			-- Max levels a building can have.
	AIRBASE_CAPACITY_MULT = 200,		-- Each level of airbase building multiplied by this, gives capacity (max operational value). Value is int. 1 for each airplane.
	ROCKETSITE_CAPACITY_MULT = 100,		-- Each level of rocketsite building multiplied by this, gives capacity (max operational value). Value is int. 1 for each rocket.
	NAVALBASE_CAPACITY_MULT = 10.0,		-- Each level of navalbase building multiplied by this, gives max capacity. Value is float. Each ship takes port_capacity_usage space.
	RADAR_RANGE_BASE = 20,				-- Radar range base, first level radar will be this + min, best radar will be this + max
	NAVALBASE_REPAIR_MULT = 0.075,		-- Each level of navalbase building repairs X strength. The value is spread on all ships needed reparation. Fe Navalbase lvl 5 x 0.5 str repair = 2.5 str repaired over 10 ships, so each ship repair hourly 0.25 str.
	RADAR_RANGE_MIN = 20,				-- Radar range (from state center to province center) in measure of map pixels. Exluding techs.
	RADAR_RANGE_MAX = 220,				-- Range is interpolated between building levels 1-15.
	RADAR_INTEL_EFFECT = 40,			-- Province covered by radar increases intel by 10 (where 255 is max). Province may be covered by multiple radars, then the value sums up.
	ENCRYPTION_INTEL_EFFECT = 50,		-- Intel level effect by encryption (reduces intel gained from country with encryption higher than other countries decryption)
	DECRYPTION_INTEL_EFFECT = 50,		-- Intel level effect by decryption (increases intel gained from country with decryption lower than other countries decryption)
	SABOTAGE_FACTORY_DAMAGE = 100.0,		-- How much damage takes a factory building in sabotage when state is occupied. Damage is mult by (1 + resistance strength), i.e. up to 2 x base value.
	BASE_FACTORY_REPAIR = 0.3,			-- Default repair rate before factories are taken into account
	BASE_FACTORY_REPAIR_FACTOR = 2.0,	-- Factory speed modifier when repairing.
	SUPPLY_PORT_LEVEL_THROUGHPUT = 3,   -- supply throughput per level of naval base
	INFRA_TO_SUPPLY = 2,
 	INFRA_TO_SUPPLY_COEFF = 1,
	MAX_SHARED_SLOTS = 50,				-- Max slots shared by factories
	OWNER_CHANGE_EXTRA_SHARED_SLOTS_FACTOR = 0.5, --Scale factor of extra shared slots when state owner change.
	DESTRUCTION_COOLDOWN_IN_WAR = 30,	-- Number of days cooldown between removal of buildings in war times
},

NDeployment = {
	BASE_DEPLOYMENT_TRAINING = 1,		-- Base training done each day during deployment.
},

NMilitary = {
	COMBAT_VALUE_ORG_IMPORTANCE = 1,		-- Multiplier on TotalOrganisation when determining the combat value of a division
	COMBAT_VALUE_STR_IMPORTANCE = 1,		-- Multiplier on TotalStrength when determining the combat value of a division
	
	HOURLY_ORG_MOVEMENT_IMPACT = -0.2,		-- how much org is lost every hour while moving an army.
	ZERO_ORG_MOVEMENT_MODIFIER = -0.8,		-- speed impact at 0 org.
	INFRA_ORG_IMPACT = 0.5,				-- scale factor of infra on org regain.

	INFRASTRUCTURE_MOVEMENT_SPEED_IMPACT = -0.05,	-- speed penalty per infrastucture below maximum.

	WAR_SCORE_LOSSES_RATIO = 0.2,				-- Scale how much losses will affect warscore ( per 1000 losses ).
	WAR_SCORE_LOSSES_MULT_IF_CAPITULATED = 0.5, -- How much your losses count towards warscore if you have capitulated.
	WAR_SCORE_AIR_WORTH = 0.1,              	-- how much strategic bombing will affect warscore
	WAR_SCORE_AIR_WORTH_CAP = 1000,				-- the warscore limit we get from strategic bombing
	WAR_SCORE_AIR_MONTHLY_FALLOFF = 10,			-- how much the warscore we got from the strategic bombing falls off every month.
	
	CORPS_COMMANDER_CAP = 24,			-- how many a corps commander is limited to. 0 = inf
	FIELD_MARSHALL_CAP = 0,			-- how many a marshall is limited to. 0 = inf
	UNIT_LEADER_GENERATION_CAPITAL_CONTINENT_FACTOR = 100, --Integer factor to multiply manpower.

	RECON_SKILL_IMPACT = 5, -- how many skillpoints is a recon advantage worth when picking a tactic.

	MAX_DIVISION_BRIGADE_WIDTH = 5,			-- Max width of regiments in division designer.
	MAX_DIVISION_BRIGADE_HEIGHT = 5,		-- Max height of regiments in division designer.
	MAX_DIVISION_SUPPORT_WIDTH = 2,			-- Max width of support in division designer.
	MAX_DIVISION_SUPPORT_HEIGHT = 5,		-- Max height of support in division designer.
	
	BASE_DIVISION_BRIGADE_GROUP_COST = 20, 	--Base cost to unlock a regiment slot,
	BASE_DIVISION_BRIGADE_CHANGE_COST = 5,	--Base cost to change a regiment column.
	BASE_DIVISION_SUPPORT_SLOT_COST = 10, 	--Base cost to unlock a support slot
	
	MAX_ARMY_EXPERIENCE = 500,			--Max army experience a country can store
	MAX_NAVY_EXPERIENCE = 500,			--Max navy experience a country can store
	MAX_AIR_EXPERIENCE = 500,				--Max air experience a country can store
	
	COMBAT_MINIMUM_TIME = 4,			-- Shortest time possible for a combat in hours
	SPOTTING_QUALITY_DROP_HOURS = 4, 	-- Each X hours the intel quality drops after unit was spotted.
	LEADER_GROUP_MAX_SIZE = 1000, --5,			-- Max slots for leader groups.

	LAND_COMBAT_ORG_DICE_SIZE = 4,                 -- nr of damage dice
	LAND_COMBAT_STR_DICE_SIZE = 2,                 -- nr of damage dice
	LAND_COMBAT_STR_DAMAGE_MODIFIER = 0.05,        -- global damage modifier... but some equipment is returned at end of battles see : EQUIPMENT_COMBAT_LOSS_FACTOR
	LAND_COMBAT_ORG_DAMAGE_MODIFIER = 0.05,        -- global damage modifier
	LAND_AIR_COMBAT_STR_DAMAGE_MODIFIER = 0.04,    -- air global damage modifier
	LAND_AIR_COMBAT_ORG_DAMAGE_MODIFIER = 0.04,    -- global damage modifier
	LAND_AIR_COMBAT_MAX_PLANES_PER_ENEMY_WIDTH = 3, -- how many CAS/TAC can enter a combat depending on enemy width there
	LAND_COMBAT_STR_ARMOR_ON_SOFT_DICE_SIZE = 2,   -- extra damage dice if our armor outclasses enemy
	LAND_COMBAT_ORG_ARMOR_ON_SOFT_DICE_SIZE = 6,   -- extra damage dice if our armor outclasses enemy
	LAND_COMBAT_STR_ARMOR_DEFLECTION_FACTOR = 0.5, -- damage reduction if armor outclassing enemy
	LAND_COMBAT_ORG_ARMOR_DEFLECTION_FACTOR = 0.5, -- damage reduction if armor outclassing enemy
	LAND_COMBAT_COLLATERAL_FACTOR = 0.005,		   -- Factor to scale collateral damage to infra and forts with.
	LAND_COMBAT_FORT_DAMAGE_CHANCE = 5,		-- chance to get a hit to damage on forts. (out of 100)
	ATTRITION_DAMAGE_ORG = 0.1,					   -- damage from attrition to Organisation
	ATTRITION_EQUIPMENT_LOSS_CHANCE = 0.1,		   -- Chance for loosing equipment when suffer attrition. Scaled up the stronger attrition is. Then scaled down by equipment reliability.
	ATTRITION_EQUIPMENT_PER_TYPE_LOSS_CHANCE = 0.1, -- Chance for loosing equipment when suffer attrition. Scaled up the stronger attrition is. Then scaled down by equipment reliability.
	ATTRITION_WHILE_MOVING_FACTOR = 1,
	BASE_CHANCE_TO_AVOID_HIT = 90,                 -- Base chance to avoid hit if defences left.
	CHANCE_TO_AVOID_HIT_AT_NO_DEF = 60,	           -- chance to avoid hit if no defences left.
	COMBAT_MOVEMENT_SPEED = 0.33,	               -- speed reduction base modifier in combat
	TACTIC_SWAP_FREQUENCEY = 24,                   -- hours between tactic swaps
	INITIATIVE_PICK_COUNTER_ADVANTAGE_FACTOR  = 0.35, -- advantage per leader level for picking a counter
	BASE_COMBAT_WIDTH = 80,                        -- base combat width
	ADDITIONAL_COMBAT_WIDTH = 40,                  -- more opened up by support attack
	AMPHIBIOUS_INVADE_MOVEMENT_COST = 24.0,        -- total progress cost of movement while amphibious invading
	LAND_SPEED_MODIFIER = 0.05,                    -- basic speed control
	RIVER_CROSSING_PENALTY = -0.3,                 -- small river crossing
	RIVER_CROSSING_PENALTY_LARGE = -0.6,           -- large river crossing
	RIVER_CROSSING_SPEED_PENALTY = -0.25,           -- small river crossing
	RIVER_CROSSING_SPEED_PENALTY_LARGE = -0.5,     -- large river crossing
	RIVER_SMALL_START_INDEX = 0,                   -- color indices for rivers
	RIVER_SMALL_STOP_INDEX = 6,
	RIVER_LARGE_STOP_INDEX = 11,
	BASE_FORT_PENALTY = -0.15, 					   -- fort penalty
	BASE_STACKING_PENALTY = -0.1,                  -- multiple direction attack penalty
	MULTIPLE_COMBATS_PENALTY = -0.5,               -- defender penalty if attacked from multiple directions
	DIG_IN_FACTOR = 0.02,						   -- bonus factor for each dug-in level
	LEADER_SKILL_FACTOR = 0.05,                    -- bonus per skill level of leader
	BASE_LEADER_TRAIT_GAIN_XP = 1,				   -- Base xp gain for traits per hour.
	MAX_NUM_TRAITS = 6,					-- cant have more
	ENEMY_AIR_SUPERIORITY_IMPACT = -0.5,           -- effect on defense due to enemy air superiorty
	ENEMY_AIR_SUPERIORITY_DEFENSE = 0.70,	       -- more AA attack will approach this amount of help (diminishing returns)
	ENEMY_AIR_SUPERIORITY_DEFENSE_STEEPNESS = 112, -- how quickly defense approaches the max impact diminishing returns curve
	ENEMY_AIR_SUPERIORITY_SPEED_IMPACT = -0.5,     -- effect on speed due to enemy air superiority
	ENCIRCLED_PENALTY = -0.3,                      -- penalty when completely encircled
	WARSCORE_WINNER_FACTOR = 1,						-- Warscore effect on winners
	WARSCORE_DEFENDER_FACTOR = 0.3,					-- Warscore effect on defender
	WARSCORE_LOSS_FACTOR = 0.2,						-- Warscore effect on losing
	WARSCORE_TOTAL_FACTOR = 3,						-- Warscore balancing value
	WARSCORE_PROVINCE_FACTOR = 0.2,					-- Warscore effect from province
	WARSCORE_MIN_HOURS = 48,						-- minimum hours
	UNIT_EXPERIENCE_PER_COMBAT_HOUR = 0.0001,
	UNIT_EXPERIENCE_SCALE = 1.0,
	UNIT_EXPERIENCE_PER_TRAINING_DAY = 0.0015,
	TRAINING_MAX_LEVEL = 2,
	DEPLOY_TRAINING_MAX_LEVEL = 1,
	TRAINING_EXPERIENCE_SCALE = 62.0,
	TRAINING_ORG = 0.2,
	ARMY_EXP_BASE_LEVEL = 1,
	UNIT_EXP_LEVELS = { 0.1, 0.3, 0.75, 0.9 },		-- Experience needed to progress to the next level
	FIELD_EXPERIENCE_SCALE = 0.002,
	FIELD_EXPERIENCE_MAX_PER_DAY = 3,				-- Most xp you can gain per day
	EXPEDITIONARY_FIELD_EXPERIENCE_SCALE = 0.5,		-- reduction factor in Xp from expeditionary forces
	LEND_LEASE_FIELD_EXPERIENCE_SCALE = 0.005,		-- Experience scale for lend leased equipment used in combat.
	LEADER_EXPERIENCE_SCALE = 1.0,
	SLOWEST_SPEED = 4,
	REINFORCEMENT_REQUEST_MAX_WAITING_DAYS = 14,   -- Every X days the equipment will be sent, regardless if still didn't produced all that has been requested.
	REINFORCEMENT_REQUEST_DAYS_FREQUENCY = 7,	   -- How many days must pass until we may give another reinforcement request
	EXPERIENCE_COMBAT_FACTOR = 0.25,
	ALERT_VERY_LOW_SUPPLY_LEVEL = 0.3,			   -- At which point we show up the low and very low supply level alert. Value is in % of supplies supported vs required.
	ALERT_LOW_SUPPLY_LEVEL = 0.9,
	UNIT_DIGIN_CAP = 5,                           -- how "deep" you can dig you can dig in until hitting max bonus
	UNIT_DIGIN_SPEED = 1,						   -- how "deep" you can dig a day.
	PARACHUTE_FAILED_EQUIPMENT_DIV = 50.0,		   -- When the transport plane was shot down, we drop unit with almost NONE equipment
	PARACHUTE_FAILED_MANPOWER_DIV = 100.0,		   -- When the transport plane was shot down, we drop unit with almost NONE manpower
	PARACHUTE_FAILED_STR_DIV = 10.0,			   -- When the transport plane was shot down, we drop unit with almost NONE strenght
	PARACHUTE_DISRUPTED_EQUIPMENT_DIV = 1.5,	   -- When the transport plane was hit, we drop unit with reduced equipment. Penalty is higher as more hits was received (and AA guns was in the state).
	PARACHUTE_DISRUPTED_MANPOWER_DIV = 1.9,	       -- When the transport plane was hit, we drop unit with reduced manpower. Penalty is higher as more hits was received (and AA guns was in the state).
	PARACHUTE_DISRUPTED_STR_DIV = 2.2,			   -- When the transport plane was hit, we drop unit with reduced strength. Penalty is higher as more hits was received (and AA guns was in the state).
	PARACHUTE_PENALTY_RANDOMNESS = 0.1,			   -- Random factor for str,manpower,eq penalties.
	PARACHUTE_DISRUPTED_AA_PENALTY = 1,            -- How much the Air defence in the state (from AA buildings level * air_defence) is scaled to affect overall disruption (equipment,manpower,str).
	PARACHUTE_COMPLETE_ORG = 0.1,				   -- Organisation value (in %) after unit being dropped, regardless if failed, disrupted, or successful.
	PARACHUTE_ORG_REGAIN_PENALTY_DURATION = 120,   -- penalty in org regain after being parachuted. Value is in hours.
	PARACHUTE_ORG_REGAIN_PENALTY_MULT = -0.8,	   -- penalty to org regain after being parachuted.
	SHIP_MORALE_TO_ORG_REGAIN_BASE = 0.2,			   -- Base org regain per hour
	BASE_NIGHT_ATTACK_PENALTY = -0.5,
	IS_AMPHIBIOUS_LIMNIT = 0.0,					   -- If the amphibious movement is _above_ this limit it is considered amphibious
	EXILE_EQUIPMENT = 1.0,						   -- Amount of equipment to keep
	EXILE_ORG = 0.0,							   -- Amount of org to keep
	EXPERIENCE_LOSS_FACTOR = 1.00,                 -- percentage of experienced solders who die when manpower is removed
	EQUIPMENT_COMBAT_LOSS_FACTOR = 0.7,	 	       -- % of equipment lost to strength ratio in combat, so some % is returned if below 1
	SUPPLY_USE_FACTOR_MOVING = 1.5,                -- supply use when moving/fighting vs inactive
	SUPPLY_USE_FACTOR_INACTIVE = 0.95,
	SUPPLY_GRACE = 72,		-- troops always carry 3 days of food and supply
	MAX_OUT_OF_SUPPLY_DAYS = 30, 				   -- how many days of shitty supply until max penalty achieved
	OUT_OF_SUPPLY_ATTRITION = 0.3,                 -- max attrition when out of supply
	OUT_OF_SUPPLY_SPEED = -0.8,                    -- max speed reduction from supply
	NON_CORE_SUPPLY_SPEED = -0.5,				   -- we are not running on our own VP supply so need to steal stuff along the way
	OUT_OF_SUPPLY_MORALE = -0.3,                   -- max org regain reduction from supply
	TRAINING_ATTRITION = 0.06,		  			   -- amount of extra attrition from being in training
	TRAINING_MIN_STRENGTH = 0.1,					-- if strength is less than this, the unit will pause training until it's been reinforced
	AIR_SUPPORT_BASE = 0.3,                        -- base ground bonus to troops when active planes helping them
	LOW_SUPPLY = 0.99,							   -- When the supply status of an unit becomes low.
	UNIT_LEADER_MAX_SKILL_XP_BOOST_FACTOR = 2.0,   -- When a commander is at maximum level, he gains ranks faster.
	BORDER_WAR_ATTRITION_FACTOR = 0.1,			   -- How much of borderwar balance of power makes it into attrition
	BORDER_WAR_VICTORY = 0.8,					   -- At wich border war balance of power is victory declared
	REINFORCE_CHANCE = 0.02,                 	   -- base chance to join combat from back line when empty
	SPEED_REINFORCEMENT_BONUS = 0.01,              -- chance to join combat bonus by each 100% larger than infantry base (up to 200%)
	OVERSEAS_LOSE_EQUIPMENT_FACTOR = 0.75,		   -- percentage of equipment lost disbanded overseas
	ENCIRCLED_DISBAND_MANPOWER_FACTOR = 0.2,       -- percentage of manpower returned when an encircled unit is disbanded
	ORG_LOSS_FACTOR_ON_CONQUER = 0.2,              -- percentage of (max) org loss on takign enemy province
	LOW_ORG_FOR_ATTACK = 0.5,                      -- at what org % we start affecting speed when doign hostile moves. scales down ZERO_ORG_MOVEMENT_MODIFIER

	PLANNING_DECAY = 0.01,
	PLANNING_GAIN = 0.02,
	PLANNING_MAX = 0.5,                           	-- can get more from techs
	CIVILWAR_ORGANIZATION_FACTOR = 0.3,			  	-- Multiplier of org for both sides when civilwar.	
	LAND_COMBAT_ATTACKER_WINNING = 0.65,		  	-- Above this means attacker is winning
	LAND_COMBAT_DEFENDER_WINNING = 0.35,		  	-- Below this means defender is winning
	PLAN_CONSIDERED_GOOD = 0.25,					-- Plan evaluations above this value are considered more or less safe
	PLAN_CONSIDERED_BAD = -0.25,					-- Plan evaluations below this value are considered unsafe
	PLAN_MIN_AUTOMATED_EMPTY_POCKET_SIZE = 2,		-- The battle plan system will only automatically attack provinces in pockets that has no resistance and are no bigger than these many provinces
	PLAN_SPREAD_ATTACK_WEIGHT = 13.0,				-- The higher the value, the less it should crowd provinces with multiple attacks.
	PLAN_SUPPLY_FACTOR = 0.1,						-- Factor applied to available supply on a front location when determining priority
	PLAN_NEIGHBORING_ENEMY_PROVINCE_FACTOR = 0.7,	-- When calculating the importance of provinces, it takes number of enemy provinces into account, factored by this
	PLAN_PROVINCE_BASE_IMPORTANCE = 2.0,			-- Used when calculating the calue of front and defense area provinces for the battle plan system
	
	PLAN_PROVINCE_LOW_VP_IMPORTANCE_AREA = 2.0,     -- Used when calculating the calue of defense area in the battle plan system
	PLAN_PROVINCE_MEDIUM_VP_IMPORTANCE_AREA = 5.0,  -- Used when calculating the calue of defense area in the battle plan system
	PLAN_PROVINCE_HIGH_VP_IMPORTANCE_AREA = 50.0,   -- Used when calculating the calue of defense area in the battle plan system
	
	PLAN_PROVINCE_LOW_VP_IMPORTANCE_FRONT = 2.0,    -- Used when calculating the calue of fronts in the battle plan system
	PLAN_PROVINCE_MEDIUM_VP_IMPORTANCE_FRONT = 2.25, -- Used when calculating the calue of fronts in the battle plan system
	PLAN_PROVINCE_HIGH_VP_IMPORTANCE_FRONT = 2.75,  -- Used when calculating the calue of fronts in the battle plan system
	
	PLAN_SHARED_FRONT_PROV_IMPORTANCE_FACTOR = 0.8,	-- If fornt orders share end provinces, they should each have a somewhat reduced prio due to it being shared.
	
	PLAN_PORVINCE_PORT_BASE_IMPORTANCE = 9.0,		-- Added importance for area defense province with a port
	PLAN_PORVINCE_PORT_LEVEL_FACTOR = 0.5,			-- Bonus factor for port level
	PLAN_PORVINCE_AIRFIELD_BASE_IMPORTANCE = 3.0,	-- Added importance for area defense province with air field
	PLAN_PORVINCE_AIRFIELD_POPULATED_FACTOR = 1.5,	-- Bonus factor when an airfield has planes on it
	PLAN_PORVINCE_AIRFIELD_LEVEL_FACTOR = 0.25,		-- Bonus factor for airfield level
	PLAN_PORVINCE_RESISTANCE_BASE_IMPORTANCE = 10.0, -- Used when calculating the calue of defense area provinces for the battle plan system (factored by resistance level)
	
	-- These need to result in province value > 1.0 for it to matter.
	PLAN_AREA_DEFENSE_ENEMY_CONTROLLER_SCORE = 15.0,-- Score applied to provinces in the defense area order controlled by enemies
	PLAN_AREA_DEFENSE_ENEMY_UNIT_FACTOR = -2.0,		-- Factor applied to province score in area defense order per enemy unit in that province
	PLAN_AREA_DEFENSE_FORT_IMPORTANCE = 0.25,		-- Used when calculating the calue of defense area provinces for the battle plan system, works as multipliers on the rest
	PLAN_AREA_DEFENSE_COASTAL_FORT_IMPORTANCE = 5.0,-- Used when calculating the calue of defense area provinces for the battle plan system
	PLAN_AREA_DEFENSE_COAST_NO_FORT_IMPORTANCE = 2.0,-- Used when calculating the calue of defense area provinces for the battle plan system
	
	PLAN_STICKINESS_FACTOR = 100.0,					-- Factor used in unitcontroller when prioritizing units for locations
	
	PLAN_PROVINCE_PRIO_DISTRIBUTION_MIN = 0.8,		-- Lowest fraction of divisions that will be distributed based on province priority
	PLAN_PROVINCE_PRIO_DISTRIBUTION_MAX = 1.0,		-- Highest fraction of divisions that will be distributed based on province priority
	PLAN_PROVINCE_PRIO_DISTRIBUTION_DPP_HIGH = 4.0, -- At what divisions per province should we use PLAN_PROVINCE_PRIO_DISTRIBUTION_MIN
	PLAN_PROVINCE_PRIO_DISTRIBUTION_DPP_LOW = 2.0,	-- At what divisions per province should we use PLAN_PROVINCE_PRIO_DISTRIBUTION_MAX
	
	PLAN_EXECUTE_CAREFUL_LIMIT = 25,				-- When looking for an attach target, this score limit is required in the battle plan to consider province for attack
	PLAN_EXECUTE_BALANCED_LIMIT = 0,				-- When looking for an attach target, this score limit is required in the battle plan to consider province for attack
	PLAN_EXECUTE_RUSH = -200,						-- When looking for an attach target, this score limit is required in the battle plan to consider province for attack
	PLAN_EXECUTE_CAREFUL_MAX_FORT = 5,				-- If execution mode is set to careful, units will not attack provinces with fort levels greater than or equal to this
	
	PLAN_MAX_PROGRESS_TO_JOIN = 0.50,				-- If Lower progress than this, probably needs support
	
	PLAN_BLITZ_OPTIMISM = 0.2,						-- Additional combat balance value in favor of blitzing side when considering targets (not a combat bonus, just offsets planning)
	
	FLANKED_PROVINCES_COUNT = 3,					-- Attacker has to attack from that many provinces for the attack to be considered as flanking
	NUKE_MIN_DAMAGE_PERCENT = 0.1,					-- Minimum damage from nukes as a percentage of current strength/organisation
	NUKE_MAX_DAMAGE_PERCENT = 0.9,					-- Minimum damage from nukes as a percentage of current strength/organisation
	EQUIPMENT_REPLACEMENT_RATIO = 0.1,				-- Equipment min ratio after blocking the equipment type
	NUKE_DELAY_HOURS = 12,							-- How many hours does it take for the nuclear drop to happen
	PARADROP_PENALTY = -0.3, 						-- Combat penalty when recently paradropped
	PARADROP_HOURS = 48,							-- time paratroopers suffer penalties in combat
	COMBAT_SUPPLY_LACK_IMPACT = -0.33,				-- combat penalty if out of supply
	COMBAT_STACKING_START = 8,						-- at what nr of divisions stacking penalty starts
	COMBAT_STACKING_EXTRA = 4,                      -- extra stacking from directions
	COMBAT_STACKING_PENALTY = -0.02,                -- how much stackign penalty per division
	COMBAT_OVER_WIDTH_PENALTY = -2,					-- over combat width penalty per %.
	COMBAT_OVER_WIDTH_PENALTY_MAX = -0.33,			-- over combat width max (when you cant join no more).
	RETREAT_SPEED_FACTOR = 0.25,                    -- speed bonus when retreating
	STRATEGIC_SPEED_BASE = 10.0,                 	-- Speed of strategic redeployment
	STRATEGIC_INFRA_SPEED = 10.0,                   -- Max of additional speed gained trouh=gh level for strategic redeployment per infra
	STRATEGIC_REDEPLOY_ORG_RATIO = 0.1,				-- Ratio of max org while strategic redeployment
	BATALION_NOT_CHANGED_EXPERIENCE_DROP = 0.0,		-- Division experience drop if unit has same batalion
	BATALION_CHANGED_EXPERIENCE_DROP = 0.5,			-- Division experience drop if unit has different batalion
	ARMOR_VS_AVERAGE = 0.3,			                -- how to weight in highest armor & pen vs the division average
	PEN_VS_AVERAGE = 0.4,

	DECRYPTION_ADVANTAGE_BONUS = 0.05,				-- How much unit base damage and base defense is increased per decryption level compared to enemies average encryption level (ex: dec. level is 5 and enemy average enc. level is 3 then 5-3 = 2 which gives 10 % increase)
	
	LAND_EQUIPMENT_BASE_COST = 10,					-- Cost in XP to upgrade a piece of equipment one level is base + ( total levels * ramp )
	LAND_EQUIPMENT_RAMP_COST = 5,					
	NAVAL_EQUIPMENT_BASE_COST = 25,
	NAVAL_EQUIPMENT_RAMP_COST = 5,
	AIR_EQUIPMENT_BASE_COST = 25,
	AIR_EQUIPMENT_RAMP_COST = 5,
	
	FASTER_ORG_REGAIN_LEVEL = 0.25,
	FASTER_ORG_REGAIN_MULT = 1.0,
	SLOWER_ORG_REGAIN_LEVEL = 0.75,
	SLOWER_ORG_REGAIN_MULT = -0.5,
	
	DISBAND_MANPOWER_LOSS = 0.7,
	MIN_DIVISION_DEPLOYMENT_TRAINING = 0.2,			-- Min level of division training
	
	FRONT_MIN_PATH_TO_REDEPLOY = 8,					-- If a units path is at least this long to reach its front location, it will strategically redeploy.
	ARMY_INITIATIVE_REINFORCE_FACTOR = 0.25,		-- scales initiative for reinforce chance
},


NAir = {
	AIR_WING_FLIGHT_SPEED_MULT = 0.02,					-- Global speed multiplier for airplanes (affects fe.transferring to another base)
	AIR_WING_MAX_STATS_ATTACK = 100,					-- Max stats
	AIR_WING_MAX_STATS_DEFENCE = 100,
	AIR_WING_MAX_STATS_AGILITY = 100,
	AIR_WING_MAX_STATS_SPEED = 6000,
	AIR_WING_MAX_STATS_BOMBING = 100,
	AIR_WING_MAX_SIZE = 1000, 							-- Max amount of airplanes in wing
	AIR_WING_BOMB_DAMAGE_FACTOR = 2,					-- Used to balance the damage done while bombing.
	COMBAT_STACK_LIMIT = 2,								-- The biggest allowed dogfight combination (1vs1 or 2vs1). Bigger value cause that amount of airplanes matters more then their stats. Only used in naval air combat, for land air combat see COMBAT_MULTIPLANE_CAP
	COMBAT_STAT_IMPORTANCE_SPEED = 1, 				-- How important is speed when comparing stats.
	COMBAT_STAT_IMPORTANCE_AGILITY = 1, 				-- How important is agility when comparing stats.
	BIGGEST_AGILITY_FACTOR_DIFF = 2.5,					-- biggest factor difference in agility for doing damage (caps to this)
	COMBAT_DAMAGE_STATS_MULTILIER = 0.3,
	COMBAT_BETTER_AGILITY_DAMAGE_REDUCTION = 0.45, 		-- How much the better agility (then opponent's) can reduce their damage to us.
	COMBAT_AMOUNT_DIFF_AFFECT_GANG_CHANCE = 0.5, 		-- More aircrafts increases chance of situation 2vs1. ( Naval air combat only )
	COMBAT_ONE_ON_ONE_CHANCE = 0.6, 					-- Base chance for 1vs1 situation. ( Naval air combat only )
	COMBAT_SITUATION_WIN_CHANCE_FROM_STATS = 0.3, 		-- How much good stats difference (speed+agility) affects the winning chance (situation win = give a hit, not necessary kill).( Naval air combat only )
	COMBAT_SITUATION_WIN_CHANCE_FROM_GANG = 0.3, 		-- How much bonus gives the airplanes amount advantage (2vs1), to winning the situation.( Naval air combat only )
	COMBAT_MAX_WINGS_AT_ONCE = 10000, 						-- Max amount of air wings in one combat simulation. The higher value, the quicker countries may loose their wings. It's a gameplay balance value.
	COMBAT_MAX_WINGS_AT_GROUND_ATTACK = 10000,	        	-- we can really pounce a land strike and escalate
	COMBAT_MAX_WINGS_AT_ONCE_PORT_STRIKE = 10000,        -- we can really pounce a naval strike and escalate
	COMBAT_ATTACK_PASSES_AT_ONCE = 0.1,					-- Wing attack stat determines of many re-approaches in single combat they do. This is a scale of this amount to balance the gameplay. Less retries = less bloody combats, and less calculations for the CPU. ( Naval air combat only )
	AIR_REGION_SUPERIORITY_PIXEL_SCALE = 0.04,           -- air superiority scale = superiority/(pixels*this)
	COMBAT_SUP_VS_SUP_ATTACK_CHANCE_SPEED_DIFF = 0.25, 	-- How much diff in speed between aircrafts affects the chance of who attacks first in superiority vs superiority.( Naval air combat only )
	COMBAT_MULTIPLANE_CAP = 3.0,						-- How many planes can shoot at each plane on other side ( if there are 100 planes we are atttacking COMBAT_MULTIPLANE_CAP * 100 of our planes can shoot )
	COMBAT_DAMAGE_SCALE = 0.1,							-- Higher value = more shot down planes
	DETECT_CHANCE_FROM_OCCUPATION = 0.10, 				-- How much the controlled provinces in area affects the air detection base value.
	DETECT_CHANCE_FROM_RADARS = 0.5, 					-- How much the radars in area affects detection chance.
	DETECT_CHANCE_FROM_AIRCRAFTS_EFFECTIVE_COUNT = 3000, -- Max amount of aircrafts in region to give full detection bonus.
	DETECT_CHANCE_FROM_AIRCRAFTS = 0.8,					-- How much aircrafts in region improves air detection (up to effective count).
	DETECT_CHANCE_FROM_NIGHT = -0.2,					-- How much the night can reduce the air detection. (see static modifiers to check how weather affects it too.)
	DETECT_EFFICIENCY_BASE = 0.1,						-- Base value for detection efficiency (once something detected, efficiency says how many airplanes was detected).
	DETECT_EFFICIENCY_FROM_RADAR = 0.7,					-- How much radars affect the efficiency.
	DETECT_EFFICIENCY_RANDOM_FACTOR = 0.1,				-- How much randomness is in amount of detected aircrafts.
	DAY_NIGHT_COVERAGE_FACTOR = 0.5,					-- How much of the land in the region must be covered by night to consider doing night missions. The same with the day.
	HOURS_DELAY_AFTER_EACH_COMBAT = 4,					-- How many hours needs the wing to be ready for the next combat. Use for tweaking if combats happens too often. (generally used as double because of roundtrip)
	CARRIER_HOURS_DELAY_AFTER_EACH_COMBAT = 4,          -- how often carrier planes do battle inside naval combat
	NAVAL_STRIKE_TARGETTING_TO_AMOUNT = 0.3,			-- Balancing value to convert the naval_strike_targetting equipment stats to chances of how many airplanes managed to do successfull strike.
	NAVAL_STRIKE_DAMAGE_TO_STR = 3.0,					-- Balancing value to convert damage ( naval_strike_attack * hits ) to Strength reduction.
	NAVAL_STRIKE_DAMAGE_TO_ORG = 3.0,					-- Balancing value to convert damage ( naval_strike_attack * hits ) to Organisation reduction.
	NAVAL_STRIKE_AIR_VS_AIR_PASS_CHANCE = 0.5,			-- Balancing value to control
	FIELD_EXPERIENCE_SCALE = 0.003,
	FIELD_EXPERIENCE_MAX_PER_DAY = 2,					-- Most xp you can gain per day
	CLOSE_AIR_SUPPORT_EXPERIENCE_SCALE = 0.0005,			-- How much the experinence gained by CAS is scaled
	PARADROP_EXPERIENCE_SCALE = 0.03,					-- How much the experinence gained by paradropping is scaled
	BOMBING_DAMAGE_EXPERIENCE_SCALE = 0.0002,           -- How much the experinence gained by bombing is scaled
	ACCIDENT_CHANCE_BASE = 0.05,							-- Base chance % (0 - 100) for accident to happen. Reduced with higher reliability stat.
	ACCIDENT_CHANCE_CARRIER_MULT = 2.0,					-- The total accident chance is scaled up when it happens on the carrier ship.
	ACCIDENT_CHANCE_BALANCE_MULT = 0.5,					-- Multiplier for balancing how often the air accident really happens. The higher mult, the more often.
	ACCIDENT_EFFECT_MULT = 0.005,						-- Multiplier for balancing the effect of accidents
	ACE_DEATH_CHANCE_BASE = 0.003,						-- Base chance % for ace pilot die when an airplane is shot down in the Ace wing.
	ACE_DEATH_CHANCE_PLANES_MULT = 0.001,				-- The more airplanes was lost in a single airplanes (more bloody it was) the higher chance of Ace to die.
	ACE_EARN_CHANCE_BASE = 0.003,						-- Base chance % for ace pilot to be created. Happens only when successfully kill airplane/ship or damage the buildings.
	ACE_EARN_CHANCE_PLANES_MULT = 0.001,				-- The more airplanes the wing shots the higher chance of earning Ace.
	AIR_AGILITY_TO_NAVAL_STRIKE_AGILITY = 0.01,         		-- conversion factor to bring agility in line with ship AA
	AIR_DAMAGE_TO_DIVISION_LOSSES = 1.0,				-- factor for conversion air damage to division losses for details statistics of air wings
	AIR_NAVAL_KAMIKAZE_DAMAGE_MULT = 20.0,				-- Balancing value to increase usual damage to Strength for Kamikaze
	AIR_NAVAL_KAMIKAZE_LOSSES_MULT = 4.0,          			-- Balancing value to increase usual losses if Kamikaze participating in the battle
	BASE_KAMIKAZE_DAMAGE = 2.0,                    				-- Base Kamikaze death rate
	BASE_KAMIKAZE_TARGETING = 2.0,			        		-- Kamikaze can't be a bad target
	BASE_STRATEGIC_BOMBING_HIT_SHIP_CHANCE = 0.01,		-- Chance to hit a ship in port when it is bombed.
	BASE_STRATEGIC_BOMBING_HIT_SHIP_DAMAGE_FACTOR = 50,
	BASE_STRATEGIC_BOMBING_HIT_PLANE_CHANCE = 0.5,		-- Chance to hit a plane in airbase when it is bombed.
	BASE_STRATEGIC_BOMBING_HIT_PLANE_DAMAGE_FACTOR = 0.2,
	STRATEGIC_BOMBER_NUKE_AIR_SUPERIORITY = 0.0,		-- How much air superiority is needed for a tactical bomber to be able to nuke a province
	AGGRESSION_THRESHOLD = { 0.0, 0.25, 0.5 },			-- Threshold levels for mission aggressivity for air
	ACE_WING_SIZE =	100,								-- size of wing ace bonuses are set up for. if lower more bonus, if higher less bonus
	ACE_WING_SIZE_MAX_BONUS = 10,                       -- biggest bonus we can get from having a small wing with an ace on
	NO_SEARCH_MISSION_DETECT_FACTOR = -0.5,				-- value of planes not on active search missions for detection
	SUPPLY_NEED_FACTOR = 0.3, 							-- multiplies supply usage
	CAPACITY_PENALTY = 2,								-- scales penalty of having overcrowded bases.
	AIR_COMBAT_FINAL_DAMAGE_SCALE = 0.015,               -- % how many max disrupted only planes are alloed to die in a single combat
	AIR_COMBAT_FINAL_DAMAGE_PLANES = 50,                -- scaling/control for when only very few planes exist to stop roundoff issues
	AIR_COMBAT_FINAL_DAMAGE_PLANES_FACTOR = 0.1,
	AA_INDUSTRY_AIR_DAMAGE_FACTOR = -0.12,				-- 5x levels = 60% defense from bombing
	NAVAL_STRIKE_DETECTION_BALANCE_FACTOR = 0.7,		-- Value used to scale the surface_visibility stats to balance the gameplay, so 100% detection chance still won't spam the strikes.
	LEND_LEASED_EQUIPMENT_EXPERIENCE_GAIN = 0.5,		-- Value used for equipment
	ANTI_AIR_PLANE_DAMAGE_FACTOR = 0.8,					-- Anti Air Gun Damage factor
	ANTI_AIR_PLANE_DAMAGE_CHANCE = 0.1,					-- Anti Air Gun hit chance
	AIR_DEPLOYMENT_DAYS = 5,							-- Days to deploy one air wing
	PORT_STRIKE_ENEMY_SUPERIORITY_LIMIT = 0.3,			-- Min air superiority for performing of naval strike
	NAVAL_STRIKE_BASE_STR_TO_PLANES_RATIO = 0.1,		-- Max airbombers to do port strike comparing to strength
	NAVAL_COMBAT_EXTERNAL_PLANES_JOIN_RATIO = 0.05,		-- Max planes that can join a combat comparing to the total strength of the ships
	NAVAL_COMBAT_EXTERNAL_PLANES_JOIN_RATIO_PER_DAY = 0.2, -- max extra plane % that can join every day
	NAVAL_COMBAT_EXTERNAL_PLANES_MIN_CAP = 20,			-- Min cap for planes that can join naval combat
	
	DISRUPTION_FACTOR = 4.0,							-- multiplier on disruption damage to scale its effects on planes
	DISRUPTION_SPEED_FACTOR = 1.0,
	DISRUPTION_AGILITY_FACTOR = 0.0,
	DISRUPTION_ATTACK_FACTOR = 0.0,
	DISRUPTION_DETECTION_FACTOR = 1.0,
	ESCORT_FACTOR = 2.0,
	ESCORT_SPEED_FACTOR = 1.0,
	ESCORT_AGILITY_FACTOR = 1.0,
	ESCORT_ATTACK_FACTOR = 1.0,
	ESCORT_DETECTION_FACTOR = 1.0,
	DISRUPTION_DEFENCE_DEFENCE_FACTOR = 0.5,
	DISRUPTION_DEFENCE_SPEED_FACTOR = 1.0,
	DISRUPTION_DEFENCE_ATTACK_FACTOR = 0.5,
	
	CAS_NIGHT_ATTACK_FACTOR = 0.1,                      -- CAS damaged get multiplied by this in land combats at night
},

NNavy = {
	DETECTION_CHANCE_MULT_BASE = 0.04,								-- base multiplier value for detection chance. Later the chance is an average between our detection and enemy visibility, mult by surface/sub detection chance in the following defines.
	DETECTION_CHANCE_MULT_FORMATION_SPREAD_PATROL = 1.6, 			-- formation spread (max recommended value 1.0). The higher value the higher detection chance, but less ships will be on the place when combat starts.
	DETECTION_CHANCE_MULT_FORMATION_SPREAD_SEARCH_AND_DESTROY = 0.5, -- same as for patrol but for search and destroy missions, should be less then patrol
	DETECTION_CHANCE_MULT_FORMATION_SPREAD_CONVOY_RAIDING = 1.2,
	DETECTION_CHANCE_MULT_FORMATION_SPREAD_CONVOY_ESCORT = 0.9,
	DETECTION_CHANCE_MULT_RADAR_BONUS = 0.02,						-- detection chance bonus from radars. 
	DETECTION_CHANCE_MULT_AIR_SUPERIORITY_BONUS = 0.25,			-- bonus from air superiority.

	DETECTION_CHANCE_BALANCE = 2.5,								-- Value to balance gameplay. The higher value = smaller detection chance. Notice: it doesn't affect the displayed detection chance numbers, as well balanced numbers could be a very small fractions like 0.012
	DETECTION_SUBS_CHANCE_BALANCE = 30.0,						-- Same as above, but for sub detection. It should be very hard to detect just the subs.
	INTERCEPT_CONVOYS_BALANCE = 2.0,							-- Balance number to distinguish the chance of intercepting convoys in comparison to the interception of naval transfers. (Intercepting convoys happens 2x less often than naval transfers and invasions)
	BEST_CAPITALS_TO_SCREENS_RATIO = 0.25, 							-- capitals / screens ratio used for creating FEX groups in naval combat
	COMBAT_MIN_WIN_CHANCE_TO_ADVANCE_WITHOUT_WAIT = 0.8, 			-- compare our forces with enemy forces. 1.0 is equal win chances. Less then 1.0 is we have low chances. If we have at least X chances, then ships will attept to attack without waiting for the other ships that are on the way.
	COMBAT_MIN_WIN_CHANCE_TO_KEEP_FIGHTING = 0.2,		 			-- compare our forces with enemy forces. 1.0 is equal win chances. Less then 1.0 is we have low chances. If we have at least X chances, then ships will attept to attack without waiting for the other ships that are on the way.
	COMBAT_MIN_WIN_CHANCE_TO_KEEP_FIGHTING_DESPITE_NO_ENGAGE = 10.0,	-- compare our forces with enemy forces. 1.0 is equal win chances. Less then 1.0 is we have low chances. If we have at least X chances, then ships will attept to attack without waiting for the other ships that are on the way.
	COMBAT_BASE_HIT_CHANCE = 0.1,									-- base chance for hit
	COMBAT_MIN_HIT_CHANCE = 0.01,									-- never less hit chance then 1%?
	COMBAT_TORPEDO_ATTACK_MAX_RANGE = 4.0,							-- max range for torpedo attack
	COMBAT_TORPEDO_ATTACK_USE_CHANCE = 0.25,						-- chance of using torpedo attack (to avoid torpedo spam when at close distance)
	COMBAT_CLOSE_DISTANCE_MAX_HIT_CHANCE_BONUS = 0.0,				-- max bonus to hit chance when target is near. So if base is 0.5, dist.bonus is 0.1, and we are facing enemy at distance 0, the total hit chance is 0.6 (60%). When enemy is barely at our max shooting range, the bonus is 0.
	COMBAT_EVASION_TO_HIT_CHANCE = 0.007,							-- we take ship evasion stats, and mult by this value, so it gives hit chance reduction. So if reduction is 0.025 and ship evasion = 10, then there will be 0.25 (25%) lower hit chance. (Fe. 50% base -25% from evasion +10% bcoz it's very close).
	COMBAT_EVASION_TO_HIT_CHANCE_TORPEDO_MULT = 40.0,				-- the above evasion hit chance is multiplied by 400% if shooting with torpedos. Torpedoes are slow, so evasion matters more.
	MAX_EVASION_BONUS = 0.1,										-- largest evasion penalty to hitting
	TARGETING_STACKING_HIT_CHANCE_PENALTY = 0.08,                    -- penalty to hit chance for each ship targeting same target
	COMBAT_LOW_ORG_HIT_CHANCE_PENALTY = -0.5,						-- % of penalty applied to hit chance when ORG is very low.
	COMBAT_DAMAGE_RANDOMNESS = 0.3,								-- random factor in damage. So if max damage is fe. 10, and randomness is 30%, then damage will be between 7-10.
	COMBAT_TORPEDO_CRITICAL_CHANCE = 0.2,							-- chance for critical hit from torpedo.
	COMBAT_TORPEDO_CRITICAL_DAMAGE_MULT = 2.0,						-- multiplier to damage when got critical hit from torpedo. (Critical hits are devastating as usualy torpedo_attack are pretty high base values).
	COMBAT_DAMAGE_TO_STR_FACTOR = 1.6,								-- casting damage value to ship strength multiplier. Use it ot balance the game difficulty.
	COMBAT_DAMAGE_TO_ORG_FACTOR = 1.9,							-- casting damage value to ship organisation multiplier. Use it to balance the game difficulty.
	COMBAT_DAMAGE_REDUCTION_ON_RETREAT = 0.8,						-- Retreating ships are using their rear cannons, so the damage should be reduced.
	NAVY_MAX_XP = 100,
	COMBAT_ESCAPING_SPEED_BALANCE = 0.8,							-- Same as above, but used to balance when escaping.
	COMBAT_ON_THE_WAY_INIT_DISTANCE_BALANCE = 0.5, 					-- Value to balance initial distance to arrive for ships that are "on the way"	
	COMBAT_CHASE_RUNNERS_SPEED_COMPARE_BALANCE = 0.6,				-- When we chanse runners and they are faster then us, then we resign. But if we are faster then them by a very small speed difference, the chase may takes weeks. So this tweak value allows to resign chasing if speed difference is not so big.
	COMABT_CHASE_RUNNERS_TIMEOUT_HOURS = 10,						-- Stop chasing after timeout
	COMBAT_CHASE_RESIGNATION_HOURS = 8,								-- Before we resign chasing enemy, give them some minimum time so the combat doesn't end instantly.
	COMBAT_SHIP_SPEED_TO_FIELD_FACTOR = 0.03,						-- Modifier to the ships speed in the combat. For better balance, make it lower to slow down the speed of approaching.
	COMBAT_MAX_DISTANCE_TO_CENTER_LINE = 50,						-- Max distance to center line. Use fire_range in subunits or equipment to compare how big is the battlefield.
	COMBAT_MAX_DISTANCE_TO_ARRIVE = 80,							-- Max distance to arrive. When ships are on their way, their distance will never exceed this value.
	COMBAT_MAX_GROUPS = 3,										-- Max amount of "Fire Exchange" groups (FEX).
	COMBAT_MIN_DURATION = 8,										-- Min combat duration before we can retreat. It's a balancing variable so it's not possible to always run with our weak ships agains big flotillas.
	COMBAT_RETREAT_DECISION_CHANCE = 0.22, 							-- There is also random factor in deciding if we should retreat or not. That causes a delay in taking decision, that sooner or later will be picked. It's needed so damaged fast ships won't troll the combat.
	COMBAT_DETECTED_CONVOYS_FROM_SURFACE_DETECTION_STAT = 0.1,		-- Each 1.0 of surface_detection that ship has (equipment stat), gives x% of convoys discovered from total travelling along the route.
	COMBAT_LEAD_TOO_MANY_SHIPS_PENALTY_SPEED = 0.1,					-- Speed penalty in % for ships coming into the battle (Those in the "incoming" field). Fe. 0.1 makes the ordinary speed drop down to 10% of the original speed when penalty is at max. Value should be between 0.0 and 1.0
	COMBAT_LEAD_TOO_MANY_SHIPS_PENALTY_CHAOS_CHANCE = 0.5,			-- Chaos penalty - chance % of not taking a shot at the target.
	COMBAT_BASE_CRITICAL_CHANCE = 0.1,								-- Base chance for receiving a critical chance. It get's scaled down with ship reliability.
	COMBAT_CRITICAL_DAMAGE_MULT = 5.0,								-- Multiplier for the critical damage. Scaled down with the ship reliability.
	COMBAT_ARMOR_PIERCING_CRITICAL_BONUS = 3.0,						-- Bonus to critical chance when shooter armor piercing is higher then target armor.
	COMBAT_ARMOR_PIERCING_DAMAGE_REDUCTION = -0.9,					-- All damage reduction % when target armor is >= then shooter armor piercing.
	REPAIR_AND_RETURN_PRIO_LOW = 0.2,								-- % of total Strength. When below, navy will go to home base to repair.
	REPAIR_AND_RETURN_PRIO_MEDIUM = 0.5,							-- % of total Strength. When below, navy will go to home base to repair.
	REPAIR_AND_RETURN_PRIO_HIGH = 0.9,								-- % of total Strength. When below, navy will go to home base to repair.
	REPAIR_AND_RETURN_PRIO_LOW_COMBAT = 0.1,						-- % of total Strength. When below, navy will go to home base to repair (in combat).
	REPAIR_AND_RETURN_PRIO_MEDIUM_COMBAT = 0.3,						-- % of total Strength. When below, navy will go to home base to repair (in combat).
	REPAIR_AND_RETURN_PRIO_HIGH_COMBAT = 0.5,						-- % of total Strength. When below, navy will go to home base to repair (in combat).
	REPAIR_AND_RETURN_AMOUNT_SHIPS_LOW = 0.2,						-- % of total damaged ships, that will be sent for repair-and-return in one call.
	REPAIR_AND_RETURN_AMOUNT_SHIPS_MEDIUM = 0.4,					-- % of total damaged ships, that will be sent for repair-and-return in one call.
	REPAIR_AND_RETURN_AMOUNT_SHIPS_HIGH = 0.8,						-- % of total damaged ships, that will be sent for repair-and-return in one call.
	REPAIR_AND_RETURN_MAX_STR_DAMAGE = 0.9,							-- Ships that STR is below this value will be sent for repair and return.
	REPAIR_AND_RETURN_UNIT_DYING_STR = 0.2,							-- Str below this point is considering a single ship "dying", and a high priority to send to repair.
	EXPERIENCE_LOSS_FACTOR = 1.00,                 					-- percentage of experienced solders who die when manpower is removed
	NAVY_EXPENSIVE_IC = 5500,										-- How much IC is considering the fleet to be expensive. Those expensive will triger the alert, when are on low STR.
	MISSION_MAX_REGIONS = 3,										-- Limit of the regions that can be assigned to naval mission. Set to 0 for unlimited.
	CONVOY_EFFICIENCY_LOSS_MODIFIER = 1.5,							-- How much efficiency drops when losing convoys. If modifier is 0.5, then losing 100% of convoys in short period, the efficiency will drop by 50%.
	CONVOY_EFFICIENCY_REGAIN_AFTER_DAYS = 7,						-- Convoy starts regaining it's efficiency after X days without any convoys being sink.
	CONVOY_EFFICIENCY_REGAIN_BASE_SPEED = 0.04,						-- How much efficiency regains every day.
	CONVOY_EFFICIENCY_INTERPOLATION_SPEED = 0.35,					-- To avoid values going up/down really quick we slowly interpolate efficiency, this is how smooth it happens.
	CONVOY_EFFICIENCY_MIN_VALUE = 0.05,								-- To avoid complete 0% efficiency, set the lower limit.
	ANTI_AIR_TARGETTING_TO_CHANCE = 0.07,							-- Balancing value to convert averaged equipment stats (anti_air_targetting and naval_strike_agility) to probability chances of airplane being hit by navies AA.
	ANTI_AIR_ATTACK_TO_AMOUNT = 0.005,								-- Balancing value to convert equipment stat anti_air_attack to the random % value of airplanes being hit.
	NO_LEADER_MAX_SHIPS = 5,										-- Max amount of ships that can be used in the unit
	UNIT_EXPERIENCE_PER_COMBAT_HOUR = 10,
	UNIT_EXPERIENCE_SCALE = 1,
	EXPERIENCE_FACTOR_CONVOY_ATTACK = 0.05,
	EXPERIENCE_FACTOR_NON_CARRIER_GAIN = 0.05,						-- Xp gain by non-carrier ships in the combat
	EXPERIENCE_FACTOR_CARRIER_GAIN = 0.1,							-- Xp gain by carrier ships in the combat
	FIELD_EXPERIENCE_SCALE = 0.15,
	FIELD_EXPERIENCE_MAX_PER_DAY = 50,								-- Most xp you can gain per day
	LEADER_EXPERIENCE_SCALE = 1.0,
	BATTLE_NAME_VP_FACTOR = 100,									-- Name is given by ((VP value) * BATTLE_NAME_VP_FACTOR) / (Distance VP -> battle)
	BATTLE_NAME_VP_CUTOFF = 1.0,									-- If best score of above calculation is below this, name will be that of region.
	AMPHIBIOUS_LANDING_PENALTY = -0.7,								-- amphibious landing penalty
	AMPHIBIOUS_INVADE_SPEED_BASE = 0.5, 							-- every hour movement progress on amphibious invasion
	AMPHIBIOUS_INVADE_MOVEMENT_COST = 24.0, 						-- total progress cost of movement while amphibious invading
	AMPHIBIOUS_INVADE_ATTACK_LOW = 0.2, 							-- low and high cap of attack modifier scale. Scale interpolated by invasion progress.
	AMPHIBIOUS_INVADE_ATTACK_HIGH = 1.0,
	AMPHIBIOUS_INVADE_DEFEND_LOW = 1.5, 							-- low and high cap of defend modifier scale. Scale interpolated by invasion progress.
	AMPHIBIOUS_INVADE_DEFEND_HIGH = 1.0,
	AMPHIBIOUS_INVADE_LANDING_PENALTY_DECREASE = 3.5, 				-- scale of bonus that decreases "amphibious penalty" during combat, relative to invading transporter tech.
	BASE_CARRIER_SORTIE_EFFICIENCY = 0.5,							-- factor of planes that can sortie by default from a carrier
	SPREAD_BASE_SPEED = 0.04,										-- base speed when spreading/shrinkign a fleet
	SPREAD_BASE_SPEED_FACTOR = 0.3,									-- base factor between regular speed and spread speed
	SPREAD_MAX_PROVINCES = 30,										-- When regions exceeds this amount of provs, we get full penalty
	SPREAD_BIG_REGION_PENALTY = 0.9,
	CONVOY_ATTACK_BASE_FACTOR = 0.15,                               -- base % of convoys that get intercepted
	NAVAL_SPEED_MODIFIER = 0.1,	                    				-- basic speed control
	NAVAL_RANGE_TO_INGAME_DISTANCE = 0.12,							-- Scale the ship stats "naval_range" to the ingame distance
	NAVAL_MISSION_COVERAGE_DEFAULT_PROVINCES = 13.0,				-- Amount of provinces for spotting efficiency for naval missions (Ex. If a ship has a 1.3 spotting efficiency then there is a 100 % effective spotting efficiency in a region with 13 provinces ( 10 * 1.3) )
	NAVAL_INVASION_PREPARE_HOURS = 168,								-- base hours needed to prepare an invasion
	NAVAL_COMBAT_RESULT_TIMEOUT_YEARS = 2,							-- after that many years, we clear the naval combat results, so they don't get stuck forever in the memory.
	NAVAL_TRANSFER_BASE_SPEED = 6,                                  -- base speed of units on water being transported
	NAVAL_TRANSFER_BASE_NAVAL_DIST_ADD = 100,						-- Extra cost for naval movement ( compared to land movement ) when deciding what ports to use for a naval transfer
	NAVAL_TRANSFER_BASE_NAVAL_DIST_MULT = 20,						-- Multiplier for the cost of naval movement ( compared to land movement ) when deciding what ports to use for naval transfer
	NAVY_VISIBILITY_BONUS_ON_RETURN_FOR_REPAIR = 0.9,				-- Multiplier for the surface/sub visiblity when the heavily damaged fleet is returning to the home base for reparation. 1.0 = no bonus. 0.0 = invisible.
	NAVAL_SUPREMACY_INTEL_LOW = 0.3,								-- we need more intel than this to get any supremacy
	NAVAL_SUPREMACY_CAN_INVADE = 0.5,								-- required naval supremacy to perform invasions on an area
	BATTLE_ARRIVAL_SPEED_BONUS_ON_ENEMY_WITH_NO_MISSION = 4.0,		-- Idle fleet with no pending mission has a bit of advantage over spreaded ones. To balance it, increase the speed for ships that are on it's way to arrive on the battle. Value is a speed MULTIPLIER.
	CARRIER_STACK_PENALTY = 4,										-- The most efficient is 4 carriers in combat. 5+ brings the penalty to the amount of wings in battle.
	CARRIER_STACK_PENALTY_EFFECT = 0.2,								-- Each carrier above the optimal amount decreases the amount of airplanes being able to takeoff by such %.
	SUBMARINE_HIDE_TIMEOUT = 4,										-- Amount of in-game-hours that takes the submarine (with position unrevealed), to hide.
	SUBMARINE_REVEALED_TIMEOUT = 8,								-- Amount of in-game-hours that makes the submarine visible if it is on the defender side.
	SUBMARINE_REVEAL_BASE_CHANCE = 0.002,							-- Base chance for submarine detection. It's modified by the difference of a spootter's submarines detection vs submarine visibility. Use this variable for game balancing.
	SHORE_BOMBARDMENT_CAP = 0.25,
	ANTI_AIR_TARGETING = 0.9,                                       -- how good ships are at hitting aircraft
	MISSION_CONVOY_RAIDING_SPREAD_BASE = 0.32,
	MISSION_CONVOY_ESCORT_SPREAD_BASE = 0.1,
	MISSION_DEFAULT_SPREAD_BASE = 0.8,
	MIN_TRACTED_ASSIST_DAMAGE_RATIO = 0.05,							-- How much damage counts as assist damage
	SUPPLY_NEED_FACTOR = 4,										    -- multiplies supply usage
	SEA_AIR_COMBAT_MAX_WINGS_ON_STACK = 200,                        -- how many attacker planes can enter naval comabt per wave
	ENEMY_AIR_SUPERIORITY_IMPACT = -1,           					-- effect on ship efficiency due to enemy air superiorty
	DECRYPTION_SPOTTING_BONUS = 0.2,
	DISBAND_MANPOWER_LOSS = 0.0,
	},

NTrade = {
	DISTANCE_TRADE_FACTOR = -0.02,			-- Trade factor is modified by distance times this
	RELATION_TRADE_FACTOR = 5,				-- Trade factor is modified by Opinion value times this
	FEAR_TRADE_FACTOR = 1,
	ALLOW_TRADE_CUT_OFF = 0,				-- If trade factor is less than this, no trade will be allowed
	MONTH_TRADE_FACTOR = 2,					-- Each month a trade gets this much boost to it's trade factor
	MAX_MONTH_TRADE_FACTOR = 50,			-- This is the maximum bonus that can be gained from time
	BASE_TRADE_FACTOR = 150,				-- This is the base trade factor
	PUPPET_MASTER_TRADE_FACTOR = 400,		-- This is priority for puppet master
	PUPPET_TRADE_FACTOR = 0,				-- This is unpriority for puppets
	LACK_OF_CONVOYS_TRADE_FACTOR = -0.1,	-- Every hour without convoys will lower trade factor this much (regain is the same)
	BASE_LAND_TRADE_RANGE = 1000,
	PARTY_SUPPORT_TRADE_FACTOR = 50,		-- Trade factor bonus at the other side having 100 % party popularity for my party
	ANTI_MONOPOLY_TRADE_FACTOR_THRESHOLD = 0.5,		-- What percentage of resources has to be sold to the buyer for the anti-monopoly factor to take effect
	ANTI_MONOPOLY_TRADE_FACTOR = -100,		-- This is added to the factor value when anti-monopoly threshold is exceeded
},

NAI = {
	GARRISON_FRACTION = 0.0, 					-- How large part of a front should always be holding the line rather than advancing at the enemy
	
	DIPLOMATIC_ACTION_GOOD_BAD_RATIO_THRESHOLD = 1,
	BASE_RELUCTANCE = 20, 						-- Base reluctance applied to all diplomatic offers
	DIPLOMATIC_ACTION_RANDOM_FACTOR = 0.5, 		-- How much of the AI diplomatic action scoring is randomly determined (1.0 = half random, 2.0 = 2/3rd random, etc)
	DIPLOMATIC_ACTION_PROPOSE_SCORE = 50, 		-- AI must score a diplomatic action at least this highly to propose it themselves
	DILPOMATIC_ACTION_DECLARE_WAR_WARGOAL_BASE = 50, -- Base diplomatic action score bonus to go to war per wargoal
	DIPLOMATIC_ACTION_BREAK_SCORE = -10, 		-- AI must score a diplomatic action less than this to break it off	
	DIPLOMACY_CREATE_FACTION_FACTOR = 0.0,		-- Factor for AI desire to create a new faction. Val < 1.0 makes it less likely to create than to join.
	DIPLOMACY_FACTION_WRONG_IDEOLOGY_PENALTY = 0, -- AI penalty for diplomatic faction acitons between nations of different ideologies
	DIPLOMACY_FACTION_SAME_IDEOLOGY_MAJOR = 0, -- AI bonus acceptance when being asked about faction is a major of the same ideology
	DIPLOMACY_FACTION_NEUTRALITY_PENALTY = 50,	-- Neutral nations have a separate penalty, not wanting to get involved at all, rather than caring much about the difference in ideology
	DIPLOMACY_FACTION_GLOBAL_TENSION_FACTOR = 0.0,-- How much the AI takes global tension into account when considering faction actions
	DIPLOMACY_LEAVE_FACTION_OPINION_FACTOR = 0.75,-- How much the opinion of countries being targeted by faction leader matters when deciding to leave a faction (democratic only)
	DIPLOMACY_FACTION_WAR_RELUCTANCE = -50,		-- Penalty to desire to enter a faction with a country that we are not fighting wars together with.
	DIPLOMACY_SCARED_MINOR_EXTRA_RELUCTANCE = -50, -- extra reluctance to join stuff as scared minor
	DIPLOMACY_FACTION_PLAYER_JOIN = 20,			-- Bonus for human players asking to join a faction.
	DIPLOMACY_BOOST_PARTY_COST_FACTOR = 100.0,	-- Desire to boost party popularity subtracts the daily cost multiplied by this
	DIPLOMACY_STAGE_COUP_COST_FACTOR = 100.0,	-- Desire to stage a coup subtracts the cost multiplied by this
	DIPLOMACY_IMPROVE_RELATION_COST_FACTOR = 5.0,-- Desire to boost relations subtracts the cost multiplied by this
	DIPLOMACY_IMPROVE_RELATION_PP_FACTOR = 0.1,	-- Desire to boost relations adds total PP multiplied by this
	DIPLOMACY_REJECTED_WAIT_MONTHS_BASE = 4,	-- AI will not repeat offers until at least this time has passed, and at most the double
	DIPLOMACY_SEND_MAX_FACTION = 0.75,			-- Country should not send away more units than this as expeditionaries
	DIPLOMACY_ACCEPT_VOLUNTEERS_BASE = 50,		-- Base value of volunteer acceptance (help is welcome)
	DIPLOMACY_FACTION_MAJOR_AT_WAR = 1000.0,	-- Factor that will be multiplied with the surrender level in the desire to offer to the other ai to join a faction
	DIPLOMACY_FACTION_SURRENDER_LEVEL = 20, 	-- How much the recipient nation losing matters for joining a faction
	DIPLO_PREFER_OTHER_FACTION = -125,			-- The country has yet to ask some other faction it would prefer to be a part of.
	MIN_ANTAGONIZE_FOR_WARGOAL_JUSTIFICATION = -100,	-- AI countries will not fabricate claims against countries with an antagonization value lower than this.
	RESEARCH_DAYS_BETWEEN_WEIGHT_UPDATE = 7, 	-- Refreshes need scores based on country situation.
	RESEARCH_LAND_DOCTRINE_NEED_GAIN_FACTOR = 0.1, -- Multiplies value based on relative military industry size / country size.
	RESEARCH_NAVAL_DOCTRINE_NEED_GAIN_FACTOR = 0.075, -- Multiplies value based on relative naval industry size / country size.
	RESEARCH_AIR_DOCTRINE_NEED_GAIN_FACTOR = 0.08, -- Multiplies value based on relative number of air base / country size.
	RESEARCH_NEW_WEIGHT_FACTOR = 0.3, 			-- Impact of previously unexplored tech weights. Higher means more random exploration.
	RESEARCH_AHEAD_BONUS_FACTOR = 2.0,          -- To which extent AI should care about ahead of time bonuses to research
	RESEARCH_BONUS_FACTOR = 1.5, 				-- To which extent AI should care about bonuses to research
	MAX_AHEAD_RESEARCH_PENALTY = 2,             -- max ahead of tiem penalty ai will pick ever
	RESEARCH_AHEAD_OF_TIME_FACTOR = 10.0, 		-- To which extent AI should care about ahead of time penalties to research
	RESEARCH_BASE_DAYS = 60,					-- AI adds a base number of days when weighting completion time for techs to ensure it doesn't only research quick techs
	DECLARE_WAR_RELATIVE_FORCE_FACTOR = 0.5,	-- Weight of relative force between nations that consider going to war
	TRADEABLE_FACTORIES_FRACTION = 0.8,			-- Will at most trade away this fraction of factories.
	MIN_DELIVERED_TRADE_FRACTION = 0.8,			-- AI will cancel trade deals that are not able to deliver more than this fraction of the agreed amount
	NAVAL_TRANSPORTS_FACTOR = 2,				-- Factor applied to the relative size of army compared to naval capacity.
	NAVAL_DOCKYARDS_SHIP_FACTOR = 1.5,			-- The extent to which number of dockyards play into amount of sips a nation wants
	NAVAL_BASES_SHIP_FACTOR = 0.75,				-- The extent to which number of naval bases play into amount of sips a nation wants
	NAVAL_STATES_SHIP_FACTOR = 0.75,			-- The extent to which number of states play into amount of sips a nation wants
	NAVAL_MAX_PRIO_THEATRES = 5,				-- A nation may have a large number of theatres, but all of them having stationed/assigned navy is redundant
	NAVAL_THEATRE_PRIO_CAPITAL_SCORE = 100,		-- Weight of capital when calculating naval theatre assignment
	NAVAL_THEATRE_PRIO_NAVAL_BASE_SCORE = 1,	-- Weight of naval bases when calculating naval theatre assignment
	NAVAL_THEATRE_PRIO_MIN_DISTANCE = 2000,		-- Minimum distance (in km) between priority theatres for naval assignment, to spread navy out
	PRODUCTION_UNAVAILABLE_RESORCE_FACTORY_FACTOR = 0.75, -- Assign/queue this proportion of desired factories when resources are short 
	PRODUCTION_EQUIPMENT_SURPLUS_FACTOR = 0.25,	-- Base value for how much of currently used equipment the AI will at least strive to have in stock
	AIR_CONTROLLED_TERRITORY_INTERCEPT_SCORE = 6,-- Interception score per controlled state in mission region
	AIR_ALLY_TERRITORY_INTERCEPT_SCORE = -400,	-- Interception score per ally controlled state in mission region
	INTERCEPT_NAVAL_BOMBING_FACTOR = 35.0,		-- Factors the weight of intercepting naval bombers in sea regions where friendly ships are
	AIR_CAS_SCORE_FACTOR = 25.0,				-- Factor applied to (friendly units) x (enemy units)) to get CAS score for region
	AIR_ENEMY_SUPERIORITY_FACTOR = 5.0,			-- How much enemy air superiority counts relative to own
	AIR_SUPERIORITY_FACTOR = 2.5,				-- Factor for air superiority score
	AIR_MIN_ASSIGN_SCORE = 10,					-- Minimum total score for region to be considered for air missions
	AIR_MIN_REASSIGN_SCORE = 25,				-- Minimum total score for region to be considered for reassigning air missions
	AIR_WING_SIZE_FACTOR = 1.0,					-- Impact on air score of assigning wings to mission
	AIR_MISSION_MIN_COVEREAGE = 0.2,			-- Between 0 and 1, limit for % coverage for air mission to be considered
	AIR_BASE_PRIORITY_DISTANCE_FACTOR = 25.0,	-- Weight of distance between region and airbase for airbase priority score
	MAX_VOLUNTEER_ARMY_FRACTION = 0.25,			-- Countries will not send more than their forces time this number to aid another country
	WANTED_UNITS_INDUSTRY_FACTORY = 1.0, 		-- How many units a country wants is partially based on how much military industry that is available

	DEPLOY_MIN_TRAINING_PEACE_FACTOR = 0.95,		-- Required percentage of training (1.0 = 100%) for AI to deploy unit in peacetime
	DEPLOY_MIN_TRAINING_WAR_FACTOR = 0.25,		-- Required percentage of training (1.0 = 100%) for AI to deploy unit in wartime
	DEPLOY_MIN_EQUIPMENT_PEACE_FACTOR = 0.95,	-- Required percentage of equipment (1.0 = 100%) for AI to deploy unit in peacetime
	DEPLOY_MIN_EQUIPMENT_WAR_FACTOR = 0.75,		-- Required percentage of equipment (1.0 = 100%) for AI to deploy unit in wartime
	DYNAMIC_STRATEGIES_THREAT_FACTOR = 4.0,		-- How much threat generated by other countries effects generated strategies
	WARGOAL_GENERATION_STRENGTH_FACTOR = 1.75,	-- Desire to generate wargoal effected negatevely if actor strength is less than this factor of target strength
	LOCATION_BALANCE_TO_ADVANCE = 0.0,			-- Limit on location strength balance between country and enemy for unit to dare to move forward.
	DIVISION_UPGRADE_MIN_XP = 5,				-- Minimum XP before attempting to upgrade a division template.
	DIVISION_CREATE_MIN_XP = 100,				-- Minimum XP before attempting to create a fresh new division template.
	VARIANT_UPGRADE_MIN_XP = 50,				-- Minimum XP before attempting to create a new variant.
	UPGRADE_XP_RUSH_UPDATE = 150,				-- If XP is above this on the daily tick the AI will attempt to spend it
	FOCUS_TREE_CONTINUE_FACTOR = 1.5,			-- Factor for score of how likely the AI is to keep going down a focus tree rather than starting a new path.
	VP_GARRISON_VALUE_FACTOR = 0.75,				-- Extent to which VP garrisons are prioritized, based on VP value and compared to other priority values.
	PLAN_VALUE_TO_EXECUTE = -0.5,				-- AI will typically avoid carrying out a plan it below this value (0.0 is considered balanced).
	DECLARE_WAR_NOT_NEIGHBOR_FACTOR = 0.25,		-- Multiplier applied before force factor if country is not neighbor with the one it is considering going to war
	CALL_ALLY_BASE_DESIRE = 20,					-- exactly what it says
	CALL_ALLY_DEMOCRATIC_DESIRE = 50,			-- Desire to call ally added for democratic AI
	CALL_ALLY_NEUTRAL_DESIRE = 25,				-- Desire to call ally added for neutral AI
	CALL_ALLY_FASCIST_DESIRE = -10,				-- Desire to call ally added for fascist AI
	CALL_ALLY_COMMUNIST_DESIRE = 75,			-- Desire to call ally added for communist AI
	JOIN_ALLY_BASE_DESIRE = 20,					-- exactly what it says
	JOIN_ALLY_DEMOCRATIC_DESIRE = 50,			-- Desire to join ally added for democratic AI
	JOIN_ALLY_NEUTRAL_DESIRE = 25,				-- Desire to join ally added for neutral AI
	JOIN_ALLY_FASCIST_DESIRE = -10,				-- Desire to join ally added for fascist AI
	JOIN_ALLY_COMMUNIST_DESIRE = 75,			-- Desire to join ally added for communist AI
	JOIN_FACTION_BOTH_LOSING = -300,			-- Desire to be in a faction when both we and htey are in losing wars
	LENDLEASE_FRACTION_OF_PRODUCTION = 0.5,		-- Base fraction AI would send as lendlease
	POLITICAL_IDEA_MIN_SCORE = 0.1,				-- Only replace or add an idea if score is above this score.
	AT_WAR_THREAT_FACTOR = 2.0,					-- How much increase in threat does AI feel for being in war against osmeone
	NEIGHBOUR_WAR_THREAT_FACTOR = 1.10, 		-- How much increase in threat does AI feel against neighbours who are at war
	POTENTIAL_ALLY_JOIN_WAR_FACTOR = 100, 		-- How much increase in threat does AI feel against neighbours who are allied against one of our enemies
	POTENTIAL_FUTURE_ENEMY_FACTOR = 100, 		-- How much increase in threat does AI feel against neighbours who at war with our allies
	NEUTRAL_THREAT_PARANOIA = 10,				-- How scared neutrals are of everyone
	DIFFERENT_FACTION_THREAT = 30,				-- Threat caused by not being in the same faction
	PLAN_MOVE_MIN_ORG_TO_ENEMY_PROVINCE = 20.0,	-- Minimum organization a unit must have to consider moving into an enemy province (not attack move)
	PLAN_ATTACK_MIN_ORG_FACTOR_LOW = 0.85,		-- Minimum org % for a unit to actively attack an enemy unit when executing a plan
	PLAN_ATTACK_MIN_STRENGTH_FACTOR_LOW = 0.4,	-- Minimum strength for a unit to actively attack an enemy unit when executing a plan
	PLAN_ATTACK_MIN_ORG_FACTOR_MED = 0.75,		-- (LOW,MED,HIGH) corresponds to the plan execution agressiveness level.
	PLAN_ATTACK_MIN_STRENGTH_FACTOR_MED = 0.3,	
	PLAN_ATTACK_MIN_ORG_FACTOR_HIGH = 0.2,		
	PLAN_ATTACK_MIN_STRENGTH_FACTOR_HIGH = 0.15,	
	PLAN_FRONTUNIT_DISTANCE_FACTOR = 10.0,		-- Factor for candidate units distance to front positions.
	PLAN_ATTACK_DEPTH_FACTOR = 0.5,				-- Factor applied to size or enemy being attacked.
	PLAN_STEP_COST_LIMIT = 11,					-- When stepping to draw a plan this cost makes it break if it hits hard terrain (multiplied by number of desired steps)
	PLAN_STEP_COST_LIMIT_REDUCTION = 3,			-- Cost limit is reduced per iteration, making hard terrain less likely to be crossed the further into enemy territory it is
	PLAN_FRONT_SECTION_MAX_LENGTH = 18,			-- When a front is longer than this it will be split in two sections for the AI
	PLAN_FRONT_SECTION_MIN_LENGTH = 10,			-- When two front sections together are this short they will be merged for the AI
	PLAN_MIN_SIZE_FOR_FALLBACK = 50,			-- A country with less provinces than this will not draw fallback plans, but rather station their troops along the front
	SEND_VOLUNTEER_EVAL_BASE_DISTANCE = 175.0,  -- How far away it will evaluate sending volunteers if not a major power
	SEND_VOLUNTEER_EVAL_MAJOER_POWER = 1.0, 	-- How willing major powers are to send volunteers.
	SEND_VOLUNTEER_EVAL_CONTAINMENT_FACTOR = 0.1, -- How much AI containment factors into its evaluation of sending volunteers.
	GIVE_STATE_CONTROL_MIN_CONTROLLED = 1,		-- AI needs to control more than this number of states before considering giving any away
	GIVE_STATE_CONTROL_MIN_CONTROL_DIFF = 2,	-- The difference in number of controlled states compared to war participation needs to be bigger than this for the AI to consider giving a state to a country
	RELATIVE_STRENGTH_TO_INVADE = 0.08,			-- Compares the estimated strength of the country/faction compared to it's enemies to see if it should invade or stay at home to defend.
	RELATIVE_STRENGTH_TO_INVADE_DEFENSIVE = 0.4,-- Compares the estimated strength of the country/faction compared to it's enemies to see if it should invade or stay at home to defend, but while being a defensive country.
	GIVE_STATE_CONTROL_BASE_SCORE = 50,			-- Base diplo score for giving away control of states
	GIVE_STATE_CONTROL_DIFF_FACTOR = 2.0,		-- Diplo score multiplier for state control compared to war participation difference
	GIVE_STATE_CONTROL_NEIGHBOR_SCORE = 20,		-- Diplo score for each neighboring state controlled by the target
	GIVE_STATE_CONTROL_NEIGHBOR_ACTOR_SCORE = -5, -- Diplo score for each neighboring state that is controlled by the sender
	GIVE_STATE_CONTROL_NEIGHBOR_OTHER_SCORE = 5, -- Diplo score for each neighboring state controlled by someone else
	GIVE_STATE_CONTROL_MAX_SCORE_DIST = 600,	-- A State that is closer to the recipient capital than this gets a score bonus based on the below value
	GIVE_STATE_CONTROL_DIST_SCORE_MULT = 0.2,	-- Multiplier for the score gained from distance ( GIVE_STATE_CONTROL_MAX_SCORE_DIST - distance ) * this
	IRRATIONALITY_LAMBDA = 200,					-- Lambda given to Poisson Random function determining if a leader should act a bit irrational 											
												-- Value of 200 should give 0.3% chance of Stalin going for instance crazy and conquering all of America
	GENERATE_WARGOAL_THREAT_BASELINE = 1.0,	-- The baseline for what the AI considers the world is getting dangerous and we want to generate wargoals	
	RESERVE_TO_COMMITTED_BALANCE = 0.1,			-- How many reserves compared to number of committed divisions in a combat (1.0 = as many as reserves as committed)
	DIPLOMACY_COMMUNIST_NOT_NEIGHBOUR = -10,	-- Communists want to stay consolidated with their influence
	MAIN_ENEMY_FRONT_IMPORTANCE = 4.0,			-- How much extra focus the AI should put on who it considers to be its current main enemy.
	EASY_TARGET_FRONT_IMPORTANCE = 7.5,			-- How much extra focus the AI should put on who it considers to be the easiest target.
	AI_FRONT_MOVEMENT_FACTOR_FOR_READY = 0.25,	-- If less than this fraction of units on a front is moving, AI sees it as ready for action	
	MICRO_POCKET_SIZE = 4,						-- Pockets with a size equal to or lower than this will be mocroed by the AI, for efficiency.
	POCKET_DISTANCE_MAX = 40000,				-- shortest square distance we bother about chasing pockets
	VP_LEVEL_IMPORTANCE_HIGH = 30,				-- Victory points with values higher than or equal to this are considered to be of high importance.
	VP_LEVEL_IMPORTANCE_MEDIUM = 10,			-- Victory points with values higher than or equal to this are considered to be of medium importance.
	VP_LEVEL_IMPORTANCE_LOW = 5,				-- Victory points with values higher than or equal to this are considered to be of low importance.
	ESTIMATED_CONVOYS_PER_DIVISION = 6,			-- Not always correct, but mainly used to make sure AI does not go crazy
	FRONT_REASSIGN_DISTANCE = 120.0,			-- If a unit is this far away from a front it is not considered to be assigned to it unless the new front is much more important
	OLD_FRONT_IMPORTANCE_FACTOR = 1.50,			-- If a unit is considered for reassignment, the importance of both new and old front is considered with a weight applied to the old ones score
	ENTRENCHMENT_WEIGHT = 2.0,					-- AI should favour units with less entrenchment when assigning units around.
	FRONT_TERRAIN_DEFENSE_FACTOR = 5.0,			-- Multiplier applied to unit defense modifier for terrain on front province multiplied by terrain importance
	FRONT_TERRAIN_ATTACK_FACTOR = 5.0,			-- Multiplier applied to unit attack modifier for terrain on enemy front province multiplied by terrain importance
	
	BASE_DISTANCE_TO_CARE = 600.0,				-- Countries that are too far away are less interesting in diplomacy
	MIN_FORCE_RATIO_TO_PROTECT = 0.5,			-- Tiny countries should not feel protective or really large ones
	
	ORG_UNIT_STRONG = 0.9,						-- Organization % for unit to be considered strong
	ORG_UNIT_WEAK = 0.15,						-- Organization % for unit to be considered weak
	STR_UNIT_STRONG = 0.75,						-- Strength (equipment) % for unit to be considered strong
	STR_UNIT_WEAK = 0.2,						-- Strength (equipment) % for unit to be considered weak
	PLAN_FACTION_STRONG_TO_EXECUTE = 0.50,		-- % or more of units in an order to consider ececuting the plan
	PLAN_FACTION_WEAK_TO_ABORT = 0.65,			-- % or more of units in an order to consider ececuting the plan
	PLAN_AVG_PREPARATION_TO_EXECUTE = 0.5,		-- % or more average plan preparation before executing
	STATE_GARRISON_MAX_UNITS = 3,				-- Max units to guard a garrison under normal circumstances (isolated core areas like England has is excempt)
	
	REDEPLOY_DISTANCE_VS_ORDER_SIZE = 1.0,		-- Factor applied to the path length of a unit compared to length of an order to determine if it should use strategic redeployment
	UNIT_ASSIGNMENT_TERRAIN_IMPORTANCE = 5.0,	-- Terrain score for units are multiplied by this when the AI is deciding which front they should be assigned to
	
	MIN_STATE_VALUE_TO_PROTECT = 7.5,			-- When AI is considering which states to protect it looks at state values to consider if it is worth it.
	
	SUPPLY_CRISIS_LIMIT = 0.9,					-- If a unit is standing in an area with 

	MAX_ALLOWED_NAVAL_DANGER = 80,				-- AI will ignore naval paths that has danger value of above this threshold while assigning units
	TRANSFER_DANGER_HOSTILE_SHIPS = 50, 		-- max danger from complete enemy naval supriority over ai in an area
	FASCISTS_BEFRIEND_FASCISTS = 10,
	FASCISTS_BEFRIEND_DEMOCRACIES = -25,
	FASCISTS_BEFRIEND_COMMUNISTS = -25,
	FASCISTS_ALLY_FASCISTS = 0,
	FASCISTS_ALLY_DEMOCRACIES = -100,
	FASCISTS_ALLY_COMMUNISTS = -100,
	FASCISTS_ANTAGONIZE_FASCISTS = -10,
	FASCISTS_ANTAGONIZE_DEMOCRACIES = 100,
	FASCISTS_ANTAGONIZE_COMMUNISTS = 100,
	DEMOCRACIES_BEFRIEND_FASCISTS = -25,
	DEMOCRACIES_BEFRIEND_DEMOCRACIES = 0,
	DEMOCRACIES_BEFRIEND_COMMUNISTS = -25,
	DEMOCRACIES_ALLY_FASCISTS = -50,
	DEMOCRACIES_ALLY_DEMOCRACIES = 0,
	DEMOCRACIES_ALLY_COMMUNISTS = -50,
	DEMOCRACIES_ANTAGONIZE_FASCISTS = 0,
	DEMOCRACIES_ANTAGONIZE_DEMOCRACIES = -25,
	DEMOCRACIES_ANTAGONIZE_COMMUNISTS = 0,
	COMMUNISTS_BEFRIEND_FASCISTS = -25,
	COMMUNISTS_BEFRIEND_DEMOCRACIES = -25,
	COMMUNISTS_BEFRIEND_COMMUNISTS = 25,
	COMMUNISTS_ALLY_FASCISTS = -100,
	COMMUNISTS_ALLY_DEMOCRACIES = -50,
	COMMUNISTS_ALLY_COMMUNISTS = 0,
	COMMUNISTS_ANTAGONIZE_FASCISTS = 100,
	COMMUNISTS_ANTAGONIZE_DEMOCRACIES = 10,
	COMMUNISTS_ANTAGONIZE_COMMUNISTS = -10,

	TENSION_MIN_FOR_GUARANTEE_VS_MINOR = 10, -- for non faction people AI will not consider you worth guaranteeing below this
	
	NUM_AI_MESSAGES = 10,				-- Set to whatever category has the highest number of messages

	DIPLOMACY_FACTION_WAR_WANTS_HELP = 50,	-- Desire to send to nations to join a faction if you are at war
	DIPLOMACY_FACTION_CIVILWAR_WANTS_HELP = -50,
	FACTION_UNSTABLE_ACCEPTANCE = -100,
	DIPLOMACY_AT_WAR_WITH_ALLY_RELUCTANCE = -1000,
	DIPLOMACY_FACTION_JOIN_COUP_INITIATOR_BONUS = 70,	-- If a country initiated coup on an another country, civil war revolter is more likely to join initiator's faction

	CALL_ALLY_WT_LIMIT = 0.8,                           -- fascists are hesitant to call allies if tension is lower than this
	CALL_ALLY_FASCIST_DESIRE_WT = -60,                  -- less desire if we are below the tension limit

	SHIPS_PRODUCTION_BASE_COST = 10000,					-- Used by the AI to normalize IC values when picking what ship to build.
	NEEDED_NAVAL_FACTORIES_EXPENSIVE_SHIP_BONUS = 12,   -- Amount of naval yards you need to get a bonus to building really expensive ships

	AIR_WING_REINFORCEMENT_LIMIT = 150,
	AIR_BASE_DANGER_ZONE_WEIGHT = 100,					-- Score used per province taken by enemy in a state to determine how dangerous it is to use an air base

	MANPOWER_FREE_USAGE_THRESHOLD = 500000,			-- If AI has this much manpower he doesn't care about the percentage
	MANPOWER_RESERVED_THRESHOLD = 0.25,					-- The AI will not deploy more units if he goes below this percentage
	START_TRAINING_EQUIPMENT_LEVEL = 0.9,               -- ai will not start to train if equipment drops below this level
	STOP_TRAINING_EQUIPMENT_LEVEL = 0.8,                -- ai will not train if equipment drops below this level
	BUILD_REFINERY_LACK_OF_RESOURCE_MODIFIER = 0.003,	-- How much lack of resources are worth when evaluating what to build.
	DIVISION_DESIGN_WEIGHTS = {							-- Base values used by AI to evaluate value of a stat
		-- Army Values
		0.5, -- default_morale
		1.0, -- defense
		1.0, -- breakthrough
		1.0, -- hardness
		1.2, -- soft_attack
		0.0, -- hard_attack
		0.0, -- recon
		0.0, -- entrenchment
		0.0, -- initiative
		0.0, -- casualty_trickleback
		-1.0, -- supply_consumption_factor
		-0.25, -- supply_consumption
		0.0, -- suppression
		0.0, -- suppression_factor
		0.0, -- experience_loss_factor
		-- Navy Values
		0.0, -- surface_detection
		0.0, -- sub_detection
		0.0, -- surface_visibility
		0.0, -- sub_visibility
		0.0, -- shore_bombardment
		0.0, -- fire_range
		0.0, -- evasion
		0.0, -- torpedo_attack
		0.0, -- sub_attack
		0.0, -- attack
		0.0, -- port_capacity_usage
		0.0, -- anti_air_attack
		0.0, -- amphibious_defense
		0.0, -- naval_speed
		0.0, -- naval_range
		0.0, -- convoy_raiding_coordination
		0.0, -- patrol_coordination
		0.0, -- search_and_destroy_coordination
		-- Air Values
		0.0, -- air_range
		0.0, -- air_defence
		0.0, -- air_attack
		0.0, -- air_agility
		0.0, -- air_bombing
		0.0, -- air_superiority
		0.0, -- naval_strike_attack
		0.0, -- naval_strike_targetting
		0.0, -- air_ground_attack
		0.0, -- air_visibility_factor
		-- Common Values
		1.0, -- max_organisation
		1.0, -- max_strength
		-0.5, -- build_cost_ic
		1.0, -- maximum_speed
		1.0, -- armor_value
		0.5, -- ap_attack
		0.0, -- reliability
		0.0, -- reliability_factor
		-0.25, -- weight
		-- Special Values
		0.0, -- strategic_attack
		0.0, -- carrier_size
	},
	DIVISION_DESIGN_MANPOWER_WEIGHT = 0.005,
	DIVISION_DESIGN_STOCKPILE_WEIGHT = 0.01,
	DIVISION_DESIGN_COMBAT_WIDTH_WEIGHT = -1.0,				-- This score is reduced the higher width is when comparing pure changes with no target
	DIVISION_DESIGN_COMBAT_WIDTH_TARGET_WEIGHT = -200.0,	-- This score is reduced the farther the width is from the target width (if set)
	DIVISION_DESIGN_MAX_FAILED_DAYS = 60,					-- max days we keep track of since failure of a design update

	BUILD_ARMOR_BASE_COST_WEIGHT = 200.0,
	BUILD_ARMOR_STRENGTH_MULTIPLIER_WEIGHT = 100.0,
	BUILD_ARMOR_ORGANIZATION_MULTIPLIER_WEIGHT = 500.0,

	UPGRADE_DIVISION_RELUCTANCE = 7,					-- How often to consider upgrading to new templates for units in the field
	UPGRADE_PERCENTAGE_OF_FORCES = 0.1,					-- How big part of the army that should be considered for upgrading

	STRATEGIC_BOMBING_DEFENCE_IMPORTANCE = 500.0,
	
	NAVAL_MISSION_MIN_FLEET_SIZE = 3,					-- AI will not send too small fleets on missions. Ignored if total number of ships country has is below	this.
	NAVY_PREFERED_MAX_SIZE = 20,						-- AI will generally attempt to merge fleets into this size, but as a soft limit.
	INVASION_COASTAL_PROVS_PER_ORDER = 12,				-- AI will consider one extra invasion per number of provinces stated here (num orders = total coast / this)

	CONVOY_NEED_SAFETY_BUFFER = 1.30,					-- AI will try and keep 15% more convoys than what it needs.
	REGION_THREAT_PER_SUNK_CONVOY = 25,					-- Threat value per convoy sunk in a region. Decays over time.
	REGION_CONVOY_DANGER_DAILY_DECAY = 1,				-- When convoys are sunk it generates threat in the region which the AI uses to prio nalval missions

	ESCORT_BOMBERS_IMPORTANCE_MODIFIER = 3.0,
	PRODUCTION_LINE_SWITCH_SURPLUS_NEEDED_MODIFIER = 0.2,	-- Is modified by efficency modifiers.
	PLAN_ACTIVATION_MAJOR_WEIGHT_FACTOR = 5.0,			-- AI countries will hold on activating plans if stronger countries have plans in the same location. Majors count extra (value of 1 will negate this)
	PLAN_ACTIVATION_PLAYER_WEIGHT_FACTOR = 50.0,		-- AI countries will hold on activating plans if player controlled countries have plans in the same location. Majors count extra (value of 1 will negate this)
	AREA_DEFENSE_BASE_IMPORTANCE = 3,					-- Area defense order base importance value (used for determining order of troop selections)
	AREA_DEFENSE_CIVIL_WAR_IMPORTANCE = 10000,			-- Area defense order importance value when a country is in a civil war as target or revolter.

	COMBINED_ARMS_LEVEL = 1,							-- 0 = Never, 1 = Infantry/Artillery, 2 = Go wild
	MAX_DISTANCE_NALAV_INVASION = 200.0,				-- AI is extremely unwilling to plan naval invasions above this naval distance limit.
	ENEMY_NAVY_STRENGTH_DONT_BOTHER = 2.5,				-- If the enemy has a navy at least these many times stronger that the own, don't bother invading
	MIN_SUPPLY_USE_SANITY_CAP = 100,					-- Ignore supply cap if below this value when deciding on how many divisions to produce.
	MAX_SUPPLY_DIVISOR = 1.75,							-- To make sure the AI does not overdeploy divisions. Higher number means more supply per unit.
	MISSING_CONVOYS_BOOST_FACTOR = 18.0,					-- The more convoys a country is missing, the more resources it diverts to cover this.
	TRANSPORTS_PER_PARATROOPER = 20,					-- Air transports only duty is to drop paratroopers.
	MAX_MICRO_ATTACKS_PER_ORDER = 3,					-- AI goes through its orders and checks if there are situations to take advantage of
	FALLBACK_LOSING_FACTOR = 1.0,						-- The lower this number, the longer the AI will hold the line before sending them to the fallback line
	PRODUCTION_MAX_PROGRESS_TTO_SWITCH_NAVAL = 0.3,		-- AI will not replace ships being built by newer types if progress is above this
	STATE_CONTROL_FOR_AREA_DEFENSE = 0.4,				-- To avoid AI sending area defense to area with very little foothold
	FORCE_FACTOR_AGAINST_EXTRA_MINOR = 0.15,			-- AI considers generating wargoals against minors below this % of force compared to themselves to get at a bigger enemy.
	MAX_EXTRA_WARGOAL_GENERATION = 2,					-- AI may want to generate wargoals against weak minors to get at larger enemy, but never more that this at any given time.
	NAVAL_MISSION_DISTANCE_BASE = 3500,					-- Base value when AI is evaluating distance score to places
	NAVAL_MISSION_INVASION_BASE = 1000,					-- Base score for region with naval invasion (modified dynamically by prioritizing orders)
	NAVAL_MISSION_AGGRESSIVE_PATROL_DIVISOR = 1,		-- Divides patrol score when not defending
	NAVAL_MISSION_AGGRESSIVE_ESCORT_DIVISOR = 2,		-- Divides escort score when not defending
	NAVAL_MISSION_PATROL_NEAR_OWNED = 50000,			-- Extra patrol mission score near owned provinces
	NAVAL_MISSION_ESCORT_NEAR_OWNED = 20000,			-- Extra escort mission score near owned provinces
	NAVAL_MISSION_PATROL_NEAR_CONTROLLED = 12000,		-- Extra patrol mission score near controlled provinces
	NAVAL_MISSION_ESCORT_NEAR_CONTROLLED = 5500,		-- Extra escort mission score near controlled provinces
	NEW_LEADER_EXTRA_PP_FACTOR = 2.0,					-- Country must have at least this many times extra PP to get new admirals or army leaders
	SCARY_LEVEL_AVERAGE_DEFENSE = -0.7,                 -- average front defense modifier to make it consider it as a PITA to go for
	ATTACK_HEAVILY_DEFENDED_LIMIT = 0.5,				-- AI will not launch attacks against heavily defended fronts unless they consider to have this level of advantage (1.0 = 100%)
	HOUR_BAD_COMBAT_REEVALUATE = 100,                   -- if we are in combat for this amount and it goes shitty then try skipping it 
	MIN_PLAN_VALUE_TO_MICRO_INACTIVE = 0.2,				-- The AI will not consider members of groups which plan is not activated AND evaluates lower than this.
	
	MAX_UNITS_FACTOR_AREA_ORDER = 1.0,					-- Factor for max number of units to assign to area defense orders
	DESIRED_UNITS_FACTOR_AREA_ORDER = 1.0,				-- Factor for desired number of units to assign to area defense orders
	MIN_UNITS_FACTOR_AREA_ORDER = 1.0,					-- Factor for min number of units to assign to area defense orders

	MAX_UNITS_FACTOR_FRONT_ORDER = 1.5,					-- Factor for max number of units to assign to area front orders
	DESIRED_UNITS_FACTOR_FRONT_ORDER = 1.5,				-- Factor for desired number of units to assign to area front orders
	MIN_UNITS_FACTOR_FRONT_ORDER = 1.0,					-- Factor for min number of units to assign to area front orders

	MAX_UNITS_FACTOR_INVASION_ORDER = 1.0,				-- Factor for max number of units to assign to naval invasion orders
	DESIRED_UNITS_FACTOR_INVASION_ORDER = 1.0,			-- Factor for desired number of units to assign to naval invasion orders
	MIN_UNITS_FACTOR_INVASION_ORDER = 1.0,				-- Factor for min number of units to assign to naval invasion orders
	
	FRONT_UNITS_CAP_FACTOR = 15.0,						-- A factor applied to total front size and supply use. Primarily effects small fronts
	MAX_DIST_PORT_RUSH = 20.0,							-- If a unit is in enemy territory with no supply it will consider nearby ports within this distance.
	
	MIN_FIELD_STRENGTH_TO_BUILD_UNITS = 0.7,			-- Cancel unit production if below this to get resources out to units in the field
	MIN_MANPOWER_TO_BUILD_UNITS = 0.7,					-- Cancel unit production if below this to get resources out to units in the field
	
	AVERAGE_SUPPLY_USE_PESSIMISM = 1.5,					-- Multiplier for when AI calculates average supply use of entire army.
	
	REQUEST_LEND_LEASE_PROTECT_VALUE = 75,				-- Limit for protect enemy desire for reducing lend lease desire
	REQUEST_LEND_LEASE_CONTAINS_VALUE = 100,			-- Limit of contain enemy desire for boosting friendly help
	REQUEST_LEND_LEASE_STOCKPILE_RATIO_LAND = 0.1,		-- Ratio to send stockpile from equipment
	REQUEST_LEND_LEASE_PRODUCTION_DAYS_LAND = 28,		-- Count of daily production amount of equipment to send
	REQUEST_LEND_LEASE_STOCKPILE_RATIO_AIR = 0.03,		-- Ratio to send stockpile from equipment
	REQUEST_LEND_LEASE_PRODUCTION_DAYS_AIR = 10,		-- Count of daily production amount of equipment to send
	REQUEST_LEND_LEASE_STOCKPILE_RATIO_NAVAL = 0.1,		-- Ratio to send stockpile from equipment
	REQUEST_LEND_LEASE_PRODUCTION_DAYS_NAVAL = 28,		-- Count of daily production amount of equipment to send
	
	FRONT_BULGE_RATIO_UPPER_CUTOFF = 1.5,				-- If total bulginess is lower than this, the front is ignored.
	FRONT_BULGE_RATIO_LOWER_CUTOFF = 0.95,				-- If local bulginess drops below this, a point of interest is found
	FRONT_CUTOFF_MIN_EDGE_PROXIMITY = 2,				-- Minimum number of provinces to the front edge to determine for cutoff oportunity.
	INVASION_DISTANCE_RANDOMNESS = 300,					-- This higher the value, the more unpredictable the invasions. Compares to actual map distance in pixels.
	
	AIR_SUPERIORITY_MISSION_FACTOR = 1.0,				-- AI air superiority mission factor
	CAS_MISSION_FACTOR = 1.4,							-- AI cas mission factor
	INTERCEPTION_MISSION_FACTOR = 0.5,					-- AI interception mission factor
	STREATEGIC_BOMBER_MISSION_FACTOR = 1.2,				-- AI strategic bombing mission factor
	NAVAL_BOMBER_MISSION_FACTOR = 0.5,					-- AI naval bombing mission factor
	NUKE_MISSION_FACTOR = 1.0,							-- AI nuke mission factor
	PARADROP_MISSION_FACTOR = 1.0,						-- AI paradrop mission factor
	KAMIKAZE_MISSION_FACTOR = 1.0,						-- AI naval kamikaze mission factor
	PORT_STRIKE_MISSION_FACTOR = 1.0,					-- AI port strike mission factor
	INDUSTRY_IC_AIR_IMPORTANCE_FACTOR = 0.02,			-- AI very specific IC cost factor for air missions
	
	AIR_SCORE_DISTANCE_IMPACT = 0.3,					-- Effect of distance applied to the score calculations
	DAYS_BETWEEN_AIR_PRIORITIES_UPDATE = 4,				-- Amount of days between air ai updates priorities for air wings ( from 1 to N )
	
	NAVAL_AIR_SUPERIORITY_IMPORTANCE = 0.10,			-- Strategic importance of air superiority ( amount of enemy planes in area )
	NAVAL_SHIP_AIR_IMPORTANCE = 2.0,					-- Naval ship air importance
	NAVAL_SHIP_IN_PORT_AIR_IMPORTANCE = 6.0,			-- Naval ship in the port air importance
	NAVAL_COMBAT_AIR_IMPORTANCE = 12.0,					-- Naval combat air importance
	NAVAL_TRANSFER_AIR_IMPORTANCE = 25.0,				-- Naval transfer air importance
	NAVAL_COMBAT_TRANSFER_AIR_IMPORTANCE = 50.0,		-- Naval combat involving enemy land units
	NAVAL_IMPORTANCE_SCALE = 1.0,						-- Naval total importance scale (every naval score get's multiplied by it)
	
	NAVAL_FIGHTERS_PER_PLANE = 1.1,						-- Amounts of air superiority planes requested per enemy plane
	NAVAL_STRIKE_PLANES_PER_ARMY = 15,					-- Amount of planes requested per enemy army
	NAVAL_STRIKE_PLANES_PER_SHIP = 5,					-- Amount of bombers requested per enemy ship
	PORT_STRIKE_PLANES_PER_SHIP = 10,					-- Amount of bombers request per enemy ship in the port
	NAVAL_MIN_EXCORT_WINGS = 0,							-- Min amount of airwings requested to excort operations
	
	LAND_DEFENSE_AIR_SUPERIORITY_IMPORTANCE = 0.10,		-- Strategic importance of air superiority ( amount of enemy planes in area )
	LAND_DEFENSE_CIVIL_FACTORY_IMPORTANCE = 50,			-- Strategic importance of civil factories
	LAND_DEFENSE_MILITARY_FACTORY_IMPORTANCE = 70,		-- Strategic importance of military factories
	LAND_DEFENSE_NAVAL_FACTORY_IMPORTANCE = 30,			-- Strategic importance of naval factories
	LAND_DEFENSE_AA_IMPORTANCE_FACTOR = 1.0,			-- Factor of AA influence on strategic importance ( 0.0 - 1.0 )
	LAND_DEFENSE_INFRA_IMPORTANCE_FACTOR = 0.5,			-- Factor of infrastructure influence on strategic importance ( 0.0 - 1.0 )
	LAND_DEFENSE_IMPORTANCE_SCALE = 1.5,				-- Lend defence total importance scale (every land defence score get's multiplied by it)
	
	LAND_DEFENSE_MIN_FACTORIES_FOR_AIR_IMPORTANCE = 6,	-- If amount of factories is less importance of factories won't apply
	
	LAND_DEFENSE_FIGHERS_PER_PLANE = 1.1,				-- Amount of air superiority planes requested per enemy plane
	LAND_DEFENSE_INTERSEPTORS_PER_BOMBERS = 0.2,		-- Amount of air interceptor planes requested per enemy plane
	
	LAND_COMBAT_AIR_SUPERIORITY_IMPORTANCE = 0.20,		-- Strategic importance of air superiority ( amount of enemy planes in area )
	LAND_COMBAT_OUR_ARMIES_AIR_IMPORTANCE = 12,			-- Strategic importance of our armies
	LAND_COMBAT_OUR_COMBATS_AIR_IMPORTANCE = 55,		-- Strategic importance of our armies in the combats
	LAND_COMBAT_FRIEND_ARMIES_AIR_IMPORTANCE = 12,		-- Strategic importance of friendly armies
	LAND_COMBAT_FRIEND_COMBATS_AIR_IMPORTANCE = 6,		-- Strategic importance of friendly armies in the combat
	LAND_COMBAT_ENEMY_ARMIES_AIR_IMPORTANCE = 8,		-- Strategic importance of our armies
	LAND_COMBAT_ENEMY_LAND_FORTS_AIR_IMPORTANCE = 5,	-- Strategic importance of enemy land forts in the region
	LAND_COMBAT_ENEMY_COASTAL_FORTS_AIR_IMPORTANCE = 3,	-- Strategic importance of enemy coastal fronts in the region
	LAND_COMBAT_IMPORTANCE_SCALE = 1.5,					-- Lend combat total importance scale (every land combat score get's multiplied by it)
	
	LAND_COMBAT_FIGHTERS_PER_PLANE = 1.1,				-- Amount of air superiority planes requested per enemy plane
	LAND_COMBAT_CAS_WINGS_PER_ENEMY_ARMY_LIMIT = 4,		-- Limit of CAS wings requested by enemy armies
	LAND_COMBAT_CAS_PER_ENEMY_ARMY = 20,				-- Amount of CAS planes requested per enemy army
	LAND_COMBAT_CAS_PER_COMBAT = 200,					-- Amount of CAS requested per combat	
	LAND_COMBAT_BOMBERS_PER_LAND_FORT_LEVEL = 15,		-- Amount of bomber planes requested per enemy land fort level
	LAND_COMBAT_BOMBERS_PER_COASTAL_FORT_LEVEL = 10,	-- Amount of bomber planes requested per enemy coastal fort level
	LAND_COMBAT_MIN_EXCORT_WINGS = 2,					-- Min amount of airwings requested to excort operations
	
	STR_BOMB_AIR_SUPERIORITY_IMPORTANCE = 0.10,			-- Strategic importance of air superiority ( amount of enemy planes in area )
	STR_BOMB_CIVIL_FACTORY_IMPORTANCE = 50,				-- Strategic importance of enemy civil factories
	STR_BOMB_MILITARY_FACTORY_IMPORTANCE = 70,			-- Strategic importance of enemy military factories
	STR_BOMB_NAVAL_FACTORY_IMPORTANCE = 30,				-- Strategic importance of enemy naval factories
	STR_BOMB_AA_IMPORTANCE_FACTOR = 0.5,				-- Factor of AA influence on strategic importance ( 0.0 - 1.0 )
	STR_BOMB_INFRA_IMPORTANCE_FACTOR = 0.25,			-- Factor of infrastructure influence on strategic importance ( 0.0 - 1.0 )
	STR_BOMB_IMPORTANCE_SCALE = 1.0,					-- str bombing total importance scale (every str bombing score get's multiplied by it)
	
	STR_BOMB_MIN_ENEMY_FIGHTERS_IN_AREA = 300,			-- If amount of enemy fighters is higher than this mission won't perform
	STR_BOMB_FIGHTERS_PER_PLANE = 1.1,					-- Amount of air superiority planes requested per enemy plane
	STR_BOMB_PLANES_PER_CIV_FACTORY = 20,				-- Amount of planes requested per enemy civ factory
	STR_BOMB_PLANES_PER_MIL_FACTORY = 25,				-- Amount of planes requested per enemy military factory
	STR_BOMB_PLANES_PER_NAV_FACTORY = 15,				-- Amount of planes requested per enemy naval factory
	STR_BOMB_MIN_EXCORT_WINGS = 2,						-- Min amount of airwings requested to excort operations
	
	ORDER_ASSIGNMENT_DISTANCE_FACTOR = 5.0,				-- When the AI assigns units to orders, it attempts to calculate the distance.
	RELUCTANCE_TO_CHANGE_FRONT_FACTOR = 0.5,			-- Factor for how reluctant the AI is to change a units order group.
	REVISITED_PROV_PENALTY_FACTOR = 1.5,				-- When the AI picks units for a front, it tries to spread out a bit which units it grabs.
	
	PLAN_ACTIVATION_SUPERIORITY_AGGRO = 1.0,			-- How aggressive a country is in activating a plan based on how superiour their force is.
	WAIT_YEARS_BEFORE_FREER_BUILDING = 3,				-- The AI will skip considering certain buildings during the buildup phase, after htese many years it starts building them regardless of threat.
	
	STRIKE_FLEET_MAX_DISTANCE_TO_COMBAT = 500.0,		-- The strike fleet will not attempt to intervene in combats further away than this.
	
	DOCKYARDS_PER_NAVAL_DESIRE_EFFECT = -20.0,			-- Effects how much AI wants to build dockyards based on how navally focused they are in general. Recommended range -100.0 to 100.0.
},

NFocus = {
	FOCUS_POINT_DAYS = 7,						-- Each point takes a week
	FOCUS_PROGRESS_PEACE = 1,					-- Progress during peace
	FOCUS_PROGRESS_WAR = 1,					-- Progress during war
	MAX_SAVED_FOCUS_PROGRESS = 10,				-- This much progress can be saved while not having a focus selected
	},
}