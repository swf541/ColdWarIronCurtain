
    Mutual_Development_and_Cooperation_Act_Vote = {
            
        allowed = { tag = USA }
        ai_will_do = { factor = 10 }
        
        available = {
            NOT = { has_country_flag = law_passing }
        }
        visible = {
            NOT = { has_country_flag = law_passing }
            has_country_flag = Mutual_Development_and_Cooperation_Act_Vote
        }
        cost = 50
        fire_only_once = yes
        
        complete_effect = {
            set_variable = {					
                bipartisan_value = 0.7
            }	
            set_country_flag = law_passing
            bipartisan_house_calc = yes
            
            hidden_effect = {
                senate_normal_dem_support = yes
                senate_gop_liberal_support = yes
                senate_gop_moderate_support = yes
            }
            
            effect_tooltip = {
                add_political_power = 30
                add_ideas = Mutual_Development_and_Cooperation_Act
            } 			
        }
        days_remove = 50
        remove_effect = {
            hidden_effect = {
                if = {
                    limit = { 
                        check_variable = { supseat > 216 } 
                        check_variable = { supseat_sen > senate_passing_value } 
                    }
                    country_event = { id = us_congress.100 }
                    add_political_power = 30
                    add_ideas = Mutual_Development_and_Cooperation_Act
                }
                if = {
                    limit = { 
                        OR = {
                            check_variable = { supseat < 217 } 
                            check_variable = { supseat_sen < senate_failing_value  } 
                        }
                    }
                    country_event = { id = parliament.1 }
                }
                set_variable = { supseat = 0 }
                set_variable = { supseat_sen = 0 }
                
                clr_country_flag = law_passing
                clear_support_types = yes
            }
        }
    }
    senate_moderate_dem_support
    senate_progressive_dem_support
    senate_dixiecrat_dem_support
    
    senate_gop_moderate_support
    senate_gop_liberal_support
    senate_gop_conservative_support
    
    senate_gop_total_support
    
    senate_normal_dem_support

    if = {
        limit = {
            has_idea = enforce_Consumer_Protection_Laws
        }
        remove_ideas = enforce_Consumer_Protection_Laws
        add_ideas = strengthen_Consumer_Protection_Laws
    }
    if = {
        limit = {
            NOT = { has_idea = enforce_Consumer_Protection_Laws }
        }
        add_ideas = enforce_Consumer_Protection_Laws
    }

    custom_effect_tooltip = ImmigrationIncrease_tt
    add_to_variable = { americanImm = 0.05  }

    lower_tax_rate = yes
    lower_tax_rate = yes
    lower_tax_rate = yes
    lower_tax_rate = yes
    decrease_upper_middle_tax_rate = yes
    decrease_upper_middle_tax_rate = yes
    decrease_lower_middle_tax_rate = yes
    decrease_lower_middle_tax_rate = yes
    decrease_lower_tax_rate = yes
    decrease_lower_tax_rate = yes