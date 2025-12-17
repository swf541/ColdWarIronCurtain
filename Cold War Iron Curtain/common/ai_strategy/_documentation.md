# Examples and documentation of how to use the AI strategies

Try to keep this reasonably up-to-date, please.

-------------------------

## List of available strategy tokens
(updated 2024-07)

### Related to diplomacy
- `alliance`
- `antagonize`
- `avoid_starting_wars`
- `asking_foreign_garrison`
- `befriend`
- `conquer`
- `consider_weak`
- `contain`
- `declare_war`
- `diplo_action_acceptance`
- `diplo_action_desire`
- `dont_join_wars_with`
- `ignore`
- `ignore_claim`
- `influence`
- `prepare_for_war`
- `protect`
- `send_lend_lease_desire`
- `send_volunteers_desire`
- `support`

### Related to fronts and armies
- `area_priority`
- `dont_defend_ally_borders`
- `force_defend_ally_borders`
- `force_concentration_front_factor`
- `force_concentration_factor`
- `force_concentration_target_weight`
- `front_armor_score`
- `front_control`
- `front_unit_request`
- `garrison`
- `garrison_reinforcement_priority`
- `ignore_army_incompetence`
- `invasion_unit_request`
- `invade`
- `occupation_policy`
- `put_unit_buffers`
- `scorched_earth_prio`
- `spare_unit_factor`
- `theatre_distribution_demand_increase`

### Related to navies
- `naval_avoid_region`
- `naval_convoy_raid_region`
- `naval_invasion_focus`
- `naval_invasion_dominance_weight`
- `naval_mission_threshold`
- `strike_force_home_base`

### Related to intelligence
- `activate_crypto`
- `agency_ai_base_num_factories_factor`
- `agency_ai_per_upgrade_factories_factor`
- `decrypt_target`
- `intelligence_agency_branch_desire_factor`
- `intelligence_agency_usable_factories`
- `operation_equipment_priority`
- `operative_mission`
- `operative_operation`

### Related to production and resources
- `added_military_to_civilian_factory_ratio`
- `air_factory_balance`
- `build_airplane`
- `build_army`
- `build_building`
- `build_ship`
- `building_target`
- `convoy_efficiency_to_cancel_trades`
- `dockyard_to_military_factory_ratio`
- `equipment_production_factor`
- `equipment_variant_production_factor`
- `equipment_production_surplus_management`
- `equipment_production_min_factories`
- `equipment_production_min_factories_archetype`
- `equipment_stockpile_surplus_ratio`
- `equipment_market_spend_factories`
- `equipment_market_for_sale_threshold`
- `equipment_market_for_sale_factor`
- `equipment_market_max_for_sale`
- `equipment_market_min_for_sale`
- `equipment_market_buying_threshold`
- `equipment_market_buy`
- `equipment_market_trade_desire`
- `factory_build_score_factor`
- `force_build_armies`
- `fuel_buffer`
- `min_convoy_efficiency_factor_for_war_support_hit`
- `production_upgrade_desire_offset`
- `railway_gun_divisions_ratio`
- `research_tech`
- `research_weight_factor`
- `role_ratio`
- `save_equipment`
- `template_prio`
- `unit_ratio`
- `land_xp_spend_priority`
- `air_xp_spend_priority`
- `navy_xp_spend_priority`
- `pp_spend_amount`
- `pp_spend_priority`
- `min_wanted_supply_trucks`
- `wanted_supply_trucks`
- `min_wanted_supply_trains`
- `wanted_supply_trains`
- `ai_wanted_divisions_factor`

### Related to airforce
- `strategic_air_importance`

### Related to raids
- `raid_target_country`

-------------------------


## UNIT RATIOS

### AIR
For air types unit_ratio strategy values behave like weights. If no value is set it defaults to 0. If a plane type is DLC locked its set ratio is ignored and 0 is used instead.

Land-based and carrier plane types are handled completely separate.

First we calculate the total number of planes that the AI want to produce:

**For land-based planes**:
- Sum up the total air base capacity (excluding carriers), and multiply it by `WANTED_LAND_PLANES_PER_BASE_CAPACITY_FACTOR`.
- Add the number of divisions the AI wants multiplied by `WANTED_LAND_PLANES_PER_DIVISION`.
- Subtract the number of planes in airwings.
- Clamp the value between 0 and the number of wanted divisions multiplied by `WANTED_LAND_PLANES_TOTAL_MAX_PER_DIVISION`.
- The result is then multiplied by hardcoded value `AI_FOCUS_AVIATION`, which beforehand has been multiplied by modifier `ai_focus_aviation_factor`.

**For carrier planes**:
- Sum up the total carrier deck capacity, and multiply it by `WANTED_CARRIER_PLANES_PER_CARRIER_CAPACITY_FACTOR`.
- Sum up the total deck capacity of carriers in production, where the carrier will be done in no more than `CARRIER_CAPACITY_IN_PRODUCTION_MAX_DAYS_LEFT_TO_INCLUDE_FACTOR` days, and multiply it by `WANTED_CARRIER_PLANES_PER_CARRIER_CAPACITY_IN_PRODUCTION_FACTOR`.
- Subtract the number of carrier planes in airwings.
- Clamp the value to minimum 0.
- The result is then multiplied by hardcoded value `AI_FOCUS_NAVAL_AIR`, which beforehand has been multiplied by modifier `ai_focus_naval_air_factor`.

**Finally we calculate and set the build_airplane strategy values**:
- For each land-based type we take the `unit_ratio`, divide it by the sum of all land-based `unit_ratio` values, and multiply it by the above calculated number of wanted land-based planes.
- We do the same for carrier planes.

### ALL BUT AIR
Unit ratios are calculated as a base of 100 plus the value indicated in the strategy. A unit type ratio of -40 would result in only 60% of the wanted number being set as a goal how the AI meets its goals thereafter can also be altered by other factors.

### EQUIPMENT PRODUCTION FACTOR
Same as above, with the percentage of calculated factories to meet need added to by the strategy


-------------------------

## Examples of AI strategy usage

The general structure of an AI strategy looks like this
```
name_of_strategy = {

	# For which countries is this AI strategy allowed? Used as a first-step filter, avoid expensive triggers.
	allowed = {  # Country scope
		original_tag = ENG
	}

	# Under what conditions should this AI strategy activate?
	enable = {  # Country scope
		date > 1938.1.1
	}

	# Under what conditions should this AI strategy deactivate?
	# Although optional, it's highly recommended to always include either an `abort` or `abort_when_not_enabled` statement.
	# In the rare case where the AI strategy legit should never deactivate, use `abort = { always = no }` to explicitly state that.
	abort = {  # Country scope
		num_of_military_factories > 30
	}
	# abort_when_not_enabled = yes  # if active, will deactivate as soon as `enable` is no longer true

	# Any number of ai_strategy entries that are active while this AI strategy is active.
	ai_strategy = { <...> }
	ai_strategy = { <...> }
}
```

### `avoid_starting_wars`
```
ai_strategy = {
	type = avoid_starting_wars
	# no need of id for this one
	value = -200  # this value is additive with the 'conquer' strategy, and is targetless. It is meant for very specific situations, and should not be used widely.
}

ai_strategy = {
	type = conquer
	id = GER
	value = 200  # This would therefore stack with the above value to reach a conquer weight of 0 for targeting Germany, and -200 for everyone else.
}
```

### `protect`
Negative value makes AI not guarantee independence on target country.
```
ai_strategy = {
	type = protect
	id = "CZE"
	value = 200
}
```

### `dont_defend_ally_borders`
Makes AI ignore frontlines belonging to a specific ally
```
ai_strategy = {
	type = dont_defend_ally_borders
	id = ITA
	value = 100  # This strategy is binary, any value > 0 activates it, while <= 0 deactivates it.
}
```

### `force_concentration_front_factor`
Used for increasing/decreasing priority score for AI force concentration on specified fronts.
```
ai_strategy = {
	type = force_concentration_front_factor

	tag = GER							# Target a specific country. Can specify multiple.
	state = 42							# Target a state. Can specify multiple.
	strategic_region = 65				# Target a strategic region. Can specify multiple.
	area = europe						# Target a specific ai area. Can specify multiple.
	country_trigger = { always = no }	# Trigger to check against a specific country. Scope is enemy country, FROM scope is our country.
	state_trigger = { always = no }		# Trigger to check against a state. Scope is state. FROM scope is enemy country FROM.FROM scope is our country.
	ratio = 0.0							# The strategy is enabled only if ratio of the front covered by this strategy's targets is greater than this ratio.

	value = 40							# Factor for the normal priority. 40 means +40 %, -60 means -60 %.
}
```

### `force_concentration_factor`
Used for modifying how large part of the "non-essential" units on an AIFC front will be used for concentrated pushes. ("Non-essential" essentially means the units that are left over after the minimum front requirements are fulfilled. So if a front gets 30 units assigned to it, and requires 10 units to fulfill the minimum front requirements, there would be 20 "non-essential" units.)
```
ai_strategy = {
	type = force_concentration_factor
	value = 20							# Factor added on top of the base ratio (see define FORCE_CONCENTRATION_UNIT_RATIO_BASE). 20 means +20 %, so if the base ratio define is 15 % the result would be 15+20 = 35 %.
}
```

### `force_concentration_target_weight`
Affects the score for offensive targets for AI Force Concentration.
```
ai_strategy = {
	type = force_concentration_target_weight

	tag = GER							# Target a specific country. Can specify multiple.
	state = 42							# Target a state. Can specify multiple.
	strategic_region = 65				# Target a strategic region. Can specify multiple.
	area = europe						# Target a specific ai area. Can specify multiple.
	country_trigger = { always = no }	# Trigger to check against a specific country. Scope is enemy country, FROM scope is our country.
	state_trigger = { always = no }		# Trigger to check against a state. Scope is state. FROM scope is enemy country FROM.FROM scope is our country.

	value = 60							# Factor for the normal priority. 40 means +40 %, -60 means -60 %.
}
```

### `front_control`
Used for controlling invasion or regular fronts
```
ai_strategy = {
	type = front_control

	# you can define a target in following ways. you can define more than one

	tag = GER							# Target a specific country. Can specify multiple.
	state = 42							# Target a state. Can specify multiple.
	strategic_region = 65				# Target a strategic region. Can specify multiple.
	area = europe						# Target a specific ai area. Can specify multiple.
	country_trigger = { always = no }	# Trigger to check against a specific country. Scope is enemy country, FROM scope is our country.
	state_trigger = { always = no }		# Trigger to check against a state. Scope is state. FROM scope is enemy country FROM.FROM scope is our country.
	ratio = 0.0							# The strategy is enabled only if ratio of the front covered by this strategy's targets is greater than this ratio.

	priority = 0						# Default 0, higher prio strats will override lower.
	ordertype = front					# `front` or `invasion`. If set this strategy will only apply to that specific order type.
	execution_type = careful			# One of {`careful`, `balanced`, `rush`, `rush_weak`}. If set will override the execution type of front (only for front orders).
	execute_order = yes					# `yes` or `no`. If set will override execute or not decision of front.
	manual_attack = yes					# Default `yes`. If `no` AI will not do manual pokes at enemy (only for front orders).
}
```

### `front_control`
Low-level frontline control. Good for example to force the AI to blitz an area.
```
ai_strategy = {
	type = front_control
	tag = HOL				# Can also target country, state, strategic_region, area. Can also specify multiple targets, each on its own line
	ratio = 0.25			# At least this ratio of the frontline provinces need to be targeted for the AI strat to apply
	priority = 100			# Higher prio strats will override lower
	ordertype = front		# Can be either {front, invasion}
	execution_type = rush	# Can be either {careful, balanced, rush, rush_weak}
	execute_order = yes		# If set, will force activate/deactivate execution
	manual_attack = yes		# If set the AI will try manual poke attacks (for front orders)
}
```

### `front_unit_request` and `invasion_unit_request`
Used for increasing/decreasing unit requests for invasions or fronts
```
ai_strategy = {
	# use one of them
	type = front_unit_request / invasion_unit_request

	# invasions will check invasion target, fronts will check provinces at front

	tag = GER							# Target a specific country. Can specify multiple.
	state = 42							# Target a state. Can specify multiple.
	strategic_region = 65				# Target a strategic region. Can specify multiple.
	area = europe						# Target a specific ai area. Can specify multiple.
	country_trigger = { always = no }	# Trigger to check against a specific country. Scope is enemy country, FROM scope is our country.
	state_trigger = { always = no }		# Trigger to check against a state. Scope is state. FROM scope is enemy country FROM.FROM scope is our country.

	value = 40							# Will be added as a factor over regular requests.
}
```

### `invade`
Affects the AI's naval invasion behavior against the specified country. If it's negative, it avoids invasions completely. If it's positive, the value acts as a factor on the importance score of invasions against the country as long as it's a potential enemy.
```
ai_strategy = {
	type = invade
	id = ITA
	value = -10  # negative, so the AI will avoid invading the specified country
	# value = 60  # positive, so any invasions against the specified country will have their importance score multiplied by 1.6 (if it's a potential enemy).
}
```

### `put_unit_buffers`
This strategy will make ai buffer/garrison some units in a target area which can be used in orders that is in target areas.
```
ai_strategy = {
	type = put_unit_buffers

	# ratio of total armeis in country to be buffered
	ratio = 0.4

	# you can specify an order id. ratio of same orders ids will be share same ratio
	order_id = 2

	# states to put garrison orders (if no state is friendly, strat is invalid)
	states = {
		125
		126
		127
		128
		129
		338
		123
		122
	}

	# ai areas that the orders will use these buffers in
	area = europe
	area = asia

	# by default if you have orders in target areas, the buffer will request less units.
	# you can override this to disable the feature
	subtract_invasions_from_need = yes
	subtract_fronts_from_need = yes
}
```

### `theatre_distribution_demand_increase`
Makes AI increase unit demand for the war fronts and area defense fronts belonging to the theatre that contains the specified state
```
ai_strategy = {
	type = theatre_distribution_demand_increase
	id = 447  # State ID for Alexandria, so will target the theatre where Alexandria belongs
	value = 10  # Increase desired unit demand by 10
}
```

### `naval_invasion_dominance_weight`
Used to make the AI focus more of their navy on increasing naval supremacy in regions where one of their naval invasions passes through
```
ai_strategy = {
	type = naval_invasion_dominance_weight
	value = 30
}
```

### `intelligence_agency_branch_desire_factor`
```
ai_strategy = {
	type = intelligence_agency_branch_desire_factor
	id = branch_defense
	value = -50  # -50% on the AI weight
}
```

### `intelligence_agency_usable_factories`
```
ai_strategy = {
	type = intelligence_agency_usable_factories
	# no need of id for this one
	value = 10
}
```

### `operative_mission`
```
ai_strategy = {
	type = operative_mission
	mission = build_intel_network	# mission token
	value = 800						# score compared to other operations & missions
	mission_target = GER			# target
	state = 1						# if specified ai will prefer this states for targeted operations assuming they are valid target
	state = 2
	priority = 100					# ai will prefer state of the highest prio strategy
}
```

### `operative_operation`
Makes ai do an operation
```
ai_strategy = {
	type = operative_operation
	operation = operation_id
	value = 900				# score compared to other operations & missions
	operation_target = GER 	# target
	state = 1				# if specified ai will prefer this states for targeted operations assuming they are valid target
	state = 2
	region = 1				# if specified ai will prefer this regions for targeted operations assuming they are valid
	region = 2
	priority = 100			# ai will prefer state/region of the highest prio strategy
}
```

### `build_building`
Used to make the AI build buildings, optionally in a certain location.
NOTE: This strategy is also used dynamically by the internal AI, with default weight value of 1.
```
ai_strategy = {
	type = build_building
	id = coastal_bunker  # Type of building

	target = 139  # Optional target location, where to build. Treated as province ID if provincial building, and state ID if state building. If the building cannot be constructed in the specified location, then the strategy is ignored.
	# If no target is specified, a random location (where it is possible to construct the building) is chosen, with one exception: If a building can be converted (base_cost_conversion > 0), no specified target means to convert instead of constructing a new building. If no valid location is found, then the strategy is ignored.
	# If the specified building is already being constructed in the target location (or anywhere if no target is specified), then the strategy will be ignored.

	value = 200  # AI weight, used for weighted random selection of what to build. The AI gathers all build_building strategies (including the ones created dynamically) with non-zero values, and selects one of them.
}
```

### `building_target`
Makes the AI try to reach at least this number of the specified building type
```
ai_strategy = {
	type = building_target
	id = industrial_complex
	value = 85  # Prioritize civilian factories until we have at least 85
}
```

### `equipment_production_factor`
Modifies the number of factories the AI wants to allocate to production of a certain equipment category (see script_enum_equipment_category in "common\script_enums.txt" for available options)
```
ai_strategy = {
	type = equipment_production_factor
	id = tactical_bomber  # equipment categories
	value = 50  # Increase the perceived needed factories by 50 % (10 needed factories would become 15)
}
```

### `equipment_production_surplus_management`
Controls what the AI produces when all their needs are already met (and it therefore doesn't need/want anymore)
```
ai_strategy = {
	type = equipment_production_surplus_management
	id = infantry_equipment  # equipment types (doesn't have to be archetypes, can also specify e.g. infantry_equipment_2)
	value = 10  # Weighed against the values of other equipment types to determine ratio of factories IF all "normal" equipment needs are already fulfilled. Be aware that very high values may interfere with the normal calculations for equipment needs.
}
```

### `equipment_production_min_factories`
Forces the AI to allocate this many factories to production of equipment belonging to this category (as defined by *"type = ..."* in the equipment database). Use with caution since it doesn't take into account how many factories are actually available.
```
ai_strategy = {
	type = equipment_production_min_factories
	id = motorized # This will include both trucks and armored cars
	value = 3  # The AI will put at least 3 factories on producing any equipment of the 'motorized' type
}
```

### `equipment_production_min_factories_archetype`
Forces the AI to allocate this many factories to production of equipment belonging to this specific archetype. This can be used if you want to be more selective than *equipment_production_min_factories*. Use with caution since it doesn't take into account how many factories are actually available.
```
ai_strategy = {
	type = equipment_production_min_factories
	id = motorized_equipment # This will include trucks but not armored cars
	value = 3  # The AI will put at least 3 factories on producing equipment using the 'motorized_equipment' archetype
}
```

### `equipment_market_spend_factories`
Modifies max nr of civilian factories the AI wants to spend on purchasing equipment
```
ai_strategy = {
	type = equipment_market_spend_factories
	value = 20  # Factor for the EQUIPMENT_MARKET_MAX_CIVS_FOR_PURCHASES_RATIO define (value = 20 results in a factor of 1.2)
}
```

### `equipment_market_for_sale_threshold`
The AI needs a surplus of this many units of the equipment type before considering it a surplus to sell on the equipment market
```
ai_strategy = {
	type = equipment_market_for_sale_threshold
	id = train
	value = 200  # Absolute number of units
}
```

### `equipment_market_for_sale_factor`
Modifies the ratio of equipment surplus to put up for sale on the market
```
ai_strategy = {
	type = equipment_market_for_sale_factor
	id = train
	value = 50  # Factor for the EQUIPMENT_MARKET_BASE_MARKET_RATIO define (value = 50 results in a factor of 1.5)
}
```

### `equipment_market_max_for_sale`
Limits how many units of the equipment type will be put up on the market
```
ai_strategy = {
	type = equipment_market_max_for_sale
	id = train
	value = 30  # The AI will put up max 30 units for sale (a value of 0 is ignored, use the other strategies to prevent the AI from selling instead)
}
```

### `equipment_market_min_for_sale`
The AI will use this as a lower limit of how many units to put up for sale, and it will keep the equipment on the market as multiples of this value. Overrides the EQUIPMENT_MARKET_DEFAULT_CIC_CHUNK_FOR_SALE define.
```
ai_strategy = {
	type = equipment_market_min_for_sale
	id = train
	value = 20  # The AI will put minimum this nr of the equipment on the market
}
```

### `equipment_market_buying_threshold`
Affects the AI's perceived archetype needs regarding equipment purchases on the market. A value of 50 means it will try to buy 50 more of the equipment than what is actually needed, while a value of -20 means it will only try to buy if it has a deficit larger than 20.
```
ai_strategy = {
	type = equipment_market_buying_threshold
	id = small_plane_cas_airframe  # equipment archetype
	value = 100  # Absolute number of units
}
```

### `equipment_market_buy`
This affects how the AI scores the available equipment to buy. Must specify either equipment_type or seller or both.
```
ai_strategy = {
	type = equipment_market_buy
	equipment_type = light_tank_chassis  # optional: equipment type or archetype to buy
	seller = GER  # optional: which country to buy from. Can be scoped variable.
	value = 200  # Part of the score calculation for things to buy. Related define: EQUIPMENT_MARKET_SCORE_FACTOR_AI_STRAT_WEIGHT
}
```

### `equipment_market_trade_desire`
Increases (or decreases if negative) the desire to trade with a certain country. Affects acceptance for purchase requests and acceptance+desire for market access.
```
ai_strategy = {
	type = equipment_market_trade_desire
	id = ENG  # desired trade partner
	value = 30  # Increases the acceptance and desire values by this
}
```

### `research_tech`
Forces AI to research a specific technology as soon as possible
```
ai_strategy = {
	type = research_tech
	id = radio_detection
	value = 100  # Value doesn't really matter as long as its positive. The AI should be forced to research the specified technology ASAP (if able).
}
```

### `research_weight_factor`
Factor for the AI weight (score) of a specific technology
```
ai_strategy = {
	type = research_weight_factor
	id = radio_detection
	value = 100  # Factor the ai_will_do value for the specified technology with this. (50 means 50 % increase, -30 means 30 % decrease, etc)
}
```

### `unit_ratio`
When AI produces equipment, the unit ratio determines how much it wants of that equipment type compared to other equipment types
```
ai_strategy = {
	type = unit_ratio
	id = naval_bomber
	value = 15  # Increase the ratio of naval bombers with 15 % (compared to other plane types)
}
```

### `land_xp_spend_priority`, `air_xp_spend_priority` and `navy_xp_spend_priority`

Used for changing the desire of the AI to spend XP on specific actions within the land, air or navy category.
The *id* specifies which action we want to modify. The following tokens are valid:

* `division_template` - update a division template
* `unlock_doctrine` - unlock doctrines
* `equipment_variant` - upgrading equipment
* `upgrade_xp_cutoff` - XP cutoff for creating equipment variants with the legacy upgrade system (not a desire per se)
* `army_spirit` / `air_spirit` / `navy_spirit` - unlock spirits (needs to match the category of the *type*)

Example:
```
ai_strategy = {
    type = land_xp_spend_priority
    id = division_template
    value = 100
}
```

### `strategic_air_importance`
Affects the AI priority regarding air superiority/combat
```
ai_strategy = {
	type = strategic_air_importance
	id = 1  # Strategic Region ID - Southern England
	value = 10000  # Value of stocked main front in active combat is usually around 35,000
}
```

### `raid_target_country`
Used to make the AI more or less likely to target a specific country with raids
```
ai_strategy = {
	type = raid_target_country
	id = GER # The target country
	value = 200  # Defines how the probability is affected. 200 means +200 %, -50 means -50 %
}
```
