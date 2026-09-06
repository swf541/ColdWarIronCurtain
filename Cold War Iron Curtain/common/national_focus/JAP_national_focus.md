#PLZ DO NOT DELETE THIS FILE. - FROM TAIGA
#PLZ DO NOT DELETE THIS FILE. - FROM TAIGA
#PLZ DO NOT DELETE THIS FILE. - FROM TAIGA

focus_tree = {
	id = Japan_historical_focus_tree
	country = {
		factor = 0
		modifier = {
			add = 10
			tag = JAP
		}
	}
	default = no
	
	#Korean War Branch
	focus = {
		id = JAP_the_korean_war
		icon = GFX_JAP_Korean_War
		cost = 0
		x = 7
		y = 0
		available = {
			always = no
		}
		allow_branch = { has_country_flag = JAP_Korean_War }
		completion_reward = {
			custom_effect_tooltip = JAP_autocomplete_focus_tt
			hidden_effect = {
                country_event = {
                    id = japan.17
                    days = 10
                    random_hours = 12
                    random_days = 5
                }
            }
		}
	}

	focus = {
		id = JAP_encourage_foreign_investments
		icon = GFX_Generic_National_Focus_Economics_22
		cost = 2
		x = -4
		y = 1
		completion_reward = {
			add_timed_idea = {
				idea = JAP_Foriegn_Economic_Investments
				days = 1000
			}
			JAP_Decrease_Dodge_Line = yes
			hidden_effect = {
				set_variable = { THIS.idea_len_@token:JAP_Foriegn_Economic_Investments = 1000 }
				set_variable = { THIS.idea_date_@token:JAP_Foriegn_Economic_Investments = global.num_days }
			}
		}
		relative_position_id = JAP_the_korean_war
		prerequisite = { focus = JAP_the_korean_war }
	}

	focus = {
		id = JAP_modernise_manufacturies_for_exports
		icon = GFX_Generic_National_Focus_Trading_13
		cost = 2
		x = -2
		y = 1
		completion_reward = {
			add_tech_bonus = {
				bonus = 1
				uses = 1
				category = industry
			}
			random_owned_controlled_state = {
				add_extra_state_shared_building_slots = 1
				add_building_construction = {
					type = industrial_complex
					level = 1
					instant_build = yes
				}
				JAP_Decrease_Dodge_Line = yes
			}
		}
		relative_position_id = JAP_the_korean_war
		prerequisite = { focus = JAP_the_korean_war }
	}

	focus = {
		id = JAP_decrease_rationing
		icon = GFX_Generic_National_Focus_Economics_5
		cost = 2
		x = 1
		y = 1
		completion_reward = {
			custom_effect_tooltip = JAP_Leftist_Unrest_02_decrease_tt
			remove_mission = JAP_Decrease_Rationing_Decision
			JAP_Decrease_Dodge_Line = yes
			hidden_effect = {
				JAP_Leftist_Unrest_02_decrease = yes
			}
		}
		relative_position_id = JAP_encourage_foreign_investments
		prerequisite = { focus = JAP_encourage_foreign_investments }
		prerequisite = { focus = JAP_modernise_manufacturies_for_exports }
	}

	focus = {
		id = JAP_unrestrained_industrial_growth
		icon = GFX_JAP_Generic_National_Focus_Production_16
		cost = 2
		x = 4
		y = 1
		completion_reward = {
			random_owned_controlled_state = {
				add_extra_state_shared_building_slots = 1
				add_building_construction = {
					type = industrial_complex
					level = 1
					instant_build = yes
				}
			}
			random_owned_controlled_state = {
				add_extra_state_shared_building_slots = 1
				add_building_construction = {
					type = industrial_complex
					level = 1
					instant_build = yes
				}
			}
			JAP_Decrease_Dodge_Line = yes
		}
		relative_position_id = JAP_encourage_foreign_investments
		prerequisite = { focus = JAP_encourage_foreign_investments }
		prerequisite = { focus = JAP_modernise_manufacturies_for_exports }
	}

	focus = {
		id = JAP_growth_in_entrepreneurs
		icon = GFX_JAP_growth_in_entrepreneurs
		cost = 2
		x = -2
		y = 1
		completion_reward = {
			random_owned_controlled_state = {
				add_extra_state_shared_building_slots = 1
				add_building_construction = {
					type = office_park
					level = 1
					instant_build = yes
				}
			}
			random_owned_controlled_state = {
				add_extra_state_shared_building_slots = 1
				add_building_construction = {
					type = office_park
					level = 1
					instant_build = yes
				}
			}
			JAP_Decrease_Dodge_Line = yes
		}
		relative_position_id = JAP_encourage_foreign_investments
		prerequisite = { focus = JAP_encourage_foreign_investments }
		prerequisite = { focus = JAP_modernise_manufacturies_for_exports }
	}

	focus = {
		id = JAP_relax_export_regulations
		icon = GFX_Generic_National_Focus_Trading_1
		cost = 2
		x = 0
		y = 1
		completion_reward = {
			random_owned_controlled_state = {
				add_extra_state_shared_building_slots = 1
				add_building_construction = {
					type = industrial_complex
					level = 1
					instant_build = yes
				}
			}
			random_owned_controlled_state = {
				add_extra_state_shared_building_slots = 1
				add_building_construction = {
					type = office_park
					level = 1
					instant_build = yes
				}
			}
			add_timed_idea = {
				idea = embrace_free_trade
				days = 730
			}
			hidden_effect = {
				set_variable = { THIS.idea_len_@token:embrace_free_trade = 730 }
				set_variable = { THIS.idea_date_@token:embrace_free_trade = global.num_days }
			}
		}
		relative_position_id = JAP_decrease_rationing
		prerequisite = { focus = JAP_decrease_rationing }
		prerequisite = { focus = JAP_unrestrained_industrial_growth }
		prerequisite = { focus = JAP_growth_in_entrepreneurs }
	}

	focus = {
		id = JAP_macarthurs_letter
		icon = GFX_JAP_McArthurs_Letter
		cost = 0
		x = 5
		y = 1
		available = {
			always = no
		}
		completion_reward = {
			custom_effect_tooltip = JAP_autocomplete_focus_tt
		}
		relative_position_id = JAP_the_korean_war
		prerequisite = { focus = JAP_the_korean_war }
    }

	focus = {
		id = JAP_establish_the_national_police_reserve
		icon = GFX_JAP_national_police_reserve2
		cost = 2
		x = -2
		y = 1
		completion_reward = {
			army_experience = 30
			custom_effect_tooltip = JAP_establish_the_national_police_reserve_tt
			country_event = { id = japan.12 }
			JAP_Decrease_Japanese_Pacifism = yes
			hidden_effect = {
				load_oob = "JAP_npr_deployment"
			}
		}
		relative_position_id = JAP_macarthurs_letter
		prerequisite = { focus = JAP_macarthurs_letter }
	}

	focus = {
		id = JAP_establish_the_coastal_safety_force
		icon = GFX_JAP_establish_the_coastal_safety_force
		cost = 2
		x = 2
		y = 1
		completion_reward = {
			navy_experience = 30
			custom_effect_tooltip = JAP_establish_the_coastal_safety_force_tt
			country_event = { id = japan.13 }
			JAP_Decrease_Japanese_Pacifism = yes
		}
		relative_position_id = JAP_macarthurs_letter
		prerequisite = { focus = JAP_macarthurs_letter }
	}

	focus = {
		id = JAP_formation_of_the_national_safety_agency
		icon = GFX_JAP_Form_The_National_Safety_Agency
		cost = 2
		x = 2
		y = 1
		completion_reward = {
			custom_effect_tooltip = JAP_formation_of_the_national_safety_agency_tt
			army_experience = 15
			navy_experience = 15
			country_event = { id = japan.16 }
			JAP_Decrease_Japanese_Pacifism = yes
			hidden_effect = {
				load_oob = "JAP_nsf_deployment"
			}
        }
        relative_position_id = JAP_establish_the_national_police_reserve
        prerequisite = { focus = JAP_establish_the_national_police_reserve }
        prerequisite = { focus = JAP_establish_the_coastal_safety_force }
    }

	focus = {
		id = JAP_selfdefense_forces_act
		icon = GFX_JAP_selfdefense_forces_act
		cost = 2
		x = 0
		y = 1
		completion_reward = {
			news_event = { id = japan.15 }
			set_country_flag = JAP_establish_the_jsdf
			JAP_Decrease_Japanese_Pacifism = yes
		}
		relative_position_id = JAP_formation_of_the_national_safety_agency
		prerequisite = { focus = JAP_formation_of_the_national_safety_agency }
	}
	
	#Military Branch
	focus = {
		id = JAP_establish_the_jsdf
		icon = GFX_JAP_Establish_The_JSDF
		cost = 0
		x = 20
		y = 13
		available = {
			always = no
		}
		allow_branch = { has_country_flag = JAP_establish_the_jsdf }
		completion_reward = {
			custom_effect_tooltip = JAP_autocomplete_focus_tt
			news_event = { id = japan.1 }
		}
	}

	focus = {
		id = JAP_japan_air_self_defense_force
		icon = GFX_Japan_Air_Self_Defense_Force
		cost = 2
		x = -10
		y = 1
		completion_reward = {
			air_experience = 50
		}
		relative_position_id = JAP_establish_the_jsdf
		prerequisite = { focus = JAP_establish_the_jsdf }
	}

	focus = {
		id = JAP_japan_ground_self_defense_force
		icon = GFX_Japan_Ground_Self_Defense_Force
		cost = 2
		x = 9
		y = 1
		completion_reward = {
			army_experience = 50
		}
		relative_position_id = JAP_establish_the_jsdf
		prerequisite = { focus = JAP_establish_the_jsdf }
	}

	focus = {
		id = JAP_japan_maritime_self_defense_force
		icon = GFX_Japan_Maritime_Self-Defense_Force
		cost = 2
		x = 19
		y = 1
		completion_reward = {
			navy_experience = 50
		}
		relative_position_id = JAP_establish_the_jsdf
		prerequisite = { focus = JAP_establish_the_jsdf }
	}

	focus = {
		id = JAP_rehabilitate_former_military_officers
		icon = GFX_generic_suspend_constitution
		cost = 2
		x = 5
		y = 1
		completion_reward = {
			custom_effect_tooltip = JAP_rehabilitate_former_military_officers_tt
		}
		relative_position_id = JAP_japan_ground_self_defense_force
		prerequisite = { focus = JAP_japan_ground_self_defense_force }
		prerequisite = { focus = JAP_japan_maritime_self_defense_force }
	}

	focus = {
		id = JAP_kaikokai_and_suikokai_foundations
		icon = GFX_generic_suspend_constitution
		cost = 2
		x = 0
		y = 1
		completion_reward = {
			
		}
		relative_position_id = JAP_rehabilitate_former_military_officers
		prerequisite = { focus = JAP_rehabilitate_former_military_officers }
	}

	focus = {
		id = JAP_purchase_f86_sabres
		icon = GFX_JAP_purchase_f86_sabres
		cost = 2
		x = -2
		y = 1
		available = {
			has_tech = jet_multirole2
		}
		completion_reward = {
			add_equipment_to_stockpile = {
				type = jet_multirole_equipment_2
				amount = 200
			}
		}
		relative_position_id = JAP_japan_air_self_defense_force
		prerequisite = { focus = JAP_japan_air_self_defense_force }
	}

	focus = {
		id = JAP_restore_the_fuchu_airbase
		icon = GFX_JAP_restore_the_fuchu_airbase
		cost = 2
		x = 2
		y = 1
		completion_reward = {
			
		}
		relative_position_id = JAP_japan_air_self_defense_force
		prerequisite = { focus = JAP_japan_air_self_defense_force }
	}

	focus = {
		id = JAP_establish_the_air_selfdefense_flying_school
		icon = GFX_generic_suspend_constitution
		cost = 2
		x = 2
		y = 1
		completion_reward = {
			
		}
		relative_position_id = JAP_purchase_f86_sabres
		prerequisite = { focus = JAP_purchase_f86_sabres }
		prerequisite = { focus = JAP_restore_the_fuchu_airbase }
	}

	focus = {
		id = JAP_joint_operations_with_the_usaf
		icon = GFX_generic_suspend_constitution
		cost = 2
		x = 2
		y = 1
		completion_reward = {
			
		}
		relative_position_id = JAP_restore_the_fuchu_airbase
		prerequisite = { focus = JAP_restore_the_fuchu_airbase }
		prerequisite = { focus = JAP_purchase_f86_sabres }
	}

	focus = {
		id = JAP_the_kyokko
		icon = GFX_generic_suspend_constitution
		cost = 2
		x = -2
		y = 1
		completion_reward = {
			add_tech_bonus = {
				bonus = 0.5
				uses = 1
				category = fighter_multirole
			}
		}
		relative_position_id = JAP_purchase_f86_sabres
		prerequisite = { focus = JAP_purchase_f86_sabres }
		prerequisite = { focus = JAP_restore_the_fuchu_airbase }
	}

	focus = {
		id = JAP_domestic_fighter_production_programme
		icon = GFX_generic_suspend_constitution
		cost = 2
		x = 2
		y = 1
		completion_reward = {
			
		}
		relative_position_id = JAP_the_kyokko
		prerequisite = { focus = JAP_the_kyokko }
		prerequisite = { focus = JAP_establish_the_air_selfdefense_flying_school }
		prerequisite = { focus = JAP_joint_operations_with_the_usaf }
	}

	focus = {
		id = JAP_construct_new_aircraft_accommodation_facilities
		icon = GFX_generic_suspend_constitution
		cost = 2
		x = 2
		y = 1
		completion_reward = {
			log = "[GetDateText]: [Root.GetName]: Focus JAP_construct_new_aircraft_accommodation_facilities"
		}
		relative_position_id = JAP_establish_the_air_selfdefense_flying_school
		prerequisite = { focus = JAP_the_kyokko }
		prerequisite = { focus = JAP_establish_the_air_selfdefense_flying_school }
		prerequisite = { focus = JAP_joint_operations_with_the_usaf }
	}

	focus = {
		id = JAP_formation_of_the_air_defense_command
		icon = GFX_generic_suspend_constitution
		cost = 2
		x = -2
		y = 1
		completion_reward = {
			
		}
		relative_position_id = JAP_construct_new_aircraft_accommodation_facilities
		prerequisite = { focus = JAP_construct_new_aircraft_accommodation_facilities }
		prerequisite = { focus = JAP_domestic_fighter_production_programme }
	}

	focus = {
		id = JAP_reorganise_the_former_npr_units
		icon = GFX_JAP_reorganize_the_former_npr_units
		cost = 2
		x = 0
		y = 1
		completion_reward = {
			
		}
		relative_position_id = JAP_japan_ground_self_defense_force
		prerequisite = { focus = JAP_japan_ground_self_defense_force }
	}

	focus = {
		id = JAP_purchase_american_infantry_equipment
		icon = GFX_generic_suspend_constitution
		cost = 2
		x = -2
		y = 1
		completion_reward = {
			
		}
		relative_position_id = JAP_reorganise_the_former_npr_units
		prerequisite = { focus = JAP_reorganise_the_former_npr_units }
	}

	focus = {
		id = JAP_purchase_american_tanks
		icon = GFX_generic_suspend_constitution
		cost = 2
		x = 2
		y = 1
		completion_reward = {
			
		}
		relative_position_id = JAP_reorganise_the_former_npr_units
		prerequisite = { focus = JAP_reorganise_the_former_npr_units }
	}

	focus = {
		id = JAP_formation_of_new_ground_units
		icon = GFX_generic_suspend_constitution
		cost = 2
		x = 2
		y = 1
		completion_reward = {
			
		}
		relative_position_id = JAP_purchase_american_infantry_equipment
		prerequisite = { focus = JAP_purchase_american_infantry_equipment }
		prerequisite = { focus = JAP_purchase_american_tanks }
	}

	focus = {
		id = JAP_plans_for_a_domestic_mbt
		icon = GFX_JAP_Develop_MBT
		cost = 2
		x = 0
		y = 1
		completion_reward = {
			
		}
		relative_position_id = JAP_formation_of_new_ground_units
		prerequisite = { focus = JAP_formation_of_new_ground_units }
	}

	focus = {
		id = JAP_facilitate_the_mobile_divisions
		icon = GFX_generic_suspend_constitution
		cost = 2
		x = -4
		y = 1
		completion_reward = {
			
		}
		relative_position_id = JAP_formation_of_new_ground_units
		prerequisite = { focus = JAP_formation_of_new_ground_units }
	}

	focus = {
		id = JAP_mechanised_equipment_production
		icon = GFX_generic_suspend_constitution
		cost = 2
		x = 4
		y = 1
		completion_reward = {
			
		}
		relative_position_id = JAP_formation_of_new_ground_units
		prerequisite = { focus = JAP_formation_of_new_ground_units }
	}

	focus = {
		id = JAP_invest_in_helicopter_production
		icon = GFX_generic_suspend_constitution
		cost = 2
		x = -2
		y = 1
		completion_reward = {
			
		}
		relative_position_id = JAP_plans_for_a_domestic_mbt
		prerequisite = { focus = JAP_plans_for_a_domestic_mbt }
		prerequisite = { focus = JAP_facilitate_the_mobile_divisions }
		prerequisite = { focus = JAP_mechanised_equipment_production }
	}

	focus = {
		id = JAP_acquire_artillery_equipment
		icon = GFX_generic_suspend_constitution
		cost = 2
		x = 2
		y = 1
		completion_reward = {
			
		}
		relative_position_id = JAP_plans_for_a_domestic_mbt
		prerequisite = { focus = JAP_plans_for_a_domestic_mbt }
		prerequisite = { focus = JAP_mechanised_equipment_production }
		prerequisite = { focus = JAP_facilitate_the_mobile_divisions }
	}

	focus = {
		id = JAP_missile_technology_modernisation
		icon = GFX_generic_suspend_constitution
		cost = 2
		x = 2
		y = 1
		completion_reward = {
			
		}
		relative_position_id = JAP_invest_in_helicopter_production
		prerequisite = { focus = JAP_invest_in_helicopter_production }
		prerequisite = { focus = JAP_acquire_artillery_equipment }
	}

	focus = {
		id = JAP_rebuilding_the_fleet
		icon = GFX_generic_suspend_constitution
		cost = 2
		x = 0
		y = 1
		completion_reward = {
			
		}
		relative_position_id = JAP_japan_maritime_self_defense_force
		prerequisite = { focus = JAP_japan_maritime_self_defense_force }
	}

	focus = {
		id = JAP_acquire_decomissioned_american_ships
		icon = GFX_generic_suspend_constitution
		cost = 2
		x = 2
		y = 1
		completion_reward = {
			
		}
		relative_position_id = JAP_rebuilding_the_fleet
		prerequisite = { focus = JAP_rebuilding_the_fleet }
	}

	focus = {
		id = JAP_reuse_the_surviving_naval_arsenal_assets
		icon = GFX_generic_suspend_constitution
		cost = 2
		x = -2
		y = 1
		completion_reward = {
			
		}
		relative_position_id = JAP_rebuilding_the_fleet
		prerequisite = { focus = JAP_rebuilding_the_fleet }
	}

	focus = {
		id = JAP_a_patrolfocused_fleet
		icon = GFX_generic_suspend_constitution
		cost = 2
		x = -2
		y = 1
		completion_reward = {
			
		}
		relative_position_id = JAP_acquire_decomissioned_american_ships
		prerequisite = { focus = JAP_acquire_decomissioned_american_ships }
		prerequisite = { focus = JAP_reuse_the_surviving_naval_arsenal_assets }
	}

	focus = {
		id = JAP_invest_in_submarines
		icon = GFX_generic_suspend_constitution
		cost = 2
		x = -2
		y = 1
		completion_reward = {
			
		}
		relative_position_id = JAP_a_patrolfocused_fleet
		prerequisite = { focus = JAP_a_patrolfocused_fleet }
	}

	focus = {
		id = JAP_purchase_p2v_neptunes
		icon = GFX_generic_suspend_constitution
		cost = 2
		x = 2
		y = 1
		completion_reward = {
			
		}
		relative_position_id = JAP_a_patrolfocused_fleet
		prerequisite = { focus = JAP_a_patrolfocused_fleet }
	}

	focus = {
		id = JAP_the_cvh_proposal
		icon = GFX_generic_suspend_constitution
		cost = 2
		x = 2
		y = 1
		completion_reward = {
			
		}
		relative_position_id = JAP_invest_in_submarines
		prerequisite = { focus = JAP_invest_in_submarines }
		prerequisite = { focus = JAP_purchase_p2v_neptunes }
	}

	focus = {
		id = JAP_first_defense_buildup_plan
		icon = GFX_generic_suspend_constitution
		cost = 2
		x = 10
		y = 1
		completion_reward = {
			
		}
		relative_position_id = JAP_japan_air_self_defense_force
		prerequisite = { focus = JAP_japan_air_self_defense_force }
		prerequisite = { focus = JAP_japan_ground_self_defense_force }
		prerequisite = { focus = JAP_japan_maritime_self_defense_force }
	}

	focus = {
		id = JAP_establish_the_national_defense_academy
		icon = GFX_generic_suspend_constitution
		cost = 2
		x = 4
		y = 1
		completion_reward = {
			
		}
		relative_position_id = JAP_first_defense_buildup_plan
		prerequisite = { focus = JAP_first_defense_buildup_plan }
	}

	focus = {
		id = JAP_technical_research_and_development_institute
		icon = GFX_generic_suspend_constitution
		cost = 2
		x = -4
		y = 1
		completion_reward = {
			
		}
		relative_position_id = JAP_first_defense_buildup_plan
		prerequisite = { focus = JAP_first_defense_buildup_plan }
	}

	focus = {
		id = JAP_readjust_the_military_budget
		icon = GFX_generic_suspend_constitution
		cost = 2
		x = 0
		y = 1
		completion_reward = {
			
		}
		relative_position_id = JAP_first_defense_buildup_plan
		prerequisite = { focus = JAP_first_defense_buildup_plan }
	}

	focus = {
		id = JAP_national_defense_basic_policy
		icon = GFX_generic_suspend_constitution
		cost = 2
		x = 2
		y = 1
		completion_reward = {
			
		}
		relative_position_id = JAP_technical_research_and_development_institute
		prerequisite = { focus = JAP_technical_research_and_development_institute }
		prerequisite = { focus = JAP_readjust_the_military_budget }
		prerequisite = { focus = JAP_establish_the_national_defense_academy }
	}

	focus = {
		id = JAP_utilise_the_heavy_industries_for_military_production
		icon = GFX_generic_suspend_constitution
		cost = 2
		x = 2
		y = 1
		completion_reward = {
			
		}
		relative_position_id = JAP_readjust_the_military_budget
		prerequisite = { focus = JAP_technical_research_and_development_institute }
		prerequisite = { focus = JAP_readjust_the_military_budget }
		prerequisite = { focus = JAP_establish_the_national_defense_academy }
	}

	focus = {
		id = JAP_the_constitutional_validity_question
		icon = GFX_generic_suspend_constitution
		cost = 2
		x = 2
		y = 1
		completion_reward = {
			
		}
		relative_position_id = JAP_national_defense_basic_policy
		prerequisite = { focus = JAP_national_defense_basic_policy }
		prerequisite = { focus = JAP_utilise_the_heavy_industries_for_military_production }
	}
	
	#Economy Branch
	focus = {
		id = JAP_Rise_from_the_Ashes
		icon = GFX_Rise_from_the_ashes
		cost = 10.00
		x = 46
		y = 0
		#allow_branch = { NOT = { has_country_flag = JAP_Ikeda_Hayato_Prime_Minister } }
		completion_reward = {
			add_stability = 0.1
			add_ideas = a_new_japan
		}
	}
	focus = {
		id = JAP_The_Government_Housing_Loan_Corporation_Law
		icon = GFX_goal_unknown
		cost = 10.00
		x = 44
		y = 1
		prerequisite = {
			focus = JAP_Rise_from_the_Ashes
		}
		completion_reward = {
			add_timed_idea = {
				idea = JAP_Urban_Planning
				days = 530
			}
		}
	}
	focus = {
		id = JAP_The_Japanese_Economic_Miracle
		icon = GFX_goal_unknown
		cost = 10.00
		x = 46
		y = 5
		available = {
			has_completed_focus = JAP_A_Post_Reconstruction_Economy
			has_completed_focus = JAP_The_Reverse_Course
			has_completed_focus = JAP_Law_for_the_Reconstruction_of_Agricultural_Finances
		}
		allow_branch = { has_country_flag = Is_this_for_what }
		completion_reward = {
			JAP = { news_event = japan.2 }
			add_ideas = JAP_Economic_Miracle
		}
	}
	focus = {
		id = JAP_Formation_of_Keiretsus
		icon = GFX_goal_unknown
		cost = 10.00
		prerequisite = {
			focus = JAP_Rise_from_the_Ashes
		}
		x = 41
		y = 1
		completion_reward = {
			add_timed_idea = {
				idea = Extensive_American_Economic_Aid
				days = 365
			}
			JAP = {
				add_opinion_modifier = {
					target = USA
					modifier = gave_economic_aid
				}
			}
		}
	}
	focus = {
		id = JAP_Reform_the_Yen
		icon = GFX_goal_unknown
		cost = 10.00
		prerequisite = {
			focus = JAP_Formation_of_Keiretsus
		}
		x = 40
		y = 2
		completion_reward = {
			add_timed_idea = {
				idea = JAP_Currency_Reform
				days = 365
			}
		}
	}
	focus = {
		id = JAP_Restore_Agricultural_Output
		icon = GFX_goal_unknown
		cost = 10.00
		prerequisite = {
			focus = JAP_Formation_of_Keiretsus
		}
		prerequisite = {
			focus = JAP_The_Government_Housing_Loan_Corporation_Law
		}
		x = 43
		y = 2
		completion_reward = {
			random_owned_state = {
				add_extra_state_shared_building_slots = 2
				add_building_construction = {
					type = water_infrastructure
					level = 1
					instant_build = yes
				}
				add_building_construction = {
					type = agri_industrial_complex
					level = 1
					instant_build = yes
				}
			}
			random_owned_state = {
				add_extra_state_shared_building_slots = 2
				add_building_construction = {
					type = water_infrastructure
					level = 1
					instant_build = yes
				}
				add_building_construction = {
					type = agri_industrial_complex
					level = 1
					instant_build = yes
				}
			}
		}
		
	}
	focus = {
		id = JAP_An_End_to_HyperInflation_and_Food_Shortages
		icon = GFX_goal_unknown
		cost = 10.00
		prerequisite = {
			focus = JAP_Restore_Agricultural_Output
		}
		prerequisite = {
			focus = JAP_Reform_the_Yen
		}
		x = 42
		y = 3
		completion_reward = {
		}
	}
	focus = {
		id = JAP_Announce_A_New_Long_Term_Economic_Plan
		icon = GFX_goal_unknown
		cost = 10.00
		prerequisite = {
			focus = JAP_The_Japanese_Economic_Miracle
		}
		x = 46
		y = 6
		completion_reward = {
			add_timed_idea = {
				idea = governmental_planning_and_management
				days = 365
			}
		}
	}
	focus = {
		id = JAP_Great_Showa_Consolidation
		icon = GFX_JAP_Great_Showa_Consolidation
		cost = 10.00
		prerequisite = {
			focus = JAP_Announce_A_New_Long_Term_Economic_Plan
		}
		x = 43
		y = 7
		completion_reward = {
			JAP = {
				news_event = japan.3 
			}
			add_ideas = JAP_Great_Showa_Consolidation
			every_owned_state = {
				add_extra_state_shared_building_slots = 2
			}
		}
	}
	focus = {
		id = JAP_Japan_Highway_Public_Corporation_Law
		icon = GFX_goal_unknown
		cost = 10.00
		prerequisite = {
			focus = JAP_Great_Showa_Consolidation
		}
		x = 41
		y = 8
		completion_reward = {

		}
	}
	focus = {
		id = JAP_Five_Year_Plan_for_Road_Development
		icon = GFX_goal_unknown
		cost = 10.00
		prerequisite = {
			focus = JAP_Japan_Highway_Public_Corporation_Law
		}
		x = 41
		y = 9
		completion_reward = {
			add_timed_idea = {
				idea = JAP_Five_Year_Plan_for_Road_Development
				days = 1825
			}
		}
	}
	focus = {
		id = JAP_Subsidise_MITI
		icon = GFX_goal_unknown
		cost = 10.00
		prerequisite = {
			focus = JAP_Rise_from_the_Ashes
		}
		x = 47
		y = 1
		completion_reward = {
			capital_scope = {
				add_extra_state_shared_building_slots = 1
				add_building_construction = {
					type = office_park
					level = 1
					instant_build = yes
				}
			}
			random_owned_controlled_state = {
				add_extra_state_shared_building_slots = 1
				add_building_construction = {
					type = office_park
					level = 1
					instant_build = yes
				}
			}
		}
	}
	focus = {
		id = JAP_Create_the_Development_Bank_of_Japan
		icon = GFX_goal_unknown
		cost = 10.00
		prerequisite = {
			focus = JAP_The_Government_Housing_Loan_Corporation_Law
		}
		prerequisite = {
			focus = JAP_Subsidise_MITI
		}
		x = 45
		y = 2
		completion_reward = {
			add_timed_idea = {
				idea = JAP_Development_Funding
				days = 1825
			}
			capital_scope = {
				add_extra_state_shared_building_slots = 2
				add_building_construction = {
					type = office_park
					level = 2
					instant_build = yes
				}
			}
		}
	}
	focus = {
		id = JAP_The_Inclined_Production_Mode
		icon = GFX_goal_unknown
		cost = 10.00
		prerequisite = {
			focus = JAP_Subsidise_MITI
		}
		x = 48
		y = 2
		completion_reward = {
			add_timed_idea = {
				idea = JAP_The_Inclined_Production_Mode
				days = 730
			}
		}
	}
	focus = {
		id = JAP_Expand_MITIs_Oversight_into_Trade
		icon = GFX_goal_unknown
		cost = 10.00
		prerequisite = {
			focus = JAP_Subsidise_MITI
		}
		x = 51
		y = 2
		completion_reward = {
			add_ideas = embrace_free_trade
		}
	}
	focus = {
		id = JAP_Revitilize_Cotton_Production
		icon = GFX_goal_unknown
		cost = 10.00
		prerequisite = {
			focus = JAP_The_Inclined_Production_Mode
		}
		prerequisite = {
			focus = JAP_Create_the_Development_Bank_of_Japan
		}
		prerequisite = {
			focus = JAP_Expand_MITIs_Oversight_into_Trade
		}
		x = 47
		y = 3
		completion_reward = {
			random_owned_controlled_state = {
				add_extra_state_shared_building_slots = 2
				add_building_construction = {
					type = water_infrastructure
					level = 1
					instant_build = yes
				}
				add_building_construction = {
					type = industrial_complex
					level = 1
					instant_build = yes
				}
			}
		}
	}
	focus = {
		id = JAP_Introduce_The_Fiscal_Investment_and_Loan_Plan
		icon = GFX_goal_unknown
		cost = 10.00
		prerequisite = {
			focus = JAP_Create_the_Development_Bank_of_Japan
		}
		prerequisite = {
			focus = JAP_ThE_Inclined_Production_Mode
		}
		prerequisite = {
			focus = JAP_Expand_MITIs_Oversight_into_Trade
		}
		x = 44
		y = 3
		completion_reward = {
			custom_effect_tooltip = JAP_1000_plus_money_tt
			add_to_variable = {
				currentMoney = 1000
			}
		}
	}
	focus = {
		id = JAP_Slash_Interest_Rates
		icon = GFX_goal_unknown
		cost = 10.00
		prerequisite = {
			focus = JAP_Announce_A_New_Long_Term_Economic_Plan
		}
		x = 46
		y = 7
		completion_reward = {
			add_timed_idea = {
				idea = Slashed_Interest_Rates
				days = 365
			}
		}
	}
	focus = {
		id = JAP_Emphasize_Technological_Development
		icon = GFX_goal_unknown
		cost = 10.00
		prerequisite = {
			focus = JAP_Announce_A_New_Long_Term_Economic_Plan
		}
		x = 49
		y = 7
		completion_reward = {
			add_timed_idea = {
				idea = encourage_scientific_competition
				days = 1825
			}
		}
	}
	focus = {
		id = JAP_National_Pensions_Law
		icon = GFX_goal_unknown
		cost = 10.00
		prerequisite = {
			focus = JAP_Slash_Interest_Rates
		}
		prerequisite = {
			focus = JAP_Emphasize_Technological_Development
		}
		x = 48
		y = 8
		completion_reward = {
			increase_pensions = yes
		}
	}
	focus = {
		id = JAP_Science_and_Technology_Agency_Establishment_Law
		icon = GFX_goal_unknown
		cost = 10.00
		prerequisite = {
			focus = JAP_National_Pensions_Law
		}
		x = 48
		y = 9
		completion_reward = {
			add_research_slot = 1
		}
	}
	focus = {
		id = JAP_Expand_the_Coal_Mines
		icon = GFX_goal_unknown
		cost = 10.00
		prerequisite = {
			focus = JAP_ThE_Inclined_Production_Mode
		}
		prerequisite = {
			focus = JAP_Create_the_Development_Bank_of_Japan
		}
		prerequisite = {
			focus = JAP_Expand_MITIs_Oversight_into_Trade
		}
		x = 50
		y = 3
		completion_reward = {
			add_resource = {
				type = oil
				amount = 5
				state = 536
			}
			add_resource = {
				type = oil
				amount = 3
				state = 528
			}
		}
	}
	focus = {
		id = JAP_Program_for_National_Subsidies_for_School_Facilities
		icon = GFX_goal_unknown
		cost = 10.00
		prerequisite = {
			focus = JAP_Emphasize_Technological_Development
		}
		x = 51
		y = 8
		completion_reward = {
			custom_effect_tooltip = JAP_25_minus_money_tt
			add_ideas = education_reform_2
			add_to_variable = {
				currentMoney = -25
			}			
		}
	}
	focus = {
		id = JAP_Establish_the_Japan_Atomic_Energy_Commission
		icon = GFX_goal_unknown
		cost = 10.00
		prerequisite = {
			focus = JAP_Program_for_National_Subsidies_for_School_Facilities
		}
		x = 51
		y = 9
		completion_reward = {
			add_tech_bonus = {
				name = nuclear_bonus
				bonus = 0.5
				uses = 2
				category = energy
			}
		}
	}
	focus = {
		id = JAP_Minimum_Wage_Law
		icon = GFX_goal_unknown
		cost = 10.00
		prerequisite = {
			focus = JAP_Science_and_Technology_Agency_Establishment_Law
		}
		prerequisite = {
			focus = JAP_Establish_the_Japan_Atomic_Energy_Commission
		}
		x = 49
		y = 10
		completion_reward = {
			add_timed_idea = {
				idea = Wage_Controls
				days = 365
			}
		}
	}
	focus = {
		id = JAP_A_Post_Reconstruction_Economy
		icon = GFX_goal_unknown
		cost = 0
		prerequisite = {
			focus = JAP_An_End_to_HyperInflation_and_Food_Shortages
		}
		prerequisite = {
			focus = JAP_Revitilize_Cotton_Production
		}
		prerequisite = {
			focus = JAP_Expand_the_Coal_Mines
		}
		prerequisite = {
			focus = JAP_Finance_New_Steel_Works
		}
		prerequisite = {
			focus = JAP_Introduce_The_Fiscal_Investment_and_Loan_Plan
		}
		available = {
			has_completed_focus = JAP_Law_for_the_Reconstruction_of_Agricultural_Finances
		}
		x = 46
		y = 4
		completion_reward = {
			remove_ideas = {
				idea_JAP_Reconstruction_begins
				a_new_japan
			}
		}
	}
	focus = {
		id = JAP_Finance_New_Steel_Works
		icon = GFX_goal_unknown
		cost = 10.00
		prerequisite = {
			focus = JAP_ThE_Inclined_Production_Mode
		}
		prerequisite = {
			focus = JAP_Create_the_Development_Bank_of_Japan
		}
		prerequisite = {
			focus = JAP_Expand_MITIs_Oversight_into_Trade
		}
		x = 53
		y = 3
		completion_reward = {
			custom_effect_tooltip = available_designer
			show_ideas_tooltip = Japan_Steel_Works
		}
	}
	focus = {
		id = JAP_The_Electric_Power_Development_Promotion_Law
		icon = GFX_goal_unknown
		cost = 10.00
		prerequisite = {
			focus = JAP_Great_Showa_Consolidation
		}
		prerequisite = {
			focus = JAP_Slash_Interest_Rates
		}
		x = 44
		y = 8
		completion_reward = {
			custom_effect_tooltip = available_designer
			show_ideas_tooltip = TEPCO
			random_owned_controlled_state = {
				add_extra_state_shared_building_slots = 1
				add_building_construction = {
					type = fossil_fuel_powerplant
					level = 1
					instant_build = yes
				}
			}
			random_owned_controlled_state = {
				add_extra_state_shared_building_slots = 1
				add_building_construction = {
					type = fossil_fuel_powerplant
					level = 1
					instant_build = yes
				}
			}
		}
	}
	focus = {
		id = JAP_Further_Strengthen_MITI_In_Accordance_with_Keynesian_Theory
		icon = GFX_goal_unknown
		cost = 10.00
		prerequisite = {
			focus = JAP_Minimum_Wage_Law
		}
		prerequisite = {
			focus = JAP_Ensure_Funding_for_Expanding_Shipyards
		}
		prerequisite = {
			focus = JAP_Loosen_Anti_Monopoly_Laws
		}
		x = 46
		y = 11
		completion_reward = {
			add_timed_idea = {
				idea = JAP_Keynesian_Theory
				days = 365
			}
		}
	}
	focus = {
		id = JAP_Expand_the_Textile_Industry
		icon = GFX_goal_unknown
		cost = 10.00
		prerequisite = {
			focus = JAP_The_Electric_Power_Development_Promotion_Law
		}
		x = 44
		y = 9
		completion_reward = {
			capital_scope = {
				add_extra_state_shared_building_slots = 2
				add_building_construction = {
					type = industrial_complex
					level = 1
					instant_build = yes
				}
				add_building_construction = {
					type = water_infrastructure
					level = 1
					instant_build = yes
				}
			}
		}
	}
	focus = {
		id = JAP_Loosen_Anti_Monopoly_Laws
		icon = GFX_goal_unknown
		cost = 10.00
		prerequisite = {
			focus = JAP_Expand_the_Textile_Industry
		}
		prerequisite = {
			focus = JAP_Five_Year_Plan_for_Road_Development
		}
		x = 43
		y = 10
		completion_reward = {
			add_timed_idea = {
				idea = Economic_Monopolies
				days = 730
			
			}
		}
	}
	focus = {
		id = JAP_Ensure_Funding_for_Expanding_Shipyards
		icon = GFX_goal_unknown
		cost = 10.00
		prerequisite = {
			focus = JAP_Science_and_Technology_Agency_Establishment_Law
		}
		prerequisite = {
			focus = JAP_Expand_the_Textile_Industry
		}
		x = 46
		y = 10
		completion_reward = {
			random_owned_controlled_state = {
				limit = {
					is_coastal = yes
				}
				add_extra_state_shared_building_slots = 2
				add_building_construction = {
					type = dockyard
					level = 2
					instant_build = yes
				}
			}
		}
	}
	
	#Yoshida Branch
	focus = {
		id = JAP_The_Yoshida_Administration
		icon = GFX_JAP_The_Yoshida_Administration
		cost = 10.00
		x = 25
		y = 0
		allow_branch = {
			has_country_flag = JAP_Shigeru_Yoshida_Prime_Minister
		}
		completion_reward = {
			add_political_power = 200
		}
	}
	focus = {
		id = JAP_The_Reverse_Course
		icon = GFX_JAP_The_Reverse_Course
		cost = 10.00
		prerequisite = {
			focus = JAP_The_Yoshida_Administration
		}
		x = 21
		y = 1
		completion_reward = {
			remove_ideas = JAP_American_Industrial_Limitations
			JAP_Decrease_GHQ_Influence = yes
		}
	}
	focus = {
		id = JAP_Form_Democracy_Cells_in_Leftist_Unions
		icon = GFX_JAP_Form_Democracy_Cells_in_Leftist_Unions
		cost = 10.00
		prerequisite = {
			focus = JAP_The_Reverse_Course
		}
		x = 23
		y = 2
		completion_reward = {
			swap_ideas = {
				remove_idea = JAP_Labour_Strikes_2
				add_idea = JAP_Labour_Strikes_1
			}
		}
	}
	focus = {
		id = JAP_Reddo_Paji
		icon = GFX_JAP_Reddo_Paji
		cost = 10.00
		prerequisite = {
			focus = JAP_Form_Democracy_Cells_in_Leftist_Unions
		}
		available = {
			date > 1950.6.1
		}
		x = 23
		y = 3
		completion_reward = {
			custom_effect_tooltip = JAP_Rightist_Equillibrium_5_increase_tt
			custom_effect_tooltip = JAP_Leftist_Unrest_02_decrease_tt
			JAP = { country_event = japan.4 }
			hidden_effect = {
				JAP_Leftist_Unrest_02_decrease = yes
				JAP_Rightist_Equillibrium_5_increase = yes
			}
		}
	}
	focus = {
		id = JAP_Play_Up_the_Communist_Menace_to_SCAP
		icon = GFX_JAP_Play_Up_the_Communist_Menace_to_SCAP
		cost = 10.00
		prerequisite = {
			focus = JAP_The_Yoshida_Administration
		}
		x = 25
		y = 2
		completion_reward = {
			custom_effect_tooltip = JAP_National_Diet_appease_public_2_tt
			custom_effect_tooltip = JAP_domestic_influence_increase_10_tt
			hidden_effect = {
				JAP_National_Diet_appease_public_2 = yes
				add_to_variable = {
					var = domestic_influence_amount
					value = 0.10
				}
			}
		}
	}
	focus = {
		id = JAP_A_Peaceful_Japan
		icon = GFX_JAP_A_Peaceful_Japan
		cost = 10.00
		prerequisite = {
			focus = JAP_Play_Up_the_Communist_Menace_to_SCAP
		}
		x = 25
		y = 4
		completion_reward = {
			remove_ideas = JAP_Legacy_of_the_Atomic_Bombings
		}
	}
	focus = {
		id = JAP_Establish_the_Yoshida_School
		icon = GFX_JAP_Establish_the_Yoshida_School
		cost = 10.00
		prerequisite = {
			focus = JAP_The_Yoshida_Administration
		}
		x = 29
		y = 1
		completion_reward = {
			add_political_power = 100
			custom_effect_tooltip = JAP_National_Diet_cabinet_approval_increase_0_tt
			hidden_effect = {
				JAP_cabinet_approval_increase_0 = yes
			}
		}
	}
	focus = {
		id = JAP_Appoint_Ex_Bureacrats_to_Ministry_Portfolios
		icon = GFX_JAP_Appoint_Ex_Bureacrats_to_Ministry_Portfolios
		cost = 10.00
		prerequisite = {
			focus = JAP_Establish_the_Yoshida_School
		}
		x = 27
		y = 2
		completion_reward = {
			add_stability = 0.05
			custom_effect_tooltip = JAP_National_Diet_cabinet_approval_increase_1_tt
			JAP_Decrease_GHQ_Influence = yes
			hidden_effect = {
				JAP_cabinet_approval_increase_1 = yes
			}
		}
	}
	focus = {
		id = JAP_Reverse_Earlier_Purges
		icon = GFX_JAP_Reverse_Earlier_Purges
		cost = 10.00
		prerequisite = {
			focus = JAP_Appoint_Ex_Bureacrats_to_Ministry_Portfolios
		}
		available = {
			date > 1950.6.1
		}
		x = 27
		y = 3
		completion_reward = {
			add_stability = 0.05
			custom_effect_tooltip = JAP_National_Diet_cabinet_approval_increase_1_tt
			JAP_Decrease_GHQ_Influence = yes
			hidden_effect = {
				JAP_cabinet_approval_increase_1 = yes
			}
		}
	}
	focus = {
		id = JAP_Reorganize_the_Farm_Collectives
		icon = GFX_JAP_Reorganize_the_Farm_Collectives
		cost = 10.00
		prerequisite = {
			focus = JAP_Establish_the_Yoshida_School
		}
		x = 31
		y = 2
		completion_reward = {
			random_owned_state = {
				add_extra_state_shared_building_slots = 1
				add_building_construction = {
					type = agri_industrial_complex
					level = 1
					instant_build = yes
				}
			}
			swap_ideas = {
				remove_idea = JAP_Agricultural_Financial_Crisis_3
				add_idea = JAP_Agricultural_Financial_Crisis_2
			}
		}
	}
	focus = {
		id = JAP_Increase_Rural_Farm_Subsisidies
		icon = GFX_JAP_Increase_Rural_Farm_Subsisidies
		cost = 10.00
		prerequisite = {
			focus = JAP_Reorganize_the_Farm_Collectives
		}
		available = {
			date > 1950.6.1
		}
		x = 31
		y = 3
		completion_reward = {
			random_owned_state = {
				add_extra_state_shared_building_slots = 1
				add_building_construction = {
					type = agri_industrial_complex
					level = 1
					instant_build = yes
				}
			}
			swap_ideas = {
				remove_idea = JAP_Agricultural_Financial_Crisis_2
				add_idea = JAP_Agricultural_Financial_Crisis_1
			}
		}
	}
	focus = {
		id = JAP_Law_for_the_Reconstruction_of_Agricultural_Finances
		icon = GFX_JAP_Law_for_the_Reconstruction_of_Agricultural_Finances
		cost = 10.00
		prerequisite = {
			focus = JAP_Increase_Rural_Farm_Subsisidies
		}
		prerequisite = {
			focus = JAP_Reverse_Earlier_Purges
		}
		x = 29
		y = 4
		completion_reward = {
			remove_ideas = {
				JAP_Agricultural_Financial_Crisis_1
				JAP_Food_Shortages
			}
		}
	}
	focus = {
		id = JAP_Massive_American_Economic_Aid
		icon = GFX_JAP_Massive_American_Economic_Aid
		cost = 10.00
		prerequisite = {
			focus = JAP_The_Reverse_Course
		}
		x = 19
		y = 2
		completion_reward = {
			add_timed_idea = {
				idea = Extensive_American_Economic_Aid
				days = 1000
			}
			JAP = {
				add_opinion_modifier = {
					target = USA
					modifier = gave_economic_aid
				}
			}
			hidden_effect = {
				set_variable = { THIS.idea_len_@token:Extensive_American_Economic_Aid = 1000 }
				set_variable = { THIS.idea_date_@token:Extensive_American_Economic_Aid = global.num_days }
			}
		}
	}
	focus = {
		id = JAP_Amend_the_National_Public_Service_Law
		icon = GFX_JAP_Amend_the_National_Public_Service_Law
		cost = 10.00
		prerequisite = {
			focus = JAP_Massive_American_Economic_Aid
		}
		available = {
			date > 1950.6.1
		}
		x = 19
		y = 3
		completion_reward = {
			remove_ideas = JAP_Politicised_Civil_Service
		}
	}
	focus = { 
		id = JAP_Question_Japan_s_Sovereignity
		icon = GFX_JAP_Question_Japan_s_Sovereignity
		cost = 10.00
		prerequisite = {
			focus = JAP_Reddo_Paji
		}
		prerequisite = {
			focus = JAP_Amend_the_National_Public_Service_Law
		}
		x = 21
		y = 4
		completion_reward = {
			swap_ideas = {
				remove_idea = JAP_American_Intervention_in_Domestic_Politics_2
				add_idea = JAP_American_Intervention_in_Domestic_Politics_1
			}
			JAP_Decrease_GHQ_Influence = yes
		}
	}
	focus = {
		id = JAP_The_Treaty_of_San_Francisco_and_Mutual_Security_Treaty
		icon = GFX_JAP_The_Treaty_of_San_Francisco_and_Mutual_Security_Treaty
		cost = 0
		prerequisite = {
			focus = JAP_A_Peaceful_Japan
		}
		prerequisite = {
			focus = JAP_Question_Japan_s_Sovereignity
		}
		prerequisite = {
			focus = JAP_Law_for_the_Reconstruction_of_Agricultural_Finances
		}
		x = 25
		y = 5
		available = {
			always = no
		}
		completion_reward = {
			custom_effect_tooltip = JAP_autocomplete_focus_tt
			JAP_Decrease_GHQ_Influence = yes
		}
	}
	focus = {
		id = JAP_Regulate_Coal_and_Utility_Strikes
		icon = GFX_JAP_Regulate_Coal_and_Utility_Strikes
		cost = 10.00
		prerequisite = {
			focus = JAP_The_Treaty_of_San_Francisco_and_Mutual_Security_Treaty
		}
		available = {
			has_completed_focus = JAP_A_Peaceful_Japan
			has_completed_focus = JAP_Question_Japan_s_Sovereignity
			has_completed_focus = JAP_Law_for_the_Reconstruction_of_Agricultural_Finances
		}
		x = 26
		y = 6
		completion_reward = {
			remove_ideas = JAP_Labour_Strikes_1
		}
	}
	focus = {
		id = JAP_Welfare_Pension_Insurance_Law
		icon = GFX_healthcare
		cost = 10.00
		prerequisite = {
			focus = JAP_The_Treaty_of_San_Francisco_and_Mutual_Security_Treaty
		}
		available = {
			has_completed_focus = JAP_A_Peaceful_Japan
			has_completed_focus = JAP_Question_Japan_s_Sovereignity
			has_completed_focus = JAP_Law_for_the_Reconstruction_of_Agricultural_Finances
		}
		x = 24
		y = 6
		completion_reward = {
		}
	}
	focus = {
		id = JAP_The_Subversive_Activities_Prevention_Act
		icon = GFX_JAP_The_Subversive_Activities_Prevention_Act
		cost = 10.00
		prerequisite = {
			focus = JAP_Welfare_Pension_Insurance_Law
		}
		prerequisite = {
			focus = JAP_Regulate_Coal_and_Utility_Strikes
		}
		available = {
			date > 1952.7.1
		}
		x = 22
		y = 7
		completion_reward = {
			custom_effect_tooltip = JAP_Remove_Unrest_Issue_Kyosanto_Militants_tt
			custom_effect_tooltip = JAP_Leftist_Unrest_05_decrease_tt
			country_event = {
				id = jap_yoshida.4
			}
			hidden_effect = {
				JAP_Leftist_Unrest_05_decrease = yes
				remove_from_array = { JAP_National_Radicalism_Issues = 3 }
			}
		}
	}
	focus = {
		id = JAP_Kimura_Proposal 
		icon = GFX_JAP_Kimura_Proposal
		cost = 10.00
		prerequisite = {
			focus = JAP_Welfare_Pension_Insurance_Law
		}
		prerequisite = {
			focus = JAP_Regulate_Coal_and_Utility_Strikes
		}
		available = {
			date > 1952.7.1
		}
		x = 25
		y = 7
		completion_reward = {
			country_event = {
				id = jap_yoshida.3
			}
		}
	}
	focus = {
		id = JAP_The_Farm_Land_Law
		icon = GFX_JAP_The_Farm_Land_Law
		cost = 10.00
		prerequisite = {
			focus = JAP_Welfare_Pension_Insurance_Law
		}
		prerequisite = {
			focus = JAP_Regulate_Coal_and_Utility_Strikes
		}
		available = {
			date > 1952.7.1
		}
		x = 28
		y = 7
		completion_reward = {
			add_timed_idea = {
				idea = New_Land_Reform_Initiative
				days = 1000
			}
			hidden_effect = {
				set_variable = { THIS.idea_len_@token:New_Land_Reform_Initiative = 1000 }
				set_variable = { THIS.idea_date_@token:New_Land_Reform_Initiative = global.num_days }
			}
		}
	}
	focus = {
		id = JAP_Guarantee_Political_Neutrality_of_Compulsory_Schools
		icon = GFX_JAP_Guarantee_Political_Neutrality_of_Compulsory_Schools
		cost = 10.00
		prerequisite = {
			focus = JAP_The_Farm_Land_Law
		}
		prerequisite = {
			focus = JAP_Kimura_Proposal
		}
		prerequisite = {
			focus = JAP_The_Subversive_Activities_Prevention_Act
		}
		x = 27
		y = 8
		completion_reward = {
			custom_effect_tooltip = JAP_National_Diet_appease_public_1_tt
			remove_ideas = JAP_Politicised_Schools
			hidden_effect = {
				JAP_National_Diet_appease_public_1 = yes
			}
		}
	}
	focus = {
		id = JAP_Declare_a_Pro_West_Stance
		icon = GFX_JAP_Declare_a_Pro_West_Stance
		cost = 10.00
		prerequisite = {
			focus = JAP_The_Farm_Land_Law
		}
		prerequisite = {
			focus = JAP_Kimura_Proposal
		}
		prerequisite = {
			focus = JAP_The_Subversive_Activities_Prevention_Act
		}
		x = 25
		y = 8
		completion_reward = {
			add_trait = {
				 character = JAP_shigeru_yoshida
				 ideology = honryu_conservativism
				 trait = american_economic_alignment
			}
		}
	}
	focus = {
		id = JAP_Expand_Compulsory_School_Funding
		icon = GFX_JAP_Expand_Compulsory_School_Funding
		cost = 10.00
		prerequisite = {
			focus = JAP_The_Farm_Land_Law
		}
		prerequisite = {
			focus = JAP_Kimura_Proposal
		}
		prerequisite = {
			focus = JAP_The_Subversive_Activities_Prevention_Act
		}
		x = 23
		y = 8
		completion_reward = {
			
		}
	}
	focus = {
		id = JAP_Offshore_Shipbuilding_Interest_Supply_Law
		icon = GFX_JAP_Offshore_Shipbuilding_Interest_Supply_Law
		cost = 10.00
		prerequisite = {
			focus = JAP_Guarantee_Political_Neutrality_of_Compulsory_Schools
		}
		prerequisite = {
			focus = JAP_Declare_a_Pro_West_Stance
		}
		prerequisite = {
			focus = JAP_Expand_Compulsory_School_Funding
		}
		x = 25
		y = 9
		completion_reward = {
			282 = {
				add_building_construction = {
					type = naval_base
					level = 2
					instant_build = yes
					province = 1182
				}
			}
			1607 = {
				add_building_construction = {
					type = naval_base
					level = 3
					instant_build = yes
					province = 1092
				}
			}
			random_owned_controlled_state = {
				limit = {
					is_coastal = yes
				}
				add_extra_state_shared_building_slots = 1
				add_building_construction = {
					type = dockyard
					level = 1
					instant_build = yes
				}
			}
		}
	}
	focus = {
		id = JAP_The_Police_Law_of_1954
		icon = GFX_JAP_The_Police_Law_of_1954
		cost = 10
		available = {
			date > 1954.6.7
		}
		prerequisite = {
			focus = JAP_Offshore_Shipbuilding_Interest_Supply_Law
		}
		x = 24
		y = 10
		completion_reward = {
			
		}
	}
	focus = {
		id = JAP_Wrap_Up_Rearmament_Debate
		icon = GFX_Dealing_with_the_Recession
		cost = 10.00
		available = {
			date > 1954.6.7
		}
		prerequisite = {
			focus = JAP_Offshore_Shipbuilding_Interest_Supply_Law
		}
		x = 26
		y = 10
		completion_reward = {
			remove_ideas = JAP_Rearmament_Debate
		}
	}
	focus = {
		id = JAP_The_Yoshida_Doctrine
		icon = GFX_JAP_The_Yoshida_Doctrine
		cost = 10.00
		prerequisite = {
			focus = JAP_The_Police_Law_of_1954
		}
		prerequisite = {
			focus = JAP_Wrap_Up_Rearmament_Debate
		}
		x = 25
		y = 11
		completion_reward = {
			add_stability = 0.1
			random_owned_state = {
				add_extra_state_shared_building_slots = 1
				add_building_construction = {
					type = industrial_complex
					level = 1
					instant_build = yes
				}
			}
			random_owned_state = {
				add_extra_state_shared_building_slots = 1
				add_building_construction = {
					type = industrial_complex
					level = 1
					instant_build = yes
				}
			}
		}
	}
	
	#Hatoyama Branch
	focus = {
		id = JAP_The_Hatoyama_Administration
		icon = GFX_goal_unknown
		cost = 10.00
		x = 25
		y = 0
		allow_branch = {
			has_country_flag = JAP_Ichiro_Hatoyama_Prime_Minister
		}
		completion_reward = {
			add_political_power = 200
		}
	}
	
	focus = {
		id = JAP_Metropolitan_Area_Redevelopment_Law
		icon = GFX_goal_unknown
		cost = 10.00
		x = 19
		y = 1
		prerequisite = {
			focus = JAP_The_Hatoyama_Administration
		}
		completion_reward = {
			282 = {
				add_building_construction = {
					type = infrastructure
					level = 1
					instant_build = yes
				}
			}
			1608 = {
				add_building_construction = {
					type = infrastructure
					level = 1
					instant_build = yes
				}
			}
			1599 = {
				add_building_construction = {
					type = infrastructure
					level = 1
					instant_build = yes
				}
			}
			1605 = {
				add_building_construction = {
					type = infrastructure
					level = 1
					instant_build = yes
				}
			}
			1601 = {
				add_building_construction = {
					type = infrastructure
					level = 1
					instant_build = yes
				}
			}
			1607 = {
				add_building_construction = {
					type = infrastructure
					level = 1
					instant_build = yes
				}
			}
			1606 = {
				add_building_construction = {
					type = infrastructure
					level = 1
					instant_build = yes
				}
			}
			JAP_Increase_Jinmu_Econ_Boom = yes
		}
	}
	
	focus = {
		id = JAP_Establish_the_Japan_Housing_Corporation
		icon = GFX_goal_unknown
		cost = 10.00
		x = 17
		y = 2
		prerequisite = {
			focus = JAP_Metropolitan_Area_Redevelopment_Law
		}
		completion_reward = {
			JAP_Expanded_Housing_Increase_Effect = yes
			JAP_Increase_Jinmu_Econ_Boom = yes
		}
	}
	
	focus = {
		id = JAP_New_Board_of_Education_Law
		icon = GFX_goal_unknown
		cost = 10.00
		x = 17
		y = 3
		prerequisite = {
			focus = JAP_Establish_the_Japan_Housing_Corporation
		}
		completion_reward = {
			custom_effect_tooltip = JAP_Leftist_Unrest_01_decrease_tt
			add_ideas = JAP_Reformed_Education_Board
			hidden_effect = {
				JAP_Leftist_Unrest_01_decrease = yes
			}
		}
	}
	
	focus = {
		id = JAP_Promote_Development_of_New_Settlements
		icon = GFX_goal_unknown
		cost = 10.00
		x = 21
		y = 2
		prerequisite = {
			focus = JAP_Metropolitan_Area_Redevelopment_Law
		}
		completion_reward = {
			add_timed_idea = {
                idea = JAP_New_Settlements_Development
                days = 730
            }
			JAP_Increase_Jinmu_Econ_Boom = yes
			hidden_effect = {
				set_variable = { THIS.idea_len_@token:JAP_New_Settlements_Development = 730 }
				set_variable = { THIS.idea_date_@token:JAP_New_Settlements_Development = global.num_days }
			}
		}
	}
	
	focus = {
		id = JAP_Establish_the_Science_and_Technology_Agency
		icon = GFX_goal_unknown
		cost = 10.00
		x = 21
		y = 3
		prerequisite = {
			focus = JAP_Promote_Development_of_New_Settlements
		}
		completion_reward = {
			add_ideas = JAP_Science_and_Technology_Agency
		}
	}
	
	focus = {
		id = JAP_Japan_Highway_Public_Corporation_Law
		icon = GFX_goal_unknown
		cost = 10.00
		x = 19
		y = 4
		prerequisite = {
			focus = JAP_New_Board_of_Education_Law
		}
		prerequisite = {
			focus = JAP_Establish_the_Science_and_Technology_Agency
		}
		completion_reward = {
			random_owned_controlled_state = {
				add_building_construction = {
					type = infrastructure
					level = 1
					instant_build = yes
				}
			}
			random_owned_controlled_state = {
				add_building_construction = {
					type = infrastructure
					level = 1
					instant_build = yes
				}
			}
			add_ideas = JAP_Japan_Highway_Public_Corporation_Law_idea
			JAP_Increase_Jinmu_Econ_Boom = yes
		}
	}
	
	focus = {
		id = JAP_Prostitution_Prevention_Law
		icon = GFX_goal_unknown
		cost = 10.00
		x = 27
		y = 1
		prerequisite = {
			focus = JAP_The_Hatoyama_Administration
		}
		completion_reward = {
			custom_effect_tooltip = JAP_National_Diet_appease_public_2_tt
			swap_ideas = {
				remove_idea = JAP_Obsolete_Pre_War_Era_Laws_4
				add_idea = JAP_Obsolete_Pre_War_Era_Laws_3
			}
			hidden_effect = {
				JAP_National_Diet_appease_public_2 = yes
			}
		}
	}
	
	focus = {
		id = JAP_Restore_the_Role_of_the_Prefectures
		icon = GFX_goal_unknown
		cost = 10.00
		x = 25
		y = 2
		prerequisite = {
			focus = JAP_Prostitution_Prevention_Law
		}
		completion_reward = {
			custom_effect_tooltip = JAP_National_Diet_appease_public_2_tt
			swap_ideas = {
				remove_idea = JAP_Obsolete_Pre_War_Era_Laws_3
				add_idea = JAP_Obsolete_Pre_War_Era_Laws_2
			}
			hidden_effect = {
				JAP_National_Diet_appease_public_2 = yes
			}
		}
	}
	
	focus = {
		id = JAP_Investigate_Promoting_the_Emperor_to_Head_of_State
		icon = GFX_goal_unknown
		cost = 10.00
		x = 29
		y = 2
		prerequisite = {
			focus = JAP_Prostitution_Prevention_Law
		}
		completion_reward = {
			custom_effect_tooltip = JAP_National_Diet_appease_public_1_tt
			add_political_power = 30
			add_stability = 0.075
			JAP_Decrease_Shame_of_Defeat = yes
			hidden_effect = {
				JAP_National_Diet_appease_public_1 = yes
			}
		}
	}
	
	focus = {
		id = JAP_The_Article_9_Question
		icon = GFX_goal_unknown
		cost = 0
		x = 27
		y = 3
		prerequisite = {
			focus = JAP_Restore_the_Role_of_the_Prefectures
		}
		prerequisite = {
			focus = JAP_Investigate_Promoting_the_Emperor_to_Head_of_State
		}
		completion_reward = {
			custom_effect_tooltip = JAP_autocomplete_focus_tt
			JAP_Decrease_Shame_of_Defeat = yes
		}
	}
	
	focus = {
		id = JAP_Establish_the_Constitutional_Research_Committee
		icon = GFX_goal_unknown
		cost = 10.00
		x = 27
		y = 4
		prerequisite = {
			focus = JAP_The_Article_9_Question
		}
		completion_reward = {
			JAP = { country_event = jap_hatoyama.3 }
		}
	}
	
	focus = {
		id = JAP_The_Hatomander_Proposal
		icon = GFX_goal_unknown
		cost = 10.00
		x = 23
		y = 5
		prerequisite = {
			focus = JAP_Japan_Highway_Public_Corporation_Law
		}
		prerequisite = {
			focus = JAP_Establish_the_Constitutional_Research_Committee
		}
		available = {
			date < 1956.7.8
		}
		cancel_if_invalid = yes
		completion_reward = {
			JAP = { country_event = jap_hatoyama.2 }
			custom_effect_tooltip = JAP_The_Hatomander_Proposal_focus_tt
		}
	}
	
	focus = {
		id = JAP_Hatoyama_Constitution_Revised
		icon = GFX_JAP_Constitution_Revision_Successful
		cost = 0
		x = 21
		y = 6
		prerequisite = {
			focus = JAP_The_Hatomander_Proposal
		}
		mutually_exclusive = {
			focus = JAP_Hatoyama_Constitution_Protected
		}
		available = {
			always = no
		}
		completion_reward = {
			custom_effect_tooltip = JAP_autocomplete_focus_tt		
			custom_effect_tooltip = JAP_WORK_IN_PROGRESS_tt
			JAP_Decrease_Shame_of_Defeat = yes
		}
	}
	
	focus = {
		id = JAP_Hatoyama_Constitution_Protected
		icon = GFX_JAP_Constitution_Revision_Shelved
		cost = 0
		x = 25
		y = 6
		prerequisite = {
			focus = JAP_The_Hatomander_Proposal
		}
		mutually_exclusive = {
			focus = JAP_Hatoyama_Constitution_Revised
		}
		available = {
			always = no
		}
		completion_reward = {
			custom_effect_tooltip = JAP_autocomplete_focus_tt
		}
	}
	
	focus = {
		id = JAP_Yuai_Seishin
		icon = GFX_goal_unknown
		cost = 10.00
		x = 23
		y = 7
		prerequisite = {
			focus = JAP_Hatoyama_Constitution_Revised
			focus = JAP_Hatoyama_Constitution_Protected
		}
		completion_reward = {
			add_timed_idea = {
                idea = JAP_Yuai_Seishin_Idea
                days = 365
            }
			hidden_effect = {
				set_variable = { THIS.idea_len_@token:JAP_Yuai_Seishin_Idea = 365 }
				set_variable = { THIS.idea_date_@token:JAP_Yuai_Seishin_Idea = global.num_days }
			}
		}
	}
	
	focus = {
		id = JAP_Formation_of_the_Jiminto
		icon = GFX_JAP_Formation_Of_The_Liberal_Democratic_Party
		cost = 0
		x = 35
		y = 1
		prerequisite = {
			focus = JAP_The_Hatoyama_Administration
		}
		available = {
			always = no
		}
		completion_reward = {
			set_power_balance = {
				id = CWIC_bop_JAP_LDP_balance_of_power
				left_side = CWIC_bop_JAP_LDP_balance_of_power_left_side
				right_side = CWIC_bop_JAP_LDP_balance_of_power_right_side
				set_value = LDP_fac_balancer_for_BOP_var
			}			
		}
	}
	
	focus = {
		id = JAP_Strengthen_the_Boryu_Factions
		icon = GFX_goal_unknown
		cost = 10
		x = 33
		y = 2
		prerequisite = {
			focus = JAP_Formation_of_the_Jiminto
		}
		completion_reward = {
			custom_effect_tooltip = JAP_LDP_Party_Strength_increase_tt
			hidden_effect = {
				JAP_LDP_Party_Strength_increase = yes
			}
		}
	}
	
	focus = {
		id = JAP_Appease_the_Former_Jiyuto_Members
		icon = GFX_goal_unknown
		cost = 10
		x = 37
		y = 2
		prerequisite = {
			focus = JAP_Formation_of_the_Jiminto
		}
		completion_reward = {
			custom_effect_tooltip = JAP_LDP_Party_Strength_increase_tt
			hidden_effect = {
				JAP_LDP_Party_Strength_increase = yes
			}
		}
	}
	
	focus = {
		id = JAP_Meet_the_Keidanrens_Demands
		icon = GFX_goal_unknown
		cost = 10
		x = 35
		y = 3
		prerequisite = {
			focus = JAP_Strengthen_the_Boryu_Factions
		}
		prerequisite = {
			focus = JAP_Appease_the_Former_Jiyuto_Members
		}
		completion_reward = {
			remove_ideas = JAP_Low_Keidanren_Support
			JAP_Increase_Jinmu_Econ_Boom = yes
		}
	}
	
	focus = {
		id = JAP_The_1955_System
		icon = GFX_JAP_The_1955_System
		cost = 10
		x = 35
		y = 4
		prerequisite = {
			focus = JAP_Meet_the_Keidanrens_Demands
		}
		completion_reward = {
			custom_effect_tooltip = JAP_LDP_Party_Strength_increase_tt
			add_political_power = 100
			add_popularity = {
				ideology = conservative
				popularity = 0.1
			}
			hidden_effect = {
				JAP_LDP_Party_Strength_increase = yes
			}
		}
	}
	
	#Ishibashi Branch
	focus = {
		id = JAP_The_Ishibashi_Administration
		icon = GFX_goal_unknown
		cost = 10.00
		x = 26
		y = 0
		allow_branch = {
			has_country_flag = JAP_Tanzan_Ishibashi_Prime_Minister
		}
		completion_reward = {
			add_political_power = 150
		}
	}
	focus = {
		id = JAP_Five_Pledges
		icon = GFX_JAP_Five_Pledges5
		cost = 10.00
		x = 26
		y = 1
		prerequisite = {
			focus = JAP_The_Ishibashi_Administration
		}
		completion_reward = {
			custom_effect_tooltip = JAP_National_Diet_appease_public_3_tt
			hidden_effect = {
				JAP_National_Diet_appease_public_2 = yes
				JAP_National_Diet_appease_public_2 = yes
			}
		}
	}
	focus = {
		id = JAP_No_to_Factional_Favouritism
		icon = GFX_JAP_End_Factional_Favouritism
		cost = 10.00
		x = 19
		y = 2
		prerequisite = {
			focus = JAP_Five_Pledges
		}
		completion_reward = {
			custom_effect_tooltip = JAP_LDP_Party_Strength_increase_tt
			hidden_effect = {
				JAP_LDP_Party_Strength_increase = yes
			}
		}
	}
	focus = {
		id = JAP_Work_With_the_Opposition
		icon = GFX_JAP_Work_With_The_Opposition
		cost = 10.00
		x = 17
		y = 3
		prerequisite = {
			focus = JAP_No_to_Factional_Favouritism
		}
		completion_reward = {
			custom_effect_tooltip = JAP_National_Diet_cabinet_approval_increase_1_tt
			custom_effect_tooltip = JAP_National_Diet_appease_public_2_tt
			hidden_effect = {
				JAP_cabinet_approval_increase_1 = yes
				JAP_National_Diet_appease_public_2 = yes
			}
		}
	}
	focus = {
		id = JAP_Suspend_the_Constitutional_Research_Committee
		icon = GFX_Generic_National_Focus_Politics_33
		cost = 10.00
		x = 21
		y = 3
		prerequisite = {
			focus = JAP_No_to_Factional_Favouritism
		}
		completion_reward = {
			custom_effect_tooltip = JAP_National_Diet_cabinet_approval_increase_0_tt
			custom_effect_tooltip = JAP_Leftist_Unrest_01_decrease_tt
			hidden_effect = {
				JAP_cabinet_approval_increase_0 = yes
				JAP_Leftist_Unrest_01_decrease = yes
			}
		}
	}
	focus = {
		id = JAP_A_Functional_Diet
		icon = GFX_JAP_Functional_Diet
		cost = 10.00
		x = 19
		y = 4
		prerequisite = {
			focus = JAP_Suspend_the_Constitutional_Research_Committee
		}
		prerequisite = {
			focus = JAP_Work_With_the_Opposition
		}
		completion_reward = {
			add_stability = 0.075
		}
	}
	focus = {
		id = JAP_Pursue_Independent_Foreign_Policy
		icon = GFX_JAP_Pursue_Independent_Foreign_Policy
		cost = 10.00
		x = 23
		y = 2
		prerequisite = {
			focus = JAP_The_Ishibashi_Administration
		}
		completion_reward = {
			add_political_power = 50
		}
	}
	focus = {
		id = JAP_Launch_Nationwide_Speech_Tour
		icon = GFX_JAP_Launch_Nationwide_Speech_Tour
		cost = 10.00
		x = 27
		y = 2
		prerequisite = {
			focus = JAP_The_Ishibashi_Administration
		}
		completion_reward = {
			JAP = { country_event = jap_ishibashi.2 }
		}
	}
	focus = {
		id = JAP_Increase_Chinese_Trade
		icon = GFX_JAP_Increase_Chinese_Trade
		cost = 10.00
		x = 25
		y = 3
		prerequisite = {
			focus = JAP_Pursue_Independent_Foreign_Policy
		}
		prerequisite = {
			focus = JAP_Launch_Nationwide_Speech_Tour
		}
		bypass = {
			PRC = {
				has_completed_focus = PRC_50s_Severance_of_Economic_And_Trade_Cooperation_with_Japan
			}
		}
		completion_reward = {
			if = {
				limit = { has_global_flag = PRC_Victory }
				add_opinion_modifier = {
					target = PRC
					modifier = small_increase_trade
				}
				PRC = {
					add_opinion_modifier = {
						target = JAP
						modifier = small_increase_trade
					}
				}
			}
			else_if = {
				limit = { has_global_flag = ROC_Victory }
				add_opinion_modifier = {
					target = CHI
					modifier = small_increase_trade
				}
				CHI = {
					add_opinion_modifier = {
						target = JAP
						modifier = small_increase_trade
					}
				}
			}
		}
	}
	focus = {
		id = JAP_Increase_Economic_Ties_With_Eastern_Europe
		icon = GFX_Generic_National_Focus_Diplomacy_24
		cost = 10.00
		x = 23
		y = 4
		prerequisite = {
			focus = JAP_Increase_Chinese_Trade
		}
		completion_reward = {
			SOV = {
				add_opinion_modifier = {
					target = JAP
					modifier = small_increase_trade
				}
			}
			POL = {
				add_opinion_modifier = {
					target = JAP
					modifier = small_increase_trade
				}
			}
			DDR = {
				add_opinion_modifier = {
					target = JAP
					modifier = small_increase_trade
				}
			}
			CZE = {
				add_opinion_modifier = {
					target = JAP
					modifier = small_increase_trade
				}
			}
			BUL = {
				add_opinion_modifier = {
					target = JAP
					modifier = small_increase_trade
				} 
			}
			ROM = {
				add_opinion_modifier = {
					target = JAP
					modifier = small_increase_trade
				}
			}
			HUN = {
				add_opinion_modifier = {
					target = JAP
					modifier = small_increase_trade
				}
			}
		}
	}
	focus = {
		id = JAP_Sino_Japanese_Fishing_Agreement
		icon = GFX_JAP_Sino_Japanese_Fishing_Agreement
		cost = 10.00
		x = 27
		y = 4
		prerequisite = {
			focus = JAP_Increase_Chinese_Trade
		}
		bypass = {
			PRC = {
				has_completed_focus = PRC_50s_Severance_of_Economic_And_Trade_Cooperation_with_Japan
			}
		}
		completion_reward = {
			country_event = jap_treaty.12
			if = {
				limit = { has_global_flag = PRC_Victory }
				PRC = { country_event = jap_treaty.12 }
			}
			else_if = {
				limit = { has_global_flag = ROC_Victory }
				CHI = { country_event = jap_treaty.12 }
			}
		}
	}
	focus = {
		id = JAP_Chinese_Friendship_Treaty
		icon = GFX_JAP_Chinese_Friendship_Treaty
		cost = 10.00
		x = 25
		y = 5
		prerequisite = {
			focus = JAP_Increase_Economic_Ties_With_Eastern_Europe
		}
		prerequisite = {
			focus = JAP_Sino_Japanese_Fishing_Agreement
		}
		bypass = {
			PRC = {
				has_completed_focus = PRC_50s_Severance_of_Economic_And_Trade_Cooperation_with_Japan
			}
		}
		completion_reward = {
			if = {
				limit = { has_global_flag = PRC_Victory }
				add_opinion_modifier = {
					target = PRC
					modifier = small_increase
				}
				PRC = {
					add_opinion_modifier = {
						target = JAP
						modifier = small_increase
					}
				}
			}
			else_if = {
				limit = { has_global_flag = ROC_Victory }
				add_opinion_modifier = {
					target = CHI
					modifier = small_increase
				}
				CHI = {
					add_opinion_modifier = {
						target = JAP
						modifier = small_increase
					}
				}
			}
		}
	}
	
	focus = {
		id = JAP_100_Billion_Yen_Tax_Cut
		icon = GFX_JAP_100_Billion_Yen_Tax_Cut
		cost = 10.00
		x = 31
		y = 3
		prerequisite = {
			focus = JAP_Launch_Nationwide_Speech_Tour
		}
		completion_reward = {
			add_timed_idea = {
				idea = JAP_100_Billion_Yen_Tax_Cut_idea
				days = 365
			}
			hidden_effect = {
				set_variable = { THIS.idea_len_@token:JAP_100_Billion_Yen_Tax_Cut_idea = 365 }
				set_variable = { THIS.idea_date_@token:JAP_100_Billion_Yen_Tax_Cut_idea = global.num_days }
			}
		}
	}
	focus = {
		id = JAP_100_Billion_Yen_Investment_Pledge
		icon = GFX_JAP_100_Billion_Yen_Investment_Pledge
		cost = 10.00
		x = 31
		y = 4
		prerequisite = {
			focus = JAP_100_Billion_Yen_Tax_Cut
		}
		completion_reward = {
			custom_effect_tooltip = JAP_100_plus_money_tt
			add_to_variable = {
				currentMoney = 100
			}
			add_timed_idea = {
				idea = JAP_Strained_Budget
				days = 100
			}
			hidden_effect = {
				set_variable = { THIS.idea_len_@token:JAP_Strained_Budget = 100 }
				set_variable = { THIS.idea_date_@token:JAP_Strained_Budget = global.num_days }
			}
		}
	}
	focus = {
		id = JAP_Increase_Professional_Standards_for_Public_Servants
		icon = GFX_JAP_Increase_Professional_Standards_for_Public_Servants
		cost = 10.00
		x = 35
		y = 3
		prerequisite = {
			focus = JAP_Launch_Nationwide_Speech_Tour
		}
		completion_reward = {
			
		}
	}
	focus = {
		id = JAP_Efforts_to_Increase_Employment_and_Production
		icon = GFX_JAP_Efforts_to_Increase_Employment_and_Production
		cost = 10.00
		x = 35
		y = 4
		prerequisite = {
			focus = JAP_Increase_Professional_Standards_for_Public_Servants
		}
		completion_reward = {
			
		}
	}
	focus = {
		id = JAP_Push_Through_Universal_Healthcare
		icon = GFX_JAP_Push_Through_Universal_Healthcare
		cost = 10.00
		x = 33
		y = 5
		prerequisite = {
			focus = JAP_100_Billion_Yen_Investment_Pledge
		}
		prerequisite = {
			focus = JAP_Efforts_to_Increase_Employment_and_Production
		}
		completion_reward = {
			
		}
	}

	
	### Kishi Branch ####################
	focus = {
		id = JAP_The_Kishi_Administration
		icon = GFX_JAP_The_Kishi_Administration
		cost = 10.00
		x = 28
		y = 0
		allow_branch = {
			has_country_flag = JAP_Nobusuke_Kishi_Prime_Minister
		}
		completion_reward = {
			add_political_power = 200
		}
	}
	focus = {
		id = JAP_Establish_Diplomatic_Relations_with_Eastern_Europe
		icon = GFX_JAP_Establish_Diplomatic_Relations_with_Eastern_Europe
		icon = GFX_JAP
		cost = 10.00
		x = 24
		y = 1
		prerequisite = {
			focus = JAP_The_Kishi_Administration
		}
		completion_reward = {
			JAP = { country_event = { id = jap_treaty.11 } }
			POL = { country_event = { id = jap_treaty.11 } }
			CZE = { country_event = { id = jap_treaty.11 } }
			HUN = { country_event = { id = jap_treaty.11 } }
			BUL = { country_event = { id = jap_treaty.11 } }
			ROM = { country_event = { id = jap_treaty.11 } }
			SOV = { country_event = { id = jap_treaty.11 } }
		}
	}
	focus = {
		id = JAP_Compensations_for_Vietnam
		icon = GFX_JAP_Compensations_for_Vietnam
		cost = 10.00
		x = 22
		y = 2
		prerequisite = {
			focus = JAP_Establish_Diplomatic_Relations_with_Eastern_Europe
		}
		completion_reward = {
			JAP = { country_event = { id = jap_vietnam.1 } }
			VIE = { country_event = { id = jap_vietnam.1 } }
		}
	}
	focus = {
		id = JAP_War_Reparations_for_Indonesia
		cost = 10.00
		x = 26
		y = 2
		prerequisite = {
			focus = JAP_Establish_Diplomatic_Relations_with_Eastern_Europe
		}
		completion_reward = {
			JAP = { country_event = { id = jap_ino.1 } }
			INO = { country_event = { id = jap_ino.1 } }
		}
	}
	focus = {
		id = JAP_Pearl_of_Asia
		cost = 10.00
		x = 24
		y = 3
		prerequisite = {
			focus = JAP_Compensations_for_Vietnam
		}
		prerequisite = {
			focus = JAP_War_Reparations_for_Indonesia
		}
		completion_reward = {
			every_country = {
				limit = {
					any_core_state = { is_on_continent = asia }
				}
				country_event = { id = japan.11 }
			}
		}
	}
	focus = {
		id = JAP_Ramp_Up_the_Constitutional_Debate
		icon = JAP_Ramp_Up_the_Constitutional_Debate
		cost = 10.00
		x = 28
		y = 1
		prerequisite = {
			focus = JAP_The_Kishi_Administration
		}
		completion_reward = {
			JAP = { country_event = { id = jap_kishi.1 } }
			JAP_Decrease_Shame_of_Defeat = yes
		}
	}
	focus = {
		id = JAP_Overcome_the_Lingering_Legacy_of_the_Occupation
		icon = GFX_JAP_Overcome_the_Lingering_Legacy_of_the_Occupation
		cost = 10.00
		x = 28
		y = 2
		prerequisite = {
			focus = JAP_Ramp_Up_the_Constitutional_Debate
		}
		completion_reward = {
			add_political_power = 50
			swap_ideas = {
				remove_idea = JAP_Obsolete_Pre_War_Era_Laws_2
				add_idea = JAP_Obsolete_Pre_War_Era_Laws_1
			}
		}
	}
	focus = {
		id = JAP_Invest_in_New_Domestic_Destroyers
		icon = GFX_goal_unknown
		cost = 10.00
		x = 28
		y = 3
		prerequisite = {
			focus = JAP_Overcome_the_Lingering_Legacy_of_the_Occupation
		}
		completion_reward = {
			add_tech_bonus = {
				bonus = 1
				uses = 1
				category = screen_tech
			}
			add_ideas = JAP_Domestic_Destroyer_Programme
		}
	}
	focus = {
		id = JAP_Request_Release_of_Remaining_War_Criminals
		icon = GFX_JAP_Request_Release_of_Remaining_War_Criminals
		cost = 10.00
		x = 32
		y = 1
		prerequisite = {
			focus = JAP_The_Kishi_Administration
		}
		completion_reward = {
			custom_effect_tooltip = JAP_Rightist_Equillibrium_1_increase_tt
			custom_effect_tooltip = JAP_Rightist_Unrest_01_decrease_tt
			custom_effect_tooltip = JAP_National_Diet_cabinet_approval_increase_0_tt
			JAP_Decrease_Shame_of_Defeat = yes
			hidden_effect = {
				JAP_Rightist_Equillibrium_1_increase = yes
				JAP_Rightist_Unrest_01_decrease = yes
				JAP_cabinet_approval_increase_0 = yes
			}
		}
	}
	focus = {
		id = JAP_Five_Million_Nationwide_Membership_Campaign
		icon = GFX_JAP_Five_Million_Nationwide_Membership_Campaign
		cost = 10.00
		x = 30
		y = 2
		prerequisite = {
			focus = JAP_Request_Release_of_Remaining_War_Criminals
		}
		completion_reward = {
			custom_effect_tooltip = JAP_LDP_Party_Strength_increase_tt
			hidden_effect = {
				JAP_LDP_Party_Strength_increase = yes
			}
		}
	}
	focus = {
		id = JAP_Push_for_Single_Member_Districts
		icon = GFX_JAP_Push_for_Single_Member_Districts
		cost = 10.00
		x = 34
		y = 2
		prerequisite = {
			focus = JAP_Request_Release_of_Remaining_War_Criminals
		}
		completion_reward = {
			add_political_power = 25
			swap_ideas = {
				remove_idea = JAP_Shakaito_Threat_2
				add_idea = JAP_Shakaito_Threat_1
			}
		}
	}
	focus = {
		id = JAP_Remove_the_Opposition_From_Committee_Chair_Positions
		icon = JAP_Remove_the_Opposition_From_Committee_Chair_Positions
		cost = 10.00
		x = 32
		y = 3
		prerequisite = {
			focus = JAP_Five_Million_Nationwide_Membership_Campaign
		}
		prerequisite = {
			focus = JAP_Push_for_Single_Member_Districts
		}
		completion_reward = {
			custom_effect_tooltip = JAP_National_Diet_cabinet_approval_decrease_1_tt
			add_political_power = 25
			remove_ideas = JAP_Shakaito_Threat_1
			hidden_effect = {
				JAP_cabinet_approval_decrease_1 = yes
			}
		}
	}
	focus = {
		id = JAP_Withdraw_the_Police_Duties_Bill
		icon = GFX_JAP_Withdraw_the_Police_Duties_Bill
		cost = 10.00
		x = 26
		y = 4
		prerequisite = {
			focus = JAP_Remove_the_Opposition_From_Committee_Chair_Positions
		}
		prerequisite = {
			focus = JAP_Pearl_of_Asia
		}
		prerequisite = {
			focus = JAP_Invest_in_New_Domestic_Destroyers
		}
		completion_reward = {
			custom_effect_tooltip = JAP_Remove_Unrest_Issue_Protests_Against_the_Police_Duties_Bill_tt
			custom_effect_tooltip = JAP_Leftist_Unrest_01_decrease_tt
			custom_effect_tooltip = JAP_National_Diet_cabinet_approval_increase_0_tt
			custom_effect_tooltip = JAP_National_Diet_appease_public_1_tt
			hidden_effect = {
				JAP_Leftist_Unrest_01_decrease = yes
				JAP_cabinet_approval_increase_0 = yes
				JAP_National_Diet_appease_public_1 = yes
				remove_from_array = { JAP_National_Radicalism_Issues = 4 }
			}
		}
	}
	focus = {
		id = JAP_School_Curriculum_and_Teachers_Efficiency_Rating_System_Reforms
		icon = GFX_JAP_School_Curriculum_and_Teachers_Efficiency_Rating_System_Reforms
		cost = 10.00
		x = 30
		y = 4
		prerequisite = {
			focus = JAP_Remove_the_Opposition_From_Committee_Chair_Positions
		}
		prerequisite = {
			focus = JAP_Pearl_of_Asia
		}
		prerequisite = {
			focus = JAP_Invest_in_New_Domestic_Destroyers
		}
		completion_reward = {
			add_timed_idea = {
				idea = JAP_School_Curriculum_and_Teachers_Efficiency_Rating_System_Reforms_idea
				days = 500
			}
			hidden_effect = {
				set_variable = { THIS.idea_len_@token:JAP_School_Curriculum_and_Teachers_Efficiency_Rating_System_Reforms_idea = 500 }
				set_variable = { THIS.idea_date_@token:JAP_School_Curriculum_and_Teachers_Efficiency_Rating_System_Reforms_idea = global.num_days }
				country_event = {
					id = jap_kishi.5
					days = 7
					random_hours = 12
					random_days = 5
				}
				country_event = {
					id = jap_kishi.6
					days = 14
					random_hours = 12
					random_days = 5
				}
			}
		}
	}
	focus = {
		id = JAP_Take_Control_of_the_M_Fund
		icon = GFX_JAP_Take_Control_Of_The_MFund
		cost = 10.00
		x = 28
		y = 5
		prerequisite = {
			focus = JAP_Withdraw_the_Police_Duties_Bill
		}
		prerequisite = {
			focus = JAP_School_Curriculum_and_Teachers_Efficiency_Rating_System_Reforms
		}
		completion_reward = {
			JAP = { country_event = { id = jap_kishi.4 } }
		}
	}
	


### IKEDA HAYATO TREE #################################################
	focus = {
		id = JAP_The_Ikeda_Administration
		icon = GFX_JAP_The_Income_Doubling_Plan
		cost = 10
		x = 26
		y = 0
		available = {
		}
		allow_branch = { has_country_flag = JAP_Ikeda_Hayato_Prime_Minister }
		completion_reward = {
			add_political_power = 100
			LDP_Ikeda_Cabinet_Jinji = yes
			hidden_effect = {
				country_event = { id = jap_ikeda.3 days = 3 }
				LDP_fac_var_set_up = yes
			}
		}
	}
### Econ Tree ###
	focus = {
		id = JAP_The_Income_Doubling_Plan
		icon = GFX_Generic_National_Focus_Economics_19
		prerequisite = { focus = JAP_The_Ikeda_Administration }
		cost = 10
		x = 26
		y = 1
		available = {
			has_completed_focus = JAP_Shift_The_Season_Of_Politics_To_The_Age_Of_Economics
			has_completed_focus = JAP_A_Post_Reconstruction_Economy
		}
		completion_reward = {
			add_timed_idea = {
				idea = governmental_planning_and_management
				days = 365
			}
			custom_effect_tooltip = JAP_The_Income_Doubling_Plan_tt
			hidden_effect = {
				JAP_The_Income_Doubling_Plan_setup = yes
				country_event = { id = jap_ikeda.4 days = 3 }
			}
		}
	}
	focus = {
		id = JAP_Basic_Agricultural_Act
		icon = GFX_Generic_National_Focus_Agriculture_26
		prerequisite = { focus = JAP_The_Income_Doubling_Plan }
		cost = 10
		x = 24
		y = 2
		available = {
		}
		completion_reward = {
			unlock_decision_tooltip = JAP_Encourage_Farmers_Buying_Machines_From_Shosha
			unlock_decision_tooltip = JAP_Import_US_Extra_Crops
			unlock_decision_tooltip = JAP_Fertilizer_Aid
			unlock_decision_tooltip = JAP_Pesticides_Aid
			unlock_decision_tooltip = JAP_Gentan_Policy
			hidden_effect = {
			
				country_event = { id = jap_ikeda.5 days = 3 }
			}
		}
	}
	focus = {
		id = JAP_Big_Four_Industrial_Acts
		icon = GFX_Generic_National_Focus_Production_10
		prerequisite = { focus = JAP_The_Income_Doubling_Plan }
		cost = 10
		x = 26
		y = 2
		available = {
		}
		completion_reward = {
			custom_effect_tooltip = available_designer
			show_ideas_tooltip = TEPCO
			random_owned_controlled_state = {
				add_extra_state_shared_building_slots = 1
				add_building_construction = {
					type = fossil_fuel_powerplant
					level = 1
					instant_build = yes
				}
			}
			random_owned_controlled_state = {
				add_extra_state_shared_building_slots = 1
				add_building_construction = {
					type = fossil_fuel_powerplant
					level = 1
					instant_build = yes
				}
			}
			hidden_effect = {
			
				country_event = { id = jap_ikeda.6 days = 3 }
			}
		}
	}
	focus = {
		id = JAP_Basic_Small_Medium_Enterprise_Act
		icon = GFX_Generic_National_Focus_Economics_16
		prerequisite = { focus = JAP_The_Income_Doubling_Plan }
		cost = 10
		x = 28
		y = 2
		available = {
		}
		completion_reward = {
			unlock_decision_tooltip = JAP_Promote_Investment_To_Small_Medium_Enterprise
			unlock_decision_tooltip = JAP_Support_Franchising_General_Super_Market_Companies
			unlock_decision_tooltip = JAP_Support_Service_Industry
		
			hidden_effect = {
			
				country_event = { id = jap_ikeda.7 days = 3 }
			}
		}
	}
	focus = {
		id = JAP_Basic_forestry_Act
		icon = GFX_Generic_National_Focus_Politics_4
		prerequisite = { focus = JAP_Big_Four_Industrial_Acts }
		prerequisite = { focus = JAP_Basic_Agricultural_Act }
		cost = 10
		x = 25
		y = 3
		available = {
		}
		completion_reward = {
			536 = { #Hokkaido
				add_building_construction = {
					type = state_infrastructure
					level = 1
					instant_build = yes
				}
			}
			1601 = { #Shizuoka
				add_building_construction = {
					type = state_infrastructure
					level = 1
					instant_build = yes
				}
			}
			533 = { #Tohoku
				add_building_construction = {
					type = state_infrastructure
					level = 1
					instant_build = yes
				}
			}
			1597 = { #Miyagi
				add_building_construction = {
					type = state_infrastructure
					level = 1
					instant_build = yes
				}
			}			
			1598 = { #Fukushima
				add_building_construction = {
					type = state_infrastructure
					level = 1
					instant_build = yes
				}
			}		
			hidden_effect = {
			
				country_event = { id = jap_ikeda.8 days = 3 }
			}
		}
	}
	focus = {
		id = JAP_New_Industrial_City_Construction_Promotion_Act
		icon = GFX_Generic_National_Focus_Production_17
		prerequisite = { focus = JAP_Big_Four_Industrial_Acts }
		prerequisite = { focus = JAP_Basic_Small_Medium_Enterprise_Act }
		cost = 10
		x = 27
		y = 3
		available = {
			has_completed_focus = JAP_Promote_Rural_To_Urban
		}
		completion_reward = {
			unlock_decision_tooltip = JAP_Small_Investment_To_Infrastructure
			unlock_decision_tooltip = JAP_Medium_Investment_To_Infrastructure
			unlock_decision_tooltip = JAP_Massive_Investment_To_Infrastructure
		
			hidden_effect = {
			
				country_event = { id = jap_ikeda.9 days = 3 }
			}
		}
	}
	focus = {
		id = JAP_Special_Industrial_Development_Act
		icon = GFX_Generic_National_Focus_Production_9
		prerequisite = { focus = JAP_Big_Four_Industrial_Acts }
		prerequisite = { focus = JAP_Basic_Small_Medium_Enterprise_Act }
		cost = 10
		x = 29
		y = 3
		available = {
		}
		completion_reward = {
			unlock_decision_tooltip = JAP_Motor_Vehicle_Industry_Investment
			unlock_decision_tooltip = JAP_Aeroplane_Industry_Investment
			unlock_decision_tooltip = JAP_Helicopter_Industry_Investment
		
			hidden_effect = {
			
				country_event = { id = jap_ikeda.10 days = 3 }
			}
		}
	}
	focus = {
		id = JAP_Coastal_Fisheries_Promotion_Act
		icon = GFX_Generic_National_Focus_Other_10
		prerequisite = { focus = JAP_Big_Four_Industrial_Acts }
		cost = 10
		x = 23
		y = 3
		available = {
		}
		completion_reward = {

		
			hidden_effect = {
			
				country_event = { id = jap_ikeda.11 days = 3 }
			}
		}
	}
	focus = {
		id = JAP_Taiheyo_Belt_Line_Project
		icon = GFX_Generic_National_Focus_Economics_11
		prerequisite = { focus = JAP_Coastal_Fisheries_Promotion_Act }
		prerequisite = { focus = JAP_Basic_forestry_Act }
		prerequisite = { focus = JAP_New_Industrial_City_Construction_Promotion_Act }
		prerequisite = { focus = JAP_Special_Industrial_Development_Act }
		cost = 10
		x = 26
		y = 4
		available = {
		}
		completion_reward = {
			unlock_decision_tooltip = JAP_Heavy_Industry_Investment
			unlock_decision_tooltip = JAP_Keihin_Industrial_Park
			unlock_decision_tooltip = JAP_Chukyo_Industrial_Park
			unlock_decision_tooltip = JAP_Hanshin_Industrial_Park
			unlock_decision_tooltip = JAP_Kitakyushu_Industrial_Park
		
			hidden_effect = {
			
				country_event = { id = jap_ikeda.12 days = 3 }
			}
		}
	}
	focus = {
		id = JAP_Maritime_Reconstruction_And_Development_Act
		icon = GFX_Generic_National_Focus_Other_1
		prerequisite = { focus = JAP_Taiheyo_Belt_Line_Project }
		cost = 10
		x = 24
		y = 5
		available = {
		}
		completion_reward = {
			random_owned_controlled_state = {
				limit = {
					is_coastal = yes
				}
				add_extra_state_shared_building_slots = 2
				add_building_construction = {
					type = dockyard
					level = 2
					instant_build = yes
				}
			}
		
			hidden_effect = {
			
				country_event = { id = jap_ikeda.13 days = 3 }
			}
		}
	}
	focus = {
		id = JAP_Science_And_Technology_Promotion_Act
		icon = GFX_Generic_National_Focus_Research_22
		prerequisite = { focus = JAP_Taiheyo_Belt_Line_Project }
		cost = 10
		x = 28
		y = 5
		available = {
		}
		completion_reward = {
			unlock_decision_tooltip = JAP_Promote_Being_Highschool_Students
			unlock_decision_tooltip = JAP_Expand_STEM_Students
			unlock_decision_tooltip = JAP_Build_Technical_College
			unlock_decision_tooltip = JAP_Launch_US_Japan_Technology_Council
			unlock_decision_tooltip = JAP_Boost_Nuclear_Technology
			add_timed_idea = {
				idea = encourage_scientific_competition
				days = 1825
			}
		
			hidden_effect = {
			
				country_event = { id = jap_ikeda.14 days = 3 }
			}
		}
	}
	focus = {
		id = JAP_The_Asian_Big_Dragon
		icon = GFX_Generic_National_Focus_Diplomacy_1
		prerequisite = { focus = JAP_Science_And_Technology_Promotion_Act }
		prerequisite = { focus = JAP_Maritime_Reconstruction_And_Development_Act }
		cost = 10
		x = 26
		y = 6
		available = {
			has_completed_focus = JAP_Tokyo_Olympic
			custom_trigger_tooltip = {
				tooltip = JAP_The_Asian_Big_Dragon_tt
				check_variable = { JAP_Economic_Development > 0.8 }
			}
		}
		completion_reward = {
			add_ideas = JAP_Economic_Miracle
		
			hidden_effect = {
			
				country_event = { id = jap_ikeda.15 days = 3 }
			}
		}
	}

### Diplomatic Tree ###
	focus = {
		id = JAP_We_Love_Amerika
		icon = GFX_Generic_National_Focus_USA_6
		prerequisite = { focus = JAP_The_Ikeda_Administration }
		cost = 10
		x = 33
		y = 1
		available = {
		}
		completion_reward = {
			add_stability = 0.05
			hidden_effect = {
			
				country_event = { id = jap_ikeda.16 days = 3 }
			}
		}
		#1961年6月19日の訪米では、キャピトルで上下院議員全員と握手し[188]、アメリカ合衆国下院で「こんどは援助の要請にきたのではありません」と演説し、拍手喝采を浴びた[189]。ハイライトは6月21日、ケネディとワシントンD.C.ポトマック川に浮ぶ、大統領専用ヨット・ハニー・フィッツ上での会談で、アメリカが日本を重視しているという態度を演じさせることに成功した[176][177][190]。このヨットでの会談はマクミラン英首相に次いで二人目だった[191]。
	}
	focus = {
		id = JAP_Kennedy_Conference
		icon = GFX_Generic_National_Focus_USA_9
		prerequisite = { focus = JAP_We_Love_Amerika }
		cost = 10
		x = 31
		y = 2
		available = {
		}
		completion_reward = {
			hidden_effect = {
			
				country_event = { id = jap_ikeda.17 days = 3 }
			}
		}
		#この首脳会談の具体的成果として、ケネディに祝日に限り沖縄の公共建築物に日の丸掲揚を認めさせ[202][203][204][205]、「沖縄と小笠原諸島に対し、日本が潜在主権を保有する」ことをアメリカに認めさせた
	}
	focus = {
		id = JAP_Second_Time_Black_Ships
		icon = GFX_Generic_National_Focus_Diplomacy_30
		prerequisite = { focus = JAP_We_Love_Amerika }
		cost = 10
		x = 36
		y = 2
		available = {
		}
		completion_reward = {
		
			hidden_effect = {
			
				country_event = { id = jap_ikeda.18 days = 3 }
			}
		}
		#欧州のいくつかの国は日本を西側につなぎとめる必要を感じてはいたものの、欧州全体でいえば、外交課題としてより重要であったのは、欧州統合問題や米欧関係であり、遠く離れた極東に位置する日本への関心は決して高くはなく、日本はアメリカを間に挟んだ形式的な、不確かなパートナーであった[246]。このような状況下での池田の欧州接近ではあったが、ドル防衛政策で陰りが見えるアメリカ市場と違い、充分な購買力を持つ欧州市場にはフロンティアとしての魅力があった[246]。また池田自身が大国志向を持っており、欧州諸国の対日経済差別を撤回させ、日本が欧州諸国と対等となることに、国際社会における日本の地位向上という意義を見出していたのである[246][247]。
	}
	focus = {
		id = JAP_Three_Principle_Theory
		icon = GFX_Generic_National_Focus_Diplomacy_47
		prerequisite = { focus = JAP_Second_Time_Black_Ships }
		prerequisite = { focus = JAP_Kennedy_Conference }
		cost = 10
		x = 33
		y = 3
		available = {
		}
		completion_reward = {
		
			hidden_effect = {
			
				country_event = { id = jap_ikeda.19 days = 3 }
			}
		}
	}
	focus = {
		id = JAP_VIsit_SEA
		icon = GFX_Generic_National_Focus_Diplomacy_17
		prerequisite = { focus = JAP_Second_Time_Black_Ships }
		cost = 10
		x = 35
		y = 3
		available = {
		}
		completion_reward = {
		
			hidden_effect = {
			
				country_event = { id = jap_ikeda.20 days = 3 }
			}
		}
	}
	focus = {
		id = JAP_Fuck_Khruschev
		icon = GFX_Generic_National_Focus_USSR_14
		prerequisite = { focus = JAP_Second_Time_Black_Ships }
		cost = 10
		x = 37
		y = 3
		available = {
		}
		completion_reward = {
			add_popularity = {
				ideology = conservative
				popularity = 0.05
			}		
			hidden_effect = {
			
				country_event = { id = jap_ikeda.21 days = 3 }
			}
		}
		#フルシチョフも黙っておらず、特に領土問題をめぐって難癖をつけてきた[213]。「領土問題は一連の国際協定によって久しき以前に解決済みであり、日本国の領土でない領土の日本への返還問題をどうして提起できるのだろうか」と、日ソ共同宣言を反故にし、歯舞群島・色丹島を含めた領土問題のゼロ回答をほのめかした[213][214]。これに対して池田は国会審議を通じて「日本固有の領土」たる国後島・択捉島は、サンフランシスコ講和条約で日本が放棄した「千島」のなかには含まれない」とする新見解を発表し「領土問題は解決済み」とするソ連側の主張に反駁し1962年3月9日には、沖縄・小笠原施政権回復とともに、北方領土回復を閣議決定した[205][215][216][217]。また池田政権として国内世論を「四島一括返還」論に一本化しようと試み、1964年には、択捉・国後に対する「南千島」という旧来の呼称に代え、四島を返還要求地域として一括する「北方領土」という用語を使用するよう指示するに至った[215][217]。
	}
	focus = {
		id = JAP_JAP_Japan_PRC_LT_Trade_Agreement
		icon = GFX_Generic_National_Focus_Diplomacy_41
		prerequisite = { focus = JAP_Second_Time_Black_Ships }
		prerequisite = { focus = JAP_Kennedy_Conference }
		cost = 10
		x = 39
		y = 3
		available = {
		}
		completion_reward = {
			custom_effect_tooltip = JAP_JAP_Japan_PRC_LT_Trade_Agreement
			JAP_Japan_PRC_LT_Trade_Agreement = yes
		
			hidden_effect = {
			
				country_event = { id = jap_ikeda.22 days = 3 }
			}
		}
		#アメリカは当時、中国敵視政策を採っており日中接近には極めて警戒的であったが[231]、親中派の石橋湛山に相談し[230]、石橋から「政治問題では松村謙三、経済と貿易問題なら高碕達之助でしょう」との助言を受けた[230]。こうして松村には全権を与え[107]、高碕には事実上の政府特使として日中関係改善にあたらせ[232]、これがLT貿易協定の締結につながった[233][223][234][235]。断絶状態にあった日中関係を再び軌道に乗せることに成功したのである[236][153]。1963年8月には、総額73億5800万円にのぼる倉敷レイヨンの中国向けビニロンプラント輸出にあたり、日本輸出銀行の融資による延べ払いを閣議で了承している[230][107]。
	}
	focus = {
		id = JAP_Join_OECD
		icon = GFX_JAP_Join_OECD
		prerequisite = { focus = JAP_Three_Principle_Theory }
		prerequisite = { focus = JAP_VIsit_SEA }
		cost = 10
		x = 34
		y = 4
		available = {
		}
		completion_reward = {
			set_temp_variable = { JAP_Business_Development_temp = 0.05 }
	        Add_JAP_Business_Development = yes
			set_temp_variable = { JAP_Industry_Development_temp = 0.05 }
	        Add_JAP_Industry_Development = yes
		
			hidden_effect = {
			
				country_event = { id = jap_ikeda.23 days = 3 }
			}
		}
		#池田は訪欧後、日本のOECD加盟の意向を表明[256]。その機運が一気に高まり、池田は米欧提携による日本分裂回避に成功した[171][246][249]。欧州首脳の池田への歓待が、池田の大国意識と結びつき、「三本柱」意識へ昇華したのである[246]。「三本柱」論が重要なのは、第二次世界大戦から立ち直り、経済成長を続ける中で、日本国民にアメリカと欧州に並ぶ「一流国」「先進国」日本という新しいアイデンティティを与えたこと[246]、また自由陣営においてアメリカを超えて欧州へと外交的地平を拡大し「自由陣営の一員」の地位を確立し、日本の国際的地位の向上と、日本の欧州市場参入への糸口をつかんだ[246]。
	}
	focus = {
		id = JAP_Start_Establishment_Of_South_Korea_Diplomatic_Relations
		icon = GFX_JGeneric_National_Focus_Politics_42
		prerequisite = { focus = JAP_Kennedy_Conference }
		cost = 10
		x = 31
		y = 3
		available = {
			has_completed_focus = JAP_The_Asian_Big_Dragon
		}
		completion_reward = {
		
			hidden_effect = {
			
				country_event = { id = jap_ikeda.24 days = 3 }
			}
		}
	}

### Political Tree ###
	focus = {
		id = JAP_Play_Myself_As_Our_Man
		icon = GFX_Generic_National_Focus_Politics_14
		prerequisite = { focus = JAP_The_Ikeda_Administration }
		cost = 10
		x = 18
		y = 1
		available = {
		}
		completion_reward = {
			add_stability = 0.05
			add_political_power = 50
		
			hidden_effect = {
			
				country_event = { id = jap_ikeda.25 days = 3 }
			}
		}
	}
	focus = {
		id = JAP_Shift_The_Season_Of_Politics_To_The_Age_Of_Economics
		icon = GFX_Generic_National_Focus_Economics_10
		prerequisite = { focus = JAP_Play_Myself_As_Our_Man }
		cost = 10
		x = 18
		y = 2
		available = {
		}
		completion_reward = {
			add_timed_idea = {
				idea = Slashed_Interest_Rates
				days = 365
			}
		
			hidden_effect = {
			
				country_event = { id = jap_ikeda.26 days = 3 }
			}
		}
	}
	focus = {
		id = JAP_Promote_Free_Trade
		icon = GFX_Generic_National_Focus_Trading_14
		prerequisite = { focus = JAP_Shift_The_Season_Of_Politics_To_The_Age_Of_Economics }
		cost = 10
		x = 15
		y = 3
		available = {
			has_completed_focus = JAP_Second_Time_Black_Ships
		}
		completion_reward = {
			add_stability = 0.05
		
			hidden_effect = {
			
				country_event = { id = jap_ikeda.27 days = 3 }
			}
		}
	}
	focus = {
		id = JAP_Upholding_Article_9
		icon = GFX_Generic_National_Focus_Politics_52
		prerequisite = { focus = JAP_Shift_The_Season_Of_Politics_To_The_Age_Of_Economics }
		cost = 10
		x = 17
		y = 3
		available = {
		}
		completion_reward = {
			add_stability = 0.05
			add_political_power = 50
		
			hidden_effect = {
			
				country_event = { id = jap_ikeda.28 days = 3 }
			}
		}
	}
	focus = {
		id = JAP_Building_Warefare_State_System
		icon = GFX_Generic_National_Focus_Other_8
		prerequisite = { focus = JAP_Shift_The_Season_Of_Politics_To_The_Age_Of_Economics }
		cost = 10
		x = 19
		y = 3
		available = {
		}
		completion_reward = {
			increase_pensions = yes
		
			hidden_effect = {
			
				country_event = { id = jap_ikeda.29 days = 3 }
			}
		}
	}
	focus = {
		id = JAP_Promote_Rural_To_Urban
		icon = GFX_JAP_Promote_Rural_To_Urban
		prerequisite = { focus = JAP_Shift_The_Season_Of_Politics_To_The_Age_Of_Economics }
		cost = 10
		x = 21
		y = 3
		available = {
		}
		completion_reward = {
			set_temp_variable = { JAP_Agricultural_Development_temp = -0.05 }
			Add_JAP_Agricultural_Development = yes
			capital_scope = {
				add_extra_state_shared_building_slots = 2
				add_building_construction = {
					type = industrial_complex
					level = 1
					instant_build = yes
				}
				add_building_construction = {
					type = water_infrastructure
					level = 1
					instant_build = yes
				}
			}
		
			hidden_effect = {
			
				country_event = { id = jap_ikeda.30 days = 3 }
			}
		}
	}
	focus = {
		id = JAP_Massive_Middle_Class_Society
		icon = GFX_Generic_National_Focus_Politics_22
		prerequisite = { focus = JAP_Building_Warefare_State_System }
		prerequisite = { focus = JAP_Promote_Rural_To_Urban }
		cost = 10
		x = 20
		y = 4
		available = {
		}
		completion_reward = {
			add_timed_idea = {
				idea = Wage_Controls
				days = 365
			}
		
			hidden_effect = {
			
				country_event = { id = jap_ikeda.31 days = 3 }
			}
		}
	}
	focus = {
		id = JAP_Japanese_Economic_Nationalism
		icon = GFX_Generic_National_Focus_Economics_21
		prerequisite = { focus = JAP_Promote_Free_Trade }
		prerequisite = { focus = JAP_Upholding_Article_9 }
		cost = 10
		x = 16
		y = 4
		available = {
			has_completed_focus = JAP_Join_OECD
			has_completed_focus = JAP_Japan_PRC_LT_Trade_Agreement
		}
		completion_reward = {
			JAP = {
				news_event = japan.3 
			}
			add_ideas = JAP_Great_Showa_Consolidation
			every_owned_state = {
				add_extra_state_shared_building_slots = 2
			}
		
			hidden_effect = {
			
				country_event = { id = jap_ikeda.32 days = 3 }
			}
		}
	}
	focus = {
		id = JAP_Tokyo_Olympic
		icon = GFX_JAP_Tokyo_Olympic
		prerequisite = { focus = JAP_Japanese_Economic_Nationalism }
		prerequisite = { focus = JAP_Massive_Middle_Class_Society }
		cost = 10
		x = 18
		y = 5
		available = {
			has_country_flag = JAP_Tokyo_Olympic
		}
		completion_reward = {
			hidden_effect = {
				country_event = { id = jap_ikeda.2 days = 30 }
			
				country_event = { id = jap_ikeda.33 days = 3 }
			}
		}
	}
	focus = {
		id = JAP_Appoint_Eisaku_Sato_As_Successor
		icon = GFX_JAP_Appoint_Eisaku_Sato_As_Successor
		prerequisite = { focus = JAP_Tokyo_Olympic }
		cost = 10
		x = 18
		y = 6
		available = {
			always = no
		}
		completion_reward = {
		
			hidden_effect = {
			
				country_event = { id = jap_ikeda.34 days = 3 }
			}
		}
	}
}
